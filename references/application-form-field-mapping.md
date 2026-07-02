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
| `登记信息.著作权人名称` | 著作权人/申请人名称 |
| `登记信息.著作权人类型` | 著作权人类型 |
| `登记信息.国家/地区` | 国家/地区 |
| `登记信息.省市` | 省市 |
| `登记信息.证件类型` | 证件类型 |
| `登记信息.证件号码` | 证件号码 |
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
- `登记信息.著作权人名称` must match every location where the copyright owner appears.
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
