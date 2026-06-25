---
name: unity-software-copyright-materials
description: Generate Chinese software copyright application materials for Unity game projects. Use when the user asks to generate or revise 软著材料, 软件著作权材料, 游戏软件说明书, 源代码节选, or 计算机软件著作权登记申请表 for a Unity project, including C#, Lua, ToLua, hybrid hot-update, or mobile game codebases.
---

# Unity 游戏软著材料生成

Use this skill for Unity game software copyright materials. It is template-driven and form-driven:

- User fills the Excel form in `assets/templates/Unity游戏软著基础信息填写表模板.xlsx`.
- User provides one final function screenshot directory.
- User provides one final output directory.
- Use the three bundled Word templates:
  - `assets/templates/游戏软件说明书模板.docx`
  - `assets/templates/源代码节选模板.docx`
  - `assets/templates/计算机软件著作权登记申请表模板.doc`

## Required Workflow

1. Create or copy the Excel input form for the user:

   ```powershell
   python3 <skill>/scripts/create_input_form.py --out-dir <output-dir>
   ```

   If `python3` is unavailable on Windows, use an available Python 3 runtime explicitly. Do not use Python 2.

2. Stop and ask the user to fill the Excel form. The form is the source of registration fields and the first six chapters of the manual.

3. After the user confirms the form is filled, parse it:

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
