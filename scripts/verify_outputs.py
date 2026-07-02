#!/usr/bin/env python3
import argparse
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path, "r") as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    return "\n".join(node.text or "" for node in root.findall(".//w:t", NS))


def inspect_docx(path: Path) -> dict:
    result = {
        "path": str(path),
        "exists": path.exists(),
        "bytes": path.stat().st_size if path.exists() else 0,
        "comments_part": False,
        "comment_markers": 0,
        "revision_markers": 0,
        "image_count": 0,
        "line_number_markers": 0,
    }
    if not path.exists() or path.suffix.lower() != ".docx":
        return result
    with zipfile.ZipFile(path, "r") as zf:
        names = set(zf.namelist())
        result["comments_part"] = "word/comments.xml" in names
        result["image_count"] = len([name for name in names if name.startswith("word/media/")])
        root = ET.fromstring(zf.read("word/document.xml"))
    result["comment_markers"] = len(root.findall(".//w:commentRangeStart", NS)) + len(root.findall(".//w:commentReference", NS))
    result["revision_markers"] = (
        len(root.findall(".//w:ins", NS))
        + len(root.findall(".//w:del", NS))
        + len(root.findall(".//w:moveFrom", NS))
        + len(root.findall(".//w:moveTo", NS))
    )
    text = docx_text(path)
    result["line_number_markers"] = len(re.findall(r"(?m)^\s*\d+\s*:", text))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Unity software copyright output files.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)

    files = sorted([p for p in output_dir.glob("*") if p.is_file()]) if output_dir.exists() else []
    docx_results = [inspect_docx(path) for path in files if path.suffix.lower() == ".docx"]
    high_risk = []
    for item in docx_results:
        if "代码" in Path(item["path"]).name or "源代码" in Path(item["path"]).name:
            if item["line_number_markers"] > 0:
                high_risk.append("源代码节选疑似显示了行号；固定要求为代码不显示行号，建议更新材料。")
    missing_kinds = []
    names = " ".join(path.name for path in files)
    if "说明书" not in names:
        missing_kinds.append("游戏软件说明书")
    if "源代码" not in names and "代码" not in names:
        missing_kinds.append("源代码节选")
    if "申请表" not in names and "登记" not in names:
        missing_kinds.append("计算机软件著作权登记申请表")

    lines = ["# 验证报告", "", f"- 输出目录：`{output_dir}`", f"- 文件数量：{len(files)}", ""]
    if missing_kinds:
        lines.append("## 缺失提醒")
        for item in missing_kinds:
            lines.append(f"- 未识别到：{item}")
        lines.append("")
    if high_risk:
        lines.append("## 高风险提醒")
        for item in high_risk:
            lines.append(f"- {item}")
        lines.append("")
    lines.extend(["## 文件", "", "| 文件 | 大小 |", "|---|---:|"])
    for path in files:
        lines.append(f"| {path.name} | {path.stat().st_size} |")
    lines.append("")
    if docx_results:
        lines.extend(["## DOCX 检查", "", "| 文件 | 批注部件 | 批注标记 | 修订标记 | 图片数 | 行号标记 |", "|---|---:|---:|---:|---:|---:|"])
        for item in docx_results:
            lines.append(
                f"| {Path(item['path']).name} | {item['comments_part']} | {item['comment_markers']} | {item['revision_markers']} | {item['image_count']} | {item['line_number_markers']} |"
            )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"REPORT: {report}")
    if missing_kinds or high_risk:
        print("STOP_FOR_USER")
        if missing_kinds:
            print("NEXT_ACTION: 输出目录中未识别到完整三份材料，请确认文件名或重新生成。")
        for item in high_risk:
            print(f"NEXT_ACTION: {item}")


if __name__ == "__main__":
    main()
