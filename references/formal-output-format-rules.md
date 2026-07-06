# Formal Output Format Rules

Use these rules when generating or verifying the three final Word files. The goal is formal software-copyright submission material, not a raw generation report.

## Style Baseline

The bundled templates define page setup, styles, and document structure. When a manually prepared reference case is available, use it only as a style benchmark, not as content to copy. A good benchmark has:

- a clear title page;
- a table of contents with numbered chapters, dot leaders, and page numbers when Word can update fields;
- chapters `1. 游戏名称` through `7. 游戏系统说明`;
- chapter 7 split into user-facing systems such as 登录与注册系统、主界面系统、商城系统、卡牌布阵系统、战斗系统、结算系统、退出系统;
- screenshots introduced by explanatory prose, referenced as `见图N`, and followed by captions such as `图N 主界面功能入口`;
- source-code excerpts grouped by function modules, with module headings, function notes, source file paths, and real code.

## Game Software Manual

The manual must be written as a polished formal document:

- Title format should identify software name, version, and `说明书`.
- Prefer a formal first page matching manually prepared cases: centered title, centered `目录`, TOC entries with dot leaders/page numbers, then body content starting after the TOC.
- Chapters 1-6 come from the normalized YAML and should be concise, readable, and aligned with the registration form.
- Chapter 7 is generated from the final screenshot set and project evidence.
- Body formatting should be restrained and formal: blue/bold only for headings, normal body text in black, compact paragraph spacing, no oversized all-blue prose, and no raw object dumps such as `@{softwareFull=...}`.
- Chapter 7 section titles must be functional names, not raw screenshot filenames. Do not use titles like `7.1 001-启动入口或主界面`.
- Every screenshot used in the manual should have surrounding explanatory text and a figure caption. Prefer `图1 登录界面及健康游戏公告`, `图2 主界面功能入口`, etc.
- Body text should explain what the user can do on the screen, which visible buttons or entries are involved, and how it connects to the next flow.
- Do not put raw report details such as `截图来源：截图\自动截图\001-...png` in the formal body. Put traceability paths in reports.
- Do not leave placeholder fragments such as `功能说明：该界面用于展示`, `本章根据资料包...生成`, or any unfinished sentence.
- If screenshots are known duplicates, stale frames, low-value, or missing required audit evidence, report the risk and pause when required; do not hide the risk in generic manual prose.

## Source Code Excerpt

The source code excerpt must look like a formal code attachment:

- Title should identify the software name and `源代码节选`.
- Include software full name, version, source program total line count, and selected excerpt line count.
- Use function module headings that correspond to manual systems or screenshot functions, not arbitrary file groups.
- Each module must include a specific Chinese reviewer-facing module note explaining which user-facing function the code supports.
- A note such as `本部分代码来源于 ... 体现游戏界面、功能流程或战斗系统的真实实现` is too generic when repeated across modules; rewrite it to describe the concrete module.
- Include `代码文件：<project-relative path>` before each file excerpt.
- Use real source code from the project inventory. Code must be traceable in the source manifest.
- Do not display line numbers or a visible line-number column.
- Do not leave template instructions such as `本模板仅保留标题和页眉`.
- Do not include internal process/compliance prose in the final attachment, such as `代码均来自项目工程源码`, `不显示行号`, `满足 3200 行`, `根据资料包自动生成`, or similar audit/generation explanations. Those belong in reports only.

## Registration Application Form

The registration form is a field-fill task, not a report-writing task:

- Copy `assets/templates/计算机软件著作权登记申请表模板.doc` first.
- Preserve the original table, controls, option markers, row/column structure, page setup, and spacing.
- Fill mapped YAML values into the existing target table cells.
- Select checkbox/option fields in place.
- Fill `源程序量` from the normalized computed source line count after the source-code excerpt is generated.
- Never append sections such as `技术预审填写信息（由软著基础信息 YAML 生成）` after the form.
- If a mapped field cannot be located in the form table, stop and report the exact field and label that failed.
- If Word automation cannot save and close without modal prompts, stop and fix the automation sequence before retrying.

## Fail The Output When

Treat any of these as high risk:

- the manual contains raw screenshot paths, filename-only section titles, or empty `功能说明` shells;
- the manual contains raw PowerShell/object dumps such as `@{softwareFull=...}` or reads like a report instead of a formal document;
- the source-code excerpt contains template instructions, internal audit/process prose, repeated generic module notes, visible line numbers, or no project-relative file paths;
- the application form contains appended YAML/report sections or mapped fields are still empty in the table;
- automatic screenshot manifest records show focus-dependent capture, wrong-window capture, stale frames, duplicate function screenshots, or non-pass quality records used as final images;
- Word lock files `~$*` remain in the template or output directory after generation.
