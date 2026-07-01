---
name: unity-software-copyright-materials
description: Use when generating or revising Chinese software copyright materials for Unity game projects, including 软著材料, 游戏软件说明书, 源代码节选, 计算机软件著作权登记申请表, C#, Lua, ToLua, or hot-update game projects.
---

# Unity 游戏软著材料生成

Use this skill for Unity game software copyright materials. It is template-driven and evidence-driven:

- Prefer collecting basic information directly in chat as Markdown or YAML.
- Offer the Excel form only when the user wants a file-based handoff or an agency requires it.
- User provides one Unity project root.
- User provides one final function screenshot directory.
- User provides one final output directory.
- Use the three bundled Word templates:
  - `assets/templates/游戏软件说明书模板.docx`
  - `assets/templates/源代码节选模板.docx`
  - `assets/templates/计算机软件著作权登记申请表模板.doc`

## Basic Information Input

At the start, ask the user which input mode they prefer. Recommend chat input unless they specifically need Excel:

```text
建议直接在聊天里粘贴基础信息，我会整理成软著材料字段；如果你更方便交给同事或代理机构填写，也可以使用 Excel 表单。你想用聊天输入还是 Excel？
```

For chat input, ask the user to paste Markdown or YAML with as many fields as they know. Missing fields may be marked red `待补充` later if the user allows it.

```yaml
软件全称:
软件简称:
版本号: V1.0
软件分类: 应用软件
开发完成日期: YYYY-MM-DD
开发方式: 单独开发
软件说明: 原创
发表状态: 未发表
首次发表日期:
著作权人名称:
著作权人类型:
国家/地区: 中国
省市:
证件类型:
证件号码:
权利取得方式: 原始取得
权利范围: 全部权利
源程序总行数:

游戏名称:
游戏类型:
游戏概述:
开发目的:
用户分析:
核心玩法:
主要功能:
功能特点:
技术特点:
运行平台:

开发硬件环境:
运行硬件环境:
开发操作系统:
软件开发环境/开发工具:
运行平台/操作系统:
运行支撑环境/支持软件:
编程语言:

Unity项目根目录:
功能截图目录:
最终软著材料输出目录:
是否允许缺失字段标红待补充: 是
其他特别要求: 代码不显示行号、源代码节选不少于 3200 行
```

If the user chooses Excel, create or copy the input form in `assets/templates/Unity游戏软著基础信息填写表模板.xlsx`. The form structure is:

- column A: field name;
- column B: user value;
- column C: `*` means required;
- column D: note or recommended length.

Screenshot filenames should help the scanner identify functions. Recommend names such as `登录.png`, `主界面.png`, `战斗_血量变化_1.png`, `战斗_血量变化_2.png`, `战斗_胜利结算.png`, `战斗_失败结算.png`, and `退出.png`.

## Required Workflow

1. Collect basic information through chat or Excel.

   - For chat input, normalize the pasted fields into the same field names used by the Excel form before generating materials.
   - For Excel input, create or copy the Excel input form for the user:

   ```powershell
   python3 <skill>/scripts/create_input_form.py --out-dir <output-dir>
   ```

   If `python3` is unavailable on Windows, use an available Python 3 runtime explicitly. Do not use Python 2.

2. Stop until the user has provided the basic information and confirmed the Unity project root, screenshot directory, and output directory.

3. If Excel was used, parse it:

   ```powershell
   python3 <skill>/scripts/parse_input_form.py --form <xlsx> --out-dir <output-dir>/00-表单解析
   ```

4. Analyze the Unity project:

   ```powershell
   python3 <skill>/scripts/analyze_unity_project.py --project <Unity project root> --out-dir <output-dir>/01-项目分析
   ```

5. Scan the screenshot directory:

   ```powershell
   python3 <skill>/scripts/scan_screenshots.py --screenshots <screenshot-dir> --out-dir <output-dir>/02-截图清单
   ```

6. Generate materials from the templates. Use `docx-toolkit` or Word/OpenXML patching. The manual template intentionally contains only the title/header placeholders, TOC entries 1-7, and body headings 1-7. Generate all section 7 sub-sections dynamically from the user-provided screenshot directory and project evidence. See:

   - `references/workflow.md`
   - `references/manual-and-application-rules.md`
   - `references/code-excerpt-rules.md`
   - `references/validation-rules.md`

7. Verify outputs:

   ```powershell
   python3 <skill>/scripts/verify_outputs.py --output-dir <output-dir>/04-正式材料 --report <output-dir>/验证报告.md
   ```

## Hard Rules

- Do not assume all Unity business code is Lua. Prefer real business code from C#, Lua, ToLua, or other project-specific scripts.
- Exclude `.meta`, `Library`, `Temp`, build output, minified files, and third-party libraries unless the user explicitly requests them.
- Login screenshots must include a healthy-game notice or equivalent health/game announcement.
- If the login screen includes account, password, registration, or start-game entries, the manual must explain them.
- Try to include both battle exit and whole-app exit screenshots and explain the source entry for each.
- If a battle module exists, check before final generation whether victory, failure, and battle HP/blood-bar change screenshots are missing. If any are missing, tell the user what is missing, recommend supplementing it, and wait for user confirmation before output.
- If a screenshot shows a button or entry that the manual does not explain, warn the user that legal review may ask them to add explanation or remove the visual element.
- Missing user-supplied fields may be written as red `待补充` when the form allows it.
- Final material names, headers, and application form software name/version must be consistent.
- Do not add fixed section 7 sub-sections to the manual template. Section 7 details are generated from the final screenshot directory.
- Do not pre-fill the source code excerpt template with fixed modules. Generate code sections according to the screenshot-derived function list and real Unity project source code.

## Output Layout

Use the user-confirmed output directory:

```text
<output-dir>/
  00-用户填写表单/
  00-表单解析/
  01-项目分析/
  02-截图清单/
  03-草稿/
  04-正式材料/
  生成报告.md
  验证报告.md
```

## When Editing DOCX/DOC

Use the built-in `docx-toolkit` skill if available. For `.doc` application-form templates, use Word COM on Windows when needed, then save as `.doc` or `.docx` according to the user's requested final format.

Always verify:

- Comments and tracked revisions are removed from final `.docx` files.
- Required screenshots are embedded.
- Source code excerpt follows the user's line-number preference.
- Code can be traced back to project files, unless the user explicitly documents an exception.
