# Release Notes

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
