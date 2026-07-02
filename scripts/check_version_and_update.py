#!/usr/bin/env python3
import argparse
import json
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path


REPO = "yinianer9739-cyber/unity-software-copyright-materials"
BRANCHES = ("main", "master")
CHECKPOINT = ".skill-update-checkpoint.json"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_version(value: str):
    result = []
    for part in value.strip().lstrip("v").split("."):
        if part.isdigit():
            result.append(int(part))
        else:
            digits = "".join(ch for ch in part if ch.isdigit())
            result.append(int(digits or "0"))
    while len(result) < 3:
        result.append(0)
    return tuple(result[:3])


def read_local_version(root: Path) -> str:
    version_file = root / "VERSION"
    if not version_file.exists():
        return "0.0.0"
    return version_file.read_text(encoding="utf-8").strip()


def fetch_text(url: str, timeout: int) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8").strip()


def remote_version(timeout: int):
    errors = []
    for branch in BRANCHES:
        url = f"https://raw.githubusercontent.com/{REPO}/{branch}/VERSION"
        try:
            return fetch_text(url, timeout), branch
        except (urllib.error.URLError, TimeoutError) as exc:
            errors.append(f"{branch}: {exc}")
    raise RuntimeError("; ".join(errors))


def download_archive(branch: str, target: Path, timeout: int) -> None:
    url = f"https://github.com/{REPO}/archive/refs/heads/{branch}.zip"
    with urllib.request.urlopen(url, timeout=timeout) as response:
        target.write_bytes(response.read())


def write_checkpoint(root: Path, args, local_version: str, remote: str, branch: str) -> Path:
    checkpoint = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "local_version": local_version,
        "remote_version": remote,
        "remote_branch": branch,
        "package_dir": args.package_dir or "",
        "stage": args.stage or "version-check",
        "resume_instruction": "重启 Codex/其他 AI 客户端后，在对话中回复“继续”。",
    }
    path = root / CHECKPOINT
    path.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def copy_tree_contents(src: Path, dst: Path) -> None:
    for item in src.iterdir():
        if item.name == ".git" or item.name == CHECKPOINT:
            continue
        target = dst / item.name
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            copy_tree_contents(item, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def update_from_archive(root: Path, branch: str, timeout: int) -> None:
    with tempfile.TemporaryDirectory(prefix="unity_soft_copyright_update_") as tmp:
        tmp_path = Path(tmp)
        archive_path = tmp_path / "repo.zip"
        extract_dir = tmp_path / "repo"
        download_archive(branch, archive_path, timeout)
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(extract_dir)
        candidates = [path for path in extract_dir.iterdir() if path.is_dir()]
        if not candidates:
            raise RuntimeError("Downloaded archive has no root directory.")
        copy_tree_contents(candidates[0], root)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check remote skill VERSION and update local skill when remote is newer.")
    parser.add_argument("--package-dir", default="", help="Current materials package directory, used only for checkpoint resume context.")
    parser.add_argument("--stage", default="", help="Current workflow stage, used only for checkpoint resume context.")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--check-only", action="store_true", help="Check versions but do not update.")
    args = parser.parse_args()

    root = skill_root()
    local = read_local_version(root)
    try:
        remote, branch = remote_version(args.timeout)
    except RuntimeError as exc:
        print(f"LOCAL_VERSION: {local}")
        print("VERSION_STATUS: check-failed")
        print(f"VERSION_CHECK_ERROR: {exc}")
        print("NEXT_ACTION: 线上版本检查失败，本次可继续使用本地技能；稍后可重试版本检查。")
        return

    print(f"LOCAL_VERSION: {local}")
    print(f"REMOTE_VERSION: {remote}")
    print(f"REMOTE_BRANCH: {branch}")

    if parse_version(remote) <= parse_version(local):
        print("VERSION_STATUS: up-to-date")
        return

    checkpoint = write_checkpoint(root, args, local, remote, branch)
    print("VERSION_STATUS: update-required")
    print(f"CHECKPOINT: {checkpoint}")

    if args.check_only:
        print("UPDATE_SKIPPED: check-only")
        return

    update_from_archive(root, branch, args.timeout)
    print("UPDATED: true")
    print("STOP_FOR_RESTART")
    print("NEXT_ACTION: 技能已更新到本地。请重启 Codex/其他 AI 客户端，重启后在对话中回复“继续”以恢复未完成流程。")


if __name__ == "__main__":
    main()
