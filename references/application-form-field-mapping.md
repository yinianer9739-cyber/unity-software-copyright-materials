# Application Form Field Mapping

Use `软著基础信息.zh.yaml` as the authoritative source for the software copyright registration application form. Do not invent registration fields from project code or screenshots when the YAML field is present.

Source program line count is the one mapped field that may be normalized from generated evidence. Generate the source inventory and source code excerpt before the application form. If `登记信息.源程序总行数` is empty, fill it from the computed project-authored source program line count. If the user-filled value differs from the computed value, use the computed value in final materials and report the mismatch.

If a mapped YAML value is empty:

- if `生成设置.是否允许缺失字段标红待补充` is `true`, write red `待补充` in the generated material when the target document supports rich text;
- otherwise stop and ask the user to fill the field;
- always list unresolved mapped fields in `报告/生成结果报告.md`.

## Direct Field Mapping

| YAML field | Application form target |
|---|---|
| `登记信息.软件全称` | 软件全称 |
| `登记信息.软件简称` | 软件简称 |
| `登记信息.版本号` | 版本号 |
| `登记信息.软件分类` | 软件分类 |
| `登记信息.开发完成日期` | 开发完成日期 |
| `登记信息.开发方式` | 开发方式 |
| `登记信息.软件说明` | 软件说明 |
| `登记信息.发表状态` | 发表状态 |
| `登记信息.首次发表日期` | 首次发表日期 |
| `登记信息.权利取得方式` | 权利取得方式 |
| `登记信息.权利范围` | 权利范围 |
| `登记信息.源程序总行数` | 源程序量/源程序总行数 |
| `项目说明.开发目的` | 开发目的 |
| `项目说明.行业/领域` | 行业/领域 |
| `项目说明.主要功能` | 软件的主要功能 |
| `项目说明.技术特点` | 技术特点 |
| `开发运行环境.开发硬件环境` | 开发的硬件环境 |
| `开发运行环境.运行硬件环境` | 运行的硬件环境 |
| `开发运行环境.开发操作系统` | 开发该软件的操作系统 |
| `开发运行环境.软件开发环境/开发工具` | 软件开发环境/开发工具 |
| `开发运行环境.运行平台/操作系统` | 该软件的运行平台/操作系统 |
| `开发运行环境.运行支撑环境/支持软件` | 软件运行支撑环境/支持软件 |
| `开发运行环境.编程语言` | 编程语言 |

## In-Place Table Filling Protocol

The registration application form must be filled inside the copied template's existing form table. Do not append mapped YAML data after the table.

Required procedure:

1. Copy `assets/templates/计算机软件著作权登记申请表模板.doc` to the output directory.
2. Open only the copied output file for editing.
3. Locate the main form table and fill values by nearby labels or known target cells.
4. For each mapped field, write into the target content cell next to or under the label, preserving the label cell itself.
5. For option fields, toggle the existing checkbox/form-control/marker in place.
6. Save the edited copy to the requested output format.
7. Re-open or inspect the saved output and verify the table cells contain the values.

Minimum in-place verification before the application form can be accepted:

- the `软件名称` target cell contains `登记信息.软件全称`;
- the `版本号` target cell contains `登记信息.版本号`;
- the `软件简称` target cell contains `登记信息.软件简称` when provided;
- the `分类号` target cell contains or selects `登记信息.软件分类`;
- software statement, publication status, development method, rights acquisition, and rights scope are selected in place;
- development/runtime environment cells are filled in the `软件功能和技术特点` section;
- `源程序量` contains the normalized computed source line count;
- `开发目的`, `面向领域/行业`, `主要功能`, and `技术特点` target cells are filled or explicitly marked `待补充` according to settings.

If any target label cannot be found, if the target cell cannot be determined, or if a value can only be appended outside the form table, stop and report the blocker. A generated form that contains a trailing section such as `技术预审填写信息` is invalid.

For the bundled legacy `.doc` template on Windows, Word COM is acceptable only with deterministic prompt-free handling:

- open the copied template, not the original template path;
- set `Application.DisplayAlerts = 0`;
- write fields in the copied document;
- use `SaveAs2` or `Save` on the output copy once;
- close documents with `DoNotSaveChanges` after saving the intended output;
- call `Quit` with `DoNotSaveChanges`;
- release COM objects;
- fail if `~$` lock files remain in either `assets/templates/` or `<package-dir>/输出/`.

Do not repeatedly try to dismiss Word save prompts through UI automation. A save prompt means the Word automation sequence is wrong.

## Legal-Team Fields

The following registration fields are intentionally not collected in `软著基础信息.zh.yaml` because legal or operations staff usually provide them. They are ignored for technical pre-review and should be left for legal completion in the registration application form:

- 著作权人/申请人名称;
- 著作权人类型;
- 国家/地区;
- 省市;
- 证件类型;
- 证件号码;
- other applicant identity or legal-entity fields not listed in the direct mapping table.

Do not block technical material generation because these legal-team fields are missing. Mention in `报告/生成结果报告.md` that legal-team fields were excluded from the technical YAML and should be completed by legal staff.

## Checkbox And Option Fields

The following mapped fields are usually checkbox/option fields in the registration application form and must be handled as selections, not as free text inserted beside the label:

- `登记信息.软件分类`;
- `登记信息.开发方式`;
- `登记信息.软件说明`;
- `登记信息.发表状态`;
- `登记信息.权利取得方式`;
- `登记信息.权利范围`;
- `生成设置.申请表输出格式` when it affects final file format.

When editing the application form:

- copy the bundled registration form template first and patch the copy in place;
- preserve the original form tables, controls, row/column counts, page setup, and checkbox/option-marker layout;
- if the template uses Word form fields or checkbox controls, set the corresponding control state;
- if the template uses text such as `□ 原创 □ 修改`, replace only the selected option marker, for example `☑ 原创 □ 修改`;
- if the template is legacy `.doc` and OpenXML cannot safely edit it, use Word COM on Windows and then save to the requested output format;
- if no available tool can preserve the template structure, stop and report the blocker;
- report any checkbox/option field that could not be reliably selected in `报告/生成结果报告.md`.
- never append a separate YAML summary, technical pre-review section, or unmapped report section after the application form.

## Derived Or Supporting Mapping

| YAML field | Application form usage |
|---|---|
| `项目说明.游戏名称` | Used for natural-language descriptions when the form needs a product/game name separate from software full name. |
| `项目说明.游戏类型` | Can support industry/domain wording and main-function wording, but must not replace `项目说明.行业/领域` when that field is filled. |
| `项目说明.游戏概述` | Supports software overview text when the form or attached explanation needs a concise description. |
| `项目说明.用户分析` | Supports user/domain description if required by the form or agency. |
| `项目说明.核心玩法` | Supports main-function expansion. |
| `项目说明.功能特点` | Supports main-function and technical-characteristics expansion. |
| `项目说明.运行平台` | Supports running platform wording, but the primary form field is `开发运行环境.运行平台/操作系统`. |

## Consistency Requirements

- `登记信息.软件全称` must match the application form, manual title/header, and source code excerpt header.
- `登记信息.版本号` must match all final materials.
- `登记信息.源程序总行数` must match the application form and source code excerpt policy/report.
- The application form source program line count must match the normalized source count recorded in `报告/生成结果报告.md`.
- `生成设置.源代码节选是否显示行号` must remain `false` unless the user documents a different legal/agency requirement.
- `生成设置.源代码节选最低行数` must be at least `3200` unless the user documents a different legal/agency requirement.

## Report Requirements

`报告/生成结果报告.md` must include:

- the package YAML path used;
- every YAML field mapped to the application form that was empty;
- every field written as `待补充`;
- any field whose generated value was expanded, summarized, or derived from a supporting YAML field;
- any consistency mismatch found across the application form, manual, and source code excerpt.
