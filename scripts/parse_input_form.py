#!/usr/bin/env python3
import argparse
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {
    "x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def cell_col(cell_ref: str) -> str:
    return "".join(ch for ch in cell_ref if ch.isalpha())


def load_shared_strings(zf):
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    values = []
    for si in root.findall("x:si", NS):
        parts = [node.text or "" for node in si.findall(".//x:t", NS)]
        values.append("".join(parts))
    return values


def workbook_sheets(zf):
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {}
    for rel in rels.findall("pr:Relationship", NS):
        rel_map[rel.attrib["Id"]] = "xl/" + rel.attrib["Target"].lstrip("/")
    result = []
    for sheet in wb.findall(".//x:sheet", NS):
        name = sheet.attrib["name"]
        rel_id = sheet.attrib.get(f"{{{NS['r']}}}id")
        if rel_id in rel_map:
            result.append((name, rel_map[rel_id]))
    return result


def cell_value(cell, shared):
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//x:t", NS)).strip()
    node = cell.find("x:v", NS)
    if node is None or node.text is None:
        return ""
    raw = node.text
    if cell_type == "s":
        index = int(raw)
        return shared[index] if 0 <= index < len(shared) else ""
    return raw.strip()


def parse_sheet(zf, path, shared):
    root = ET.fromstring(zf.read(path))
    rows = []
    headers = {}
    for row in root.findall(".//x:sheetData/x:row", NS):
        row_index = int(row.attrib.get("r", "0"))
        values = {}
        for cell in row.findall("x:c", NS):
            col = cell_col(cell.attrib.get("r", ""))
            values[col] = cell_value(cell, shared)
        if row_index == 1:
            headers = values
            continue
        field = values.get("A", "").strip()
        if not field:
            continue
        rows.append(
            {
                "field": field,
                "value": values.get("B", "").strip(),
                "required": values.get("C", "").strip() == "*",
                "note": values.get("D", "").strip(),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse the filled Unity software copyright Excel form.")
    parser.add_argument("--form", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    form = Path(args.form)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    data = {"form": str(form), "sheets": {}, "missing_required": []}
    with zipfile.ZipFile(form, "r") as zf:
        shared = load_shared_strings(zf)
        for sheet_name, sheet_path in workbook_sheets(zf):
            rows = parse_sheet(zf, sheet_path, shared)
            data["sheets"][sheet_name] = rows
            for row in rows:
                if row["required"] and not row["value"]:
                    data["missing_required"].append({"sheet": sheet_name, "field": row["field"]})

    json_path = out_dir / "基础信息表单解析.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# 基础信息表单解析", "", f"- 表单：`{form}`", ""]
    for sheet, rows in data["sheets"].items():
        lines.extend([f"## {sheet}", "", "| 字段 | 填写内容 | 必填 |", "|---|---|---|"])
        for row in rows:
            lines.append(f"| {row['field']} | {row['value'] or '未填写'} | {'是' if row['required'] else '否'} |")
        lines.append("")
    if data["missing_required"]:
        lines.append("## 缺失必填项")
        for item in data["missing_required"]:
            lines.append(f"- {item['sheet']} / {item['field']}")
    else:
        lines.append("## 缺失必填项")
        lines.append("- 无")
    md_path = out_dir / "基础信息表单解析.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"JSON: {json_path}")
    print(f"MD: {md_path}")
    if data["missing_required"]:
        print("STOP_FOR_USER")
        print("NEXT_ACTION: 表单仍有必填项未填写；如果允许正式材料标红待补充，请用户确认后继续。")


if __name__ == "__main__":
    main()
