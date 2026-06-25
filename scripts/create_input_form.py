#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy the Unity software copyright Excel input form.")
    parser.add_argument("--out-dir", required=True, help="Final material workspace/output directory.")
    parser.add_argument("--filename", default="Unity游戏软著基础信息填写表.xlsx")
    args = parser.parse_args()

    template = skill_root() / "assets" / "templates" / "Unity游戏软著基础信息填写表模板.xlsx"
    if not template.exists():
        raise SystemExit(f"Missing template: {template}")

    form_dir = Path(args.out_dir) / "00-用户填写表单"
    form_dir.mkdir(parents=True, exist_ok=True)
    out_path = form_dir / args.filename
    shutil.copy2(template, out_path)

    for name in ["00-表单解析", "01-项目分析", "02-截图清单", "03-草稿", "04-正式材料"]:
        (Path(args.out_dir) / name).mkdir(parents=True, exist_ok=True)

    print(f"FORM: {out_path}")
    print("STOP_FOR_USER")
    print("NEXT_ACTION: 请填写 Excel 表单，并确认功能截图目录和最终软著材料输出目录。")


if __name__ == "__main__":
    main()
