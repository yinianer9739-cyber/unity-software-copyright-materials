#!/usr/bin/env python3
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

CODE_EXTS = {".cs", ".lua", ".shader", ".hlsl", ".compute", ".js", ".boo", ".uxml", ".uss", ".json", ".xml"}
EXCLUDE_PARTS = {"Library", "Temp", "Obj", "obj", "Build", "Builds", "Logs", ".git", ".vs", "node_modules"}
THIRD_PARTY_HINTS = {"Plugins", "ThirdParty", "SDK", "External", "Vendor"}


def skip_path(path: Path) -> bool:
    if path.suffix.lower() == ".meta":
        return True
    return any(part in EXCLUDE_PARTS for part in path.parts)


def is_third_party(path: Path) -> bool:
    return any(part in THIRD_PARTY_HINTS for part in path.parts)


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return ""


def count_lines(path: Path) -> int:
    text = read_text(path)
    return len(text.splitlines()) if text else 0


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(path: Path) -> str:
    lowered = "/".join(part.lower() for part in path.parts)
    if "login" in lowered or "登录" in lowered:
        return "登录/注册"
    if "battle" in lowered or "fight" in lowered or "战斗" in lowered:
        return "战斗"
    if "home" in lowered or "main" in lowered or "主界面" in lowered:
        return "主界面"
    if "shop" in lowered or "store" in lowered or "商城" in lowered:
        return "商城"
    if "mail" in lowered or "email" in lowered or "邮件" in lowered:
        return "邮件"
    if "card" in lowered or "formation" in lowered or "role" in lowered or "hero" in lowered:
        return "卡牌/角色/阵容"
    if "setting" in lowered or "quit" in lowered or "exit" in lowered:
        return "设置/退出"
    return "其他业务/系统"


def unity_version(project: Path) -> str:
    version_file = project / "ProjectSettings" / "ProjectVersion.txt"
    if not version_file.exists():
        return ""
    for line in read_text(version_file).splitlines():
        if "m_EditorVersion:" in line:
            return line.split(":", 1)[1].strip()
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a Unity project for software copyright materials.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--max-candidates", type=int, default=300)
    args = parser.parse_args()

    project = Path(args.project)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not project.exists():
        raise SystemExit(f"Project path does not exist: {project}")

    files = []
    ext_counts = Counter()
    module_counts = Counter()
    total_lines = 0
    for path in project.rglob("*"):
        if not path.is_file() or skip_path(path):
            continue
        ext = path.suffix.lower()
        if ext not in CODE_EXTS:
            continue
        rel = path.relative_to(project).as_posix()
        lines = count_lines(path)
        total_lines += lines
        ext_counts[ext] += 1
        module = classify(path)
        module_counts[module] += 1
        files.append(
            {
                "path": rel,
                "extension": ext,
                "language": {"cs": "C#", "lua": "Lua"}.get(ext.lstrip("."), ext.lstrip(".").upper()),
                "line_count": lines,
                "module_guess": module,
                "third_party_hint": is_third_party(path),
                "sha256": sha256(path) if lines and lines < 20000 else "",
            }
        )

    files.sort(key=lambda item: (item["third_party_hint"], -item["line_count"], item["path"]))
    data = {
        "project": str(project),
        "looks_like_unity": (project / "Assets").exists() and (project / "ProjectSettings").exists(),
        "unity_version": unity_version(project),
        "source_file_count": len(files),
        "source_line_count": total_lines,
        "extension_counts": dict(ext_counts),
        "module_counts": dict(module_counts),
        "candidates": files[: args.max_candidates],
        "exclusions": sorted(EXCLUDE_PARTS | {".meta"}),
    }

    json_path = out_dir / "Unity项目分析.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Unity 项目分析",
        "",
        f"- 项目目录：`{project}`",
        f"- Unity 项目结构：{'是' if data['looks_like_unity'] else '未确认'}",
        f"- Unity 版本：{data['unity_version'] or '未识别'}",
        f"- 源码文件数：{data['source_file_count']}",
        f"- 源码总行数：{data['source_line_count']}",
        "",
        "## 模块候选统计",
        "",
    ]
    for key, value in module_counts.most_common():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 代码候选清单", "", "| 文件 | 语言 | 行数 | 模块猜测 | 第三方提示 |", "|---|---|---:|---|---|"])
    for item in data["candidates"]:
        lines.append(
            f"| {item['path']} | {item['language']} | {item['line_count']} | {item['module_guess']} | {'是' if item['third_party_hint'] else '否'} |"
        )
    md_path = out_dir / "Unity项目分析.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"JSON: {json_path}")
    print(f"MD: {md_path}")


if __name__ == "__main__":
    main()
