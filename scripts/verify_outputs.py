#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
BAD_CAPTURE_TERMS = (
    "readscreenpixel",
    "desktop",
    "window",
    "win32",
    "screen-region",
    "screen region",
    "cropped to game area",
)
BAD_SCREENSHOT_QUALITIES = {
    "duplicate",
    "duplicate_or_low_value",
    "wrong_window",
    "focus_lost",
    "blank",
    "pure_color",
    "loading_only",
    "low_information",
    "stale_frame",
    "skipped",
    "target_not_reached",
    "postcondition_failed",
    "semantic_mismatch",
}
SYNTHETIC_INTERACTION_TERMS = (
    "synthetic_view_hook",
    "uimanager.showview",
    "direct_showview",
    "model_mutation",
    "debug_state_injected",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def docx_payload(path: Path) -> dict:
    with zipfile.ZipFile(path, "r") as zf:
        names = set(zf.namelist())
        document_xml = zf.read("word/document.xml")
        root = ET.fromstring(document_xml)
    text = "\n".join(node.text or "" for node in root.findall(".//w:t", NS))
    tables = []
    for table in root.findall(".//w:tbl", NS):
        rows = []
        for row in table.findall("w:tr", NS):
            cells = []
            for cell in row.findall("w:tc", NS):
                cell_text = "".join(node.text or "" for node in cell.findall(".//w:t", NS))
                cells.append(clean_cell_text(cell_text))
            rows.append(cells)
        tables.append(rows)
    return {
        "names": names,
        "root": root,
        "text": text,
        "tables": tables,
        "document_xml": document_xml.decode("utf-8", errors="ignore"),
    }


def clean_cell_text(value: str) -> str:
    value = value.replace("\x07", "").replace("\r", "").replace("\n", "")
    return re.sub(r"\s+", " ", value).strip()


def compact(value: str) -> str:
    return re.sub(r"[\s\x07\r\n]+", "", value or "")


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
        "table_count": 0,
        "text": "",
        "tables": [],
    }
    if not path.exists() or path.suffix.lower() != ".docx":
        return result

    payload = docx_payload(path)
    root = payload["root"]
    names = payload["names"]
    text = payload["text"]
    result["comments_part"] = "word/comments.xml" in names
    result["image_count"] = len([name for name in names if name.startswith("word/media/")])
    result["comment_markers"] = len(root.findall(".//w:commentRangeStart", NS)) + len(root.findall(".//w:commentReference", NS))
    result["revision_markers"] = (
        len(root.findall(".//w:ins", NS))
        + len(root.findall(".//w:del", NS))
        + len(root.findall(".//w:moveFrom", NS))
        + len(root.findall(".//w:moveTo", NS))
    )
    result["line_number_markers"] = len(re.findall(r"(?m)^\s*\d+\s*:", text))
    result["table_count"] = len(payload["tables"])
    result["text"] = text
    result["tables"] = payload["tables"]
    return result


def first_file(files, *keywords):
    for path in files:
        name = path.name
        if all(keyword in name for keyword in keywords):
            return path
    return None


def add_docx_common_risks(item: dict, high_risk: list) -> None:
    name = Path(item["path"]).name
    if item["comments_part"] or item["comment_markers"]:
        high_risk.append(f"{name} 含批注部件或批注标记，正式材料应移除批注。")
    if item["revision_markers"]:
        high_risk.append(f"{name} 含修订标记，正式材料应移除修订痕迹。")


def verify_manual(item: dict, high_risk: list) -> None:
    text = item["text"]
    name = Path(item["path"]).name
    if item["image_count"] <= 0:
        high_risk.append(f"{name} 未嵌入截图。")
    if "功能说明：该界面用于展示" in text:
        high_risk.append(f"{name} 存在空壳功能说明：`功能说明：该界面用于展示`。")
    if "截图来源：" in text:
        high_risk.append(f"{name} 将截图路径/来源写进了正式正文；路径应放在报告中。")
    if "本章根据资料包" in text:
        high_risk.append(f"{name} 含生成报告式说明，不符合正式说明书格式。")
    if re.search(r"7\.\d+\s+0\d{2}[-－]", text):
        high_risk.append(f"{name} 第 7 章小节标题疑似直接使用截图文件名，应改成功能系统名称。")
    figure_count = len(re.findall(r"图\s*\d+", text))
    if item["image_count"] and figure_count < item["image_count"]:
        high_risk.append(f"{name} 截图数量为 {item['image_count']}，但图号/图注数量只有 {figure_count}，说明书图注格式不足。")


def verify_source_excerpt(item: dict, high_risk: list) -> None:
    text = item["text"]
    name = Path(item["path"]).name
    if item["line_number_markers"] > 0:
        high_risk.append("源代码节选疑似显示了行号；固定要求为代码不显示行号。")
    if "本模板仅保留标题和页眉" in text:
        high_risk.append(f"{name} 仍保留模板说明文字。")
    if re.search(r"功能备注：本部分代码来源于.*体现游戏界面、功能流程或战斗系统的真实实现", text):
        high_risk.append(f"{name} 存在重复泛化的功能备注，应改为对应功能模块的具体说明。")
    if "代码文件：" not in text:
        high_risk.append(f"{name} 未识别到 `代码文件：` 路径，源码可追溯性不足。")
    selected = re.search(r"源代码节选行数[:：]\s*(\d+)", text)
    if not selected:
        high_risk.append(f"{name} 未识别到源代码节选行数。")
    elif int(selected.group(1)) < 3200:
        high_risk.append(f"{name} 源代码节选行数 {selected.group(1)} 少于 3200 行。")


def next_cell_value(tables, label: str) -> str:
    label_compact = compact(label)
    for table in tables:
        for row in table:
            for index, cell in enumerate(row):
                if label_compact and label_compact in compact(cell):
                    if index + 1 < len(row):
                        return clean_candidate_value(row[index + 1])
                    return ""
    return ""


def clean_candidate_value(value: str) -> str:
    value = clean_cell_text(value)
    if not value:
        return ""
    compacted = compact(value)
    placeholders = {
        "年月日",
        "行",
        "（50字以内）",
        "(50字以内)",
        "（100字以内）",
        "(100字以内)",
        "（500字以上，1300字以内）",
    }
    if compacted in {compact(item) for item in placeholders}:
        return ""
    return value


def verify_application_form(item: dict, high_risk: list) -> None:
    text = item["text"]
    name = Path(item["path"]).name
    if "技术预审填写信息" in text:
        high_risk.append(f"{name} 在登记表后追加了 `技术预审填写信息`，必须改为填入原表格目标单元格。")
    if item["table_count"] <= 0:
        high_risk.append(f"{name} 未识别到登记表表格。")
        return

    required_labels = [
        "软件名称",
        "版本号",
        "分类号",
        "开发的硬件环境",
        "运行的硬件环境",
        "开发该软件的操作系统",
        "软件开发环境/开发工具",
        "该软件的运行平台/操作系统",
        "软件运行支撑环境/支持软件",
        "编程语言",
        "源程序量",
        "开发目的",
        "面向领域/行业",
        "主要功能",
        "技术特点",
    ]
    empty_labels = []
    for label in required_labels:
        if not next_cell_value(item["tables"], label):
            empty_labels.append(label)
    if empty_labels:
        high_risk.append(f"{name} 以下映射字段未在原表格目标单元格中识别到填写值：{', '.join(empty_labels)}。")


def verify_screenshot_manifest(package_dir: Path, high_risk: list, warnings: list) -> None:
    manifest = package_dir / "报告" / "自动截图manifest.json"
    if not manifest.exists():
        return
    try:
        loaded = json.loads(manifest.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        high_risk.append(f"自动截图manifest.json 无法解析：{exc}")
        return
    records = loaded.get("records") if isinstance(loaded, dict) else loaded
    if not isinstance(records, list):
        high_risk.append("自动截图manifest.json 顶层结构不是列表，也不是包含 records 列表的对象。")
        return
    for record in records:
        if not isinstance(record, dict):
            high_risk.append("自动截图manifest.json 存在非对象记录，无法验证截图来源。")
            continue
        method = str(record.get("capture_method", "")).lower()
        focus = str(record.get("focus_dependency", "")).lower()
        quality = str(record.get("quality", "pass")).lower()
        interaction = str(record.get("interaction_method", "")).lower()
        state_injection = str(record.get("state_injection", "")).lower()
        file_name = record.get("file", "<unknown>")
        if quality == "pass":
            for field in ("capture_method", "focus_dependency", "sha256"):
                if not str(record.get(field, "")).strip():
                    high_risk.append(f"{file_name} 自动截图manifest缺少 `{field}`，无法验证截图可靠性。")
            if not interaction:
                high_risk.append(f"{file_name} 自动截图manifest缺少 `interaction_method`，无法区分真实游玩与合成钩子。")
            if (record.get("expected_view") or record.get("expected_text")) and record.get("postcondition_passed") is not True:
                high_risk.append(f"{file_name} 自动截图未通过目标状态校验，不应作为该功能截图进入最终说明书。")
        if any(term in method for term in BAD_CAPTURE_TERMS):
            high_risk.append(f"{file_name} 使用焦点/窗口依赖截图方法 `{record.get('capture_method')}`，不能作为常规自动截图结果。")
        if focus in {"foreground_only", "focus_dependent", "requires_focus"}:
            high_risk.append(f"{file_name} 标记为前台/焦点依赖截图，用户切换应用时可能截错窗口。")
        if quality in BAD_SCREENSHOT_QUALITIES:
            high_risk.append(f"{file_name} 截图质量为 `{quality}`，不应进入最终说明书。")
        if "rendertexture" in method or "render texture" in method:
            cameras = record.get("cameras_rendered", [])
            if not cameras:
                high_risk.append(f"{file_name} 使用 RenderTexture 兜底但未记录渲染相机，可能漏掉 UICamera/Overlay UI。")
            else:
                camera_text = json.dumps(cameras, ensure_ascii=False).lower()
                if "ui" not in camera_text and "canvas" not in camera_text:
                    warnings.append(f"{file_name} 使用 RenderTexture 兜底但相机记录未显示 UI/Canvas 相机，请确认 UI 未丢失。")
        if any(term in interaction for term in SYNTHETIC_INTERACTION_TERMS) or any(term in state_injection for term in SYNTHETIC_INTERACTION_TERMS):
            warnings.append(f"{file_name} 由合成钩子或调试状态生成，应在报告中说明，不能描述成自然游玩路径。")


def verify_duplicate_auto_screenshots(package_dir: Path, high_risk: list) -> None:
    auto_dir = package_dir / "截图" / "自动截图"
    if not auto_dir.exists():
        return
    groups = defaultdict(list)
    for path in sorted(auto_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            groups[sha256(path)].append(path.relative_to(auto_dir).as_posix())
    duplicate_groups = [names for names in groups.values() if len(names) > 1]
    for names in duplicate_groups:
        high_risk.append(f"自动截图存在不同文件同哈希，疑似重复/旧帧：{', '.join(names)}。")


def verify_lock_files(output_dir: Path, high_risk: list) -> None:
    roots = [output_dir]
    skill_root = Path(__file__).resolve().parents[1]
    roots.append(skill_root / "assets" / "templates")
    for root in roots:
        if root.exists():
            locks = sorted(path.name for path in root.glob("~$*"))
            if locks:
                high_risk.append(f"{root} 存在 Word 锁文件：{', '.join(locks)}。")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Unity software copyright output files.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    package_dir = output_dir.parent
    report = Path(args.report)
    report.parent.mkdir(parents=True, exist_ok=True)

    files = sorted([p for p in output_dir.glob("*") if p.is_file()]) if output_dir.exists() else []
    docx_results = [inspect_docx(path) for path in files if path.suffix.lower() == ".docx"]
    by_path = {Path(item["path"]): item for item in docx_results}

    high_risk = []
    warnings = []

    for item in docx_results:
        add_docx_common_risks(item, high_risk)

    missing_kinds = []
    names = " ".join(path.name for path in files)
    manual_path = first_file(files, "说明书")
    source_path = first_file(files, "源代码")
    form_path = first_file(files, "申请表") or first_file(files, "登记")
    if "说明书" not in names:
        missing_kinds.append("游戏软件说明书")
    if "源代码" not in names and "代码" not in names:
        missing_kinds.append("源代码节选")
    if "申请表" not in names and "登记" not in names:
        missing_kinds.append("计算机软件著作权登记申请表")

    if manual_path and manual_path in by_path:
        verify_manual(by_path[manual_path], high_risk)
    if source_path and source_path in by_path:
        verify_source_excerpt(by_path[source_path], high_risk)
    if form_path and form_path in by_path:
        verify_application_form(by_path[form_path], high_risk)

    verify_screenshot_manifest(package_dir, high_risk, warnings)
    verify_duplicate_auto_screenshots(package_dir, high_risk)
    verify_lock_files(output_dir, high_risk)

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
    if warnings:
        lines.append("## 一般提醒")
        for item in warnings:
            lines.append(f"- {item}")
        lines.append("")
    lines.extend(["## 文件", "", "| 文件 | 大小 |", "|---|---:|"])
    for path in files:
        lines.append(f"| {path.name} | {path.stat().st_size} |")
    lines.append("")
    if docx_results:
        lines.extend(
            [
                "## DOCX 检查",
                "",
                "| 文件 | 批注部件 | 批注标记 | 修订标记 | 图片数 | 表格数 | 行号标记 |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for item in docx_results:
            lines.append(
                f"| {Path(item['path']).name} | {item['comments_part']} | {item['comment_markers']} | "
                f"{item['revision_markers']} | {item['image_count']} | {item['table_count']} | {item['line_number_markers']} |"
            )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"REPORT: {report}")
    if missing_kinds or high_risk:
        print("STOP_FOR_USER")
        if missing_kinds:
            print("NEXT_ACTION: 输出目录中未识别到完整三份材料，请确认文件名或重新生成。")
        for item in high_risk:
            print(f"NEXT_ACTION: {item}")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
