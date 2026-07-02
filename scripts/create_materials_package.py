#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


PACKAGE_YAML = "软著基础信息.zh.yaml"
DIRS = ("截图", "输出", "报告")


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or repair a Unity software copyright materials package.")
    parser.add_argument("--package-dir", required=True, help="Materials package root directory.")
    parser.add_argument("--yaml-name", default=PACKAGE_YAML, help="YAML file name to create if missing.")
    args = parser.parse_args()

    package_dir = Path(args.package_dir).expanduser().resolve()
    package_dir.mkdir(parents=True, exist_ok=True)

    created_dirs = []
    for name in DIRS:
        path = package_dir / name
        if not path.exists():
            path.mkdir(parents=True)
            created_dirs.append(str(path))

    template = skill_root() / "assets" / "templates" / "软著基础信息.zh.yaml"
    if not template.exists():
        raise SystemExit(f"Missing YAML template: {template}")

    yaml_path = package_dir / args.yaml_name
    yaml_created = False
    if not yaml_path.exists():
        shutil.copy2(template, yaml_path)
        yaml_created = True

    print(f"PACKAGE_DIR: {package_dir}")
    print(f"YAML: {yaml_path}")
    print(f"SCREENSHOTS_DIR: {package_dir / '截图'}")
    print(f"OUTPUT_DIR: {package_dir / '输出'}")
    print(f"REPORT_DIR: {package_dir / '报告'}")
    if created_dirs:
        print("CREATED_DIRS:")
        for path in created_dirs:
            print(f"- {path}")
    if yaml_created:
        print("YAML_CREATED: true")
        print("NEXT_ACTION: 请填写 YAML，并把功能截图放入“截图”目录。")
    else:
        print("YAML_CREATED: false")
        print("NEXT_ACTION: 已发现现有 YAML，未覆盖；请继续填写或复核该文件。")


if __name__ == "__main__":
    main()
