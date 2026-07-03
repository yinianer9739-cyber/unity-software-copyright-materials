#!/usr/bin/env python3
import argparse
import hashlib
import json
import struct
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
BATTLE_KEYWORDS = ("战斗", "battle", "fight", "combat", "出征", "战役")
VICTORY_KEYWORDS = ("胜利", "victory", "win", "success")
DEFEAT_KEYWORDS = ("失败", "defeat", "fail", "failure", "lose", "loss")
HP_CHANGE_KEYWORDS = ("血量", "血条", "生命", "hp", "health", "变化", "倒计时", "计时")
LOGIN_KEYWORDS = ("登录", "login")
HEALTH_NOTICE_KEYWORDS = ("健康", "公告", "适龄", "防沉迷", "health", "notice", "announcement")
EXIT_KEYWORDS = ("退出", "exit", "quit", "return", "返回")


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    return None


def jpeg_size(data):
    if not data.startswith(b"\xff\xd8"):
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in (0xD8, 0xD9):
            continue
        length = int.from_bytes(data[i : i + 2], "big")
        if marker in range(0xC0, 0xC4):
            height = int.from_bytes(data[i + 3 : i + 5], "big")
            width = int.from_bytes(data[i + 5 : i + 7], "big")
            return width, height
        i += length
    return None


def image_size(path):
    data = path.read_bytes()[:1024 * 128]
    return png_size(data) or jpeg_size(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan function screenshots.")
    parser.add_argument("--screenshots", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    screenshots = Path(args.screenshots)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not screenshots.exists():
        raise SystemExit(f"Screenshot directory does not exist: {screenshots}")

    screenshots_resolved = screenshots.resolve()
    items = []
    rejected_external = []
    for path in sorted(screenshots.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
            continue
        resolved = path.resolve()
        if not is_relative_to(resolved, screenshots_resolved):
            rejected_external.append(
                {
                    "file": path.relative_to(screenshots).as_posix(),
                    "resolved_path": str(resolved),
                    "reason": "resolved path is outside screenshot directory",
                }
            )
            continue
        size = image_size(path)
        items.append(
            {
                "file": path.relative_to(screenshots).as_posix(),
                "extension": path.suffix.lower(),
                "bytes": path.stat().st_size,
                "modified_time": path.stat().st_mtime,
                "width": size[0] if size else None,
                "height": size[1] if size else None,
                "sha256": sha256(path),
            }
        )

    names = " ".join(item["file"].lower() for item in items)
    warnings = []
    has_login = any(keyword in names for keyword in LOGIN_KEYWORDS)
    has_health_notice = any(keyword in names for keyword in HEALTH_NOTICE_KEYWORDS)
    if not has_login:
        warnings.append("未从文件名识别到登录截图。登录界面是软著说明书常见必备材料，缺失可能影响审核。")
    elif not has_health_notice:
        warnings.append("已识别到登录截图，但未从文件名识别到健康游戏公告/适龄/防沉迷等提示。登录界面必须包含健康游戏公告或等效提示，建议补充或重命名截图以便复核。")
    if not any(keyword in names for keyword in EXIT_KEYWORDS):
        warnings.append("未从文件名识别到退出截图。建议提供退出战斗和退出整个 APP 的截图与说明来源。")
    battle_items = [
        item for item in items
        if any(keyword in item["file"].lower() for keyword in BATTLE_KEYWORDS)
    ]
    if not battle_items:
        warnings.append("未从文件名识别到战斗截图。")

    confirmation_required = []
    if battle_items:
        has_victory = any(
            any(keyword in item["file"].lower() for keyword in VICTORY_KEYWORDS)
            for item in battle_items
        )
        has_defeat = any(
            any(keyword in item["file"].lower() for keyword in DEFEAT_KEYWORDS)
            for item in battle_items
        )
        hp_change_items = [
            item for item in battle_items
            if any(keyword in item["file"].lower() for keyword in HP_CHANGE_KEYWORDS)
        ]
        if not has_victory:
            confirmation_required.append("战斗模块缺失胜利结算截图。")
        if not has_defeat:
            confirmation_required.append("战斗模块缺失失败结算截图。")
        if len(hp_change_items) < 2:
            confirmation_required.append("战斗模块缺失能体现战斗血量变化数据的连续截图，建议至少提供2张。")
        warnings.extend(confirmation_required)
    if rejected_external:
        warnings.append("检测到解析路径位于截图目录之外的图片，已拒绝使用。最终材料只能使用资料包“截图/”内的图片。")

    data = {
        "screenshot_dir": str(screenshots),
        "screenshot_dir_resolved": str(screenshots_resolved),
        "count": len(items),
        "items": items,
        "rejected_external": rejected_external,
        "warnings": warnings,
        "requires_user_confirmation": bool(confirmation_required),
        "confirmation_required": confirmation_required,
    }
    json_path = out_dir / "功能截图清单.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# 功能截图清单", "", f"- 截图目录：`{screenshots}`", f"- 图片数量：{len(items)}", ""]
    if warnings:
        lines.extend(["## 提醒", ""])
        lines.extend(f"- {warning}" for warning in warnings)
        lines.append("")
    if confirmation_required:
        lines.extend(["## 输出前确认", ""])
        lines.append("检测到战斗模块，但战斗截图材料不完整。生成正式材料前应先提醒用户补充以下截图，或由用户明确确认继续：")
        lines.extend(f"- {warning}" for warning in confirmation_required)
        lines.append("")
    if rejected_external:
        lines.extend(["## 已拒绝的外部图片", "", "| 文件 | 解析路径 | 原因 |", "|---|---|---|"])
        for item in rejected_external:
            lines.append(f"| {item['file']} | `{item['resolved_path']}` | {item['reason']} |")
        lines.append("")
    lines.extend(["## 图片", "", "| 文件 | 尺寸 | 大小 | SHA-256 |", "|---|---:|---:|---|"])
    for item in items:
        dim = f"{item['width']}x{item['height']}" if item["width"] and item["height"] else "未识别"
        lines.append(f"| {item['file']} | {dim} | {item['bytes']} | {item['sha256']} |")
    md_path = out_dir / "功能截图清单.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"JSON: {json_path}")
    print(f"MD: {md_path}")
    if confirmation_required:
        print("STOP_FOR_USER: 检测到战斗模块但战斗截图材料不完整。请先提醒用户补充缺失截图，或等待用户明确确认继续。")
        for warning in confirmation_required:
            print(f"- {warning}")
    if rejected_external:
        print("STOP_FOR_USER: 检测到解析路径位于截图目录之外的图片，已拒绝使用。请将需要的图片直接放入资料包的截图目录。")
        for item in rejected_external:
            print(f"- {item['file']} -> {item['resolved_path']}")


if __name__ == "__main__":
    main()
