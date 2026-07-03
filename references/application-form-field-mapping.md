# Application Form Field Mapping

Use `软著基础信息.zh.yaml` as the authoritative source for the software copyright registration application form. Do not invent registration fields from project code or screenshots when the YAML field is present.

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

- if the template uses Word form fields or checkbox controls, set the corresponding control state;
- if the template uses text such as `□ 原创 □ 修改`, replace only the selected option marker, for example `☑ 原创 □ 修改`;
- if the template is legacy `.doc` and OpenXML cannot safely edit it, use Word COM on Windows and then save to the requested output format;
- report any checkbox/option field that could not be reliably selected in `报告/生成结果报告.md`.

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
- `生成设置.源代码节选是否显示行号` must remain `false` unless the user documents a different legal/agency requirement.
- `生成设置.源代码节选最低行数` must be at least `3200` unless the user documents a different legal/agency requirement.

## Report Requirements

`报告/生成结果报告.md` must include:

- the package YAML path used;
- every YAML field mapped to the application form that was empty;
- every field written as `待补充`;
- any field whose generated value was expanded, summarized, or derived from a supporting YAML field;
- any consistency mismatch found across the application form, manual, and source code excerpt.
