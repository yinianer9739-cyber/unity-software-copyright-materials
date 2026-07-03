# Release Notes

## v0.5.0

### Changed

- Updated `VERSION` to `0.5.0`.
- Reworked automatic screenshot execution into two explicit user choices: temporary project copy mode, recommended and slower, or current Unity instance takeover mode, faster but requiring exact user confirmation.
- Made Unity-internal screenshot capture mandatory for automatic screenshots. OS mouse control and desktop/window screenshots are no longer valid final automatic screenshot sources.
- Added a strict screenshot source whitelist: final materials may only use images resolved under the selected package `截图/` directory; external images and symlink escapes are rejected.
- Added screenshot manifest requirements for automatic captures, including source project, working project, scene, action, capture method, and quality result.
- Added template-protection mode for Word output: copy bundled templates first and patch the copies in place; do not rebuild DOC/DOCX files or reconstruct registration-form tables.
- Added source line-count closure: generate/analyze source code before the application form, compute source program line count and selected excerpt line count, fill the application form automatically, and verify consistency.
- Strengthened `scan_screenshots.py` to reject image files whose resolved paths are outside the screenshot directory.

## v0.4.2

### Changed

- Updated `VERSION` to `0.4.2`.
- Expanded skill trigger wording for `软著`, `生成软著`, and `启动软著技能`; broad ambiguous requests should confirm whether to start the generation workflow.
- Clarified package setup messaging so users may place existing screenshots immediately or wait for the later automatic screenshot workflow.
- Reworked post-YAML choices into ordered actions such as `2,3,1`, separating automatic screenshotting, auto-fill, and final generation.
- Expanded auto-fill coverage to include game overview, user analysis, core gameplay, function features, development purpose, main functions, and technical characteristics.
- Added optional YAML screenshot settings for automatic screenshot resolution and screen orientation.
- Updated automatic screenshot rules to prefer an already-open target Unity instance and preserve the user's Game View resolution; new Unity instances default to `720x1280` portrait or `1280x720` landscape.
- Strengthened automatic screenshot coverage for obvious clickable entries, second-level/switchable interfaces, and both victory and failure settlement screenshots when battle outcomes support them.
- Strengthened pre-generation audit rules for missing clickable-interface screenshots and missing victory/failure settlement screenshots.

## v0.4.1

### Changed

- Updated `VERSION` to `0.4.1`.
- Made the user-selected materials package directory a hard workflow gate: the assistant must not default to `outputs/`, the current workspace, or the Unity project directory.
- Required the post-package setup reminder to tell the user to fill `软著基础信息.zh.yaml`, place screenshots under `截图/`, and reply `已填好` before generation choices are offered.

## v0.4.0

### Changed

- Updated `VERSION` to `0.4.0`.
- Removed legal-team applicant identity fields from the user YAML template; these are now documented as legal-team fields outside technical pre-review.
- Added default YAML values for common registration and development/runtime environment fields.
- Changed industry/domain default to `游戏`.
- Added optional auto-fill workflow for technical characteristics, development purpose, and main functions when those fields are empty.
- Added application-form checkbox/option handling rules for registration fields such as software category, development method, software statement, publication status, rights acquisition, and rights scope.
- Release artifacts are now generated under ignored `release/` as versioned zip files instead of `latest` zip files.

## v0.3.0

### Added

- Added `VERSION` with current version `0.3.0`.
- Added package-first workflow: one materials package directory with `软著基础信息.zh.yaml`, `截图/`, `输出/`, and `报告/`.
- Added a full Chinese YAML input template with registration fields, project description, development/runtime environment fields, examples, notes, and option references.
- Added `scripts/create_materials_package.py` to create or repair a materials package without overwriting existing YAML.
- Added `scripts/check_version_and_update.py` to compare local and remote `VERSION`, write an update checkpoint, update from GitHub, and stop for client restart.
- Added mandatory audit gates for line-number-free 3200+ line code excerpts, healthy-game login notice, login-entry explanations, exit screenshots, and unexplained screenshot UI entries.
- Added explicit YAML-to-registration-application-form field mapping without changing the `0.3.0` version number.
- Added internal optional intelligent Unity auto-screenshot workflow after YAML completion, without adding auto-screenshot settings to the user YAML.

### Changed

- `输出/` is now reserved for the three final formal material files only.
- Support reports now belong under `报告/` and should be linked in the final assistant response.
- Screenshot scanning now warns more clearly about login, health notice, exit, and battle screenshot risks.

## v0.2.0

### Changed

- Recommended chat-based Markdown/YAML input as the default way to collect basic software copyright information.
- Kept the Excel form as an optional handoff format for agencies, collaborators, or file-based workflows.
- Updated workflow documentation to require four confirmed inputs: basic information, Unity project root, screenshot directory, and output directory.
- Added README instructions for installing from the GitHub `latest` zip package.
- Updated the MIT license copyright holder for public publishing.

## v0.1.0

Initial public release.

### Included

- Codex skill definition in `SKILL.md`.
- UI metadata in `agents/openai.yaml`.
- Unity game software copyright material templates:
  - basic information Excel form template;
  - game software manual template;
  - source code excerpt template;
  - software copyright registration application form template.
- Reference rules for:
  - workflow;
  - Unity project analysis;
  - screenshot scanning;
  - manual and application form generation;
  - source code excerpt selection;
  - output validation.
- Helper scripts for:
  - creating the input form;
  - parsing the filled form;
  - analyzing a Unity project;
  - scanning screenshot directories;
  - verifying generated outputs.

### Notes

- This release is intended as a Codex skill package.
- Generated software copyright materials should be reviewed before formal submission.
- This project does not provide legal advice.
