---
name: unity-software-copyright-materials
description: Use when generating or revising Chinese software copyright materials for Unity game projects, including 软著材料, 游戏软件说明书, 源代码节选, 计算机软件著作权登记申请表, C#, Lua, ToLua, or hot-update game projects.
---

# Unity 游戏软著材料生成

Use this skill for Unity game software copyright materials. It is package-driven and evidence-driven:

- Always check the remote `VERSION` before starting the workflow.
- Prefer one user-selected materials package directory.
- Store user input in `<package-dir>/软著基础信息.zh.yaml`.
- Derive screenshots from `<package-dir>/截图/`.
- Generate only the three final formal files in `<package-dir>/输出/`.
- Write support reports in `<package-dir>/报告/`.
- Use the three bundled Word templates:
  - `assets/templates/游戏软件说明书模板.docx`
  - `assets/templates/源代码节选模板.docx`
  - `assets/templates/计算机软件著作权登记申请表模板.doc`

## Version Check Gate

At the start of every skill run, check the GitHub repository version before collecting or generating materials:

```powershell
python3 <skill>/scripts/check_version_and_update.py --stage <current-stage>
```

If `python3` is unavailable on Windows, use an available Python 3 runtime explicitly. Do not use Python 2.

If a materials package directory is already known, also pass `--package-dir <package-dir>` so the checkpoint can resume with more context.

Remote repository: `https://github.com/yinianer9739-cyber/unity-software-copyright-materials.git`.

If the online version check fails because the network or remote `VERSION` is unavailable, warn the user and continue with the local skill.

If the remote `VERSION` is newer than local:

- write `.skill-update-checkpoint.json` in the skill directory;
- update the local skill from GitHub;
- stop immediately;
- tell the user to restart Codex or the current AI client;
- after restart, the user can reply `继续` to resume the unfinished workflow.

## Materials Package

The materials package directory is user-selected and is a non-negotiable workflow gate.

Before creating or repairing any package content, ask the user to provide exactly one materials package directory. The directory may be a new directory or an existing directory. Do not invent, infer, or default this path from the current workspace, `outputs/`, the Unity project path, or any other location.

If no user-selected package directory is known:

- stop immediately after the version check;
- ask the user for the materials package directory address;
- do not create `软著基础信息.zh.yaml`;
- do not create `截图/`, `输出/`, or `报告/`;
- do not continue to YAML collection or generation choices.

After the user provides the package directory, create it if it is new. If it already exists, repair missing directories and never overwrite an existing YAML file.

```powershell
python3 <skill>/scripts/create_materials_package.py --package-dir <package-dir>
```

Package layout:

```text
<package-dir>/
  软著基础信息.zh.yaml
  截图/
  输出/
  报告/
```

Rules:

- `输出/` contains only the three final files: 游戏软件说明书, 源代码节选, 计算机软件著作权登记申请表.
- `报告/` contains support files such as 生成结果报告 and 验证报告.
- screenshots are always read from `截图/`; do not ask the user to fill screenshot paths.
- output path is always `输出/`; do not ask the user to fill output paths.
- the YAML still requires `项目路径.Unity项目根目录`.
- YAML template: `assets/templates/软著基础信息.zh.yaml`.

## Mandatory Audit Gates

Before final generation, audit these five items. If any item is missing, inconsistent, or likely non-compliant, warn the user that the material may fail review and recommend updating the material before continuing.

1. Code excerpts must not display line numbers, and the source code excerpt must include at least 3200 lines.
2. The login/startup/entry screen must include a healthy-game notice or equivalent health/game announcement.
3. If account, password, registration, or start-game entries appear on the login/startup/entry screen, the manual must explain them.
4. Recommend providing both battle-exit and whole-app-exit screenshots, plus the source entry or operation for each.
5. If a screenshot shows a button or entry not explained in the manual, recommend adding an explanation or removing that visual element from the screenshot.

## Required Workflow

1. Run the version check gate.
2. If the user has not provided a materials package directory in this conversation or resume checkpoint, stop and ask for the directory. Do not choose a default path.
3. Create or repair the user-selected materials package directory.
4. Stop until the user fills `软著基础信息.zh.yaml` and places screenshots under `截图/`. The stop message must include the exact package paths and this exact instruction: `填写完成后请回复：已填好`.
5. After the user replies `已填好` or otherwise clearly confirms the YAML is filled, offer these three choices:

   - `1. 直接生成软著资料`: use the current `截图/` directory.
   - `2. 智能运行游戏并生成候选截图后再生成`: try to run the Unity project, explore the game flow, capture candidate screenshots, and then continue generation.
   - `3. 自动补充技术特点、开发目的、主要功能后再生成`: if these YAML fields are empty, infer suggested text from the Unity project, screenshots, and existing YAML fields, then continue generation.

   If the user chooses automatic screenshots or auto-fill and `项目路径.Unity项目根目录` is empty, stop and ask the user to fill the Unity project root in YAML.

   Automatic screenshot strategy is internal; do not add it to the user YAML. Follow `references/auto-screenshot-rules.md`.
   Auto-fill strategy is internal; do not add it to the user YAML. Follow `references/auto-fill-rules.md`.

6. Read `项目路径.Unity项目根目录` from YAML and analyze the Unity project:

   ```powershell
   python3 <skill>/scripts/analyze_unity_project.py --project <Unity project root> --out-dir <package-dir>/报告/01-项目分析
   ```

7. Scan screenshots:

   ```powershell
   python3 <skill>/scripts/scan_screenshots.py --screenshots <package-dir>/截图 --out-dir <package-dir>/报告/02-截图清单
   ```

8. Apply the mandatory audit gates. Pause when a gate has a high-risk warning unless the user explicitly confirms to continue.

9. Generate materials from the templates. Use `docx-toolkit` or Word/OpenXML patching. The manual template intentionally contains only the title/header placeholders, TOC entries 1-7, and body headings 1-7. Generate all section 7 sub-sections dynamically from the screenshot directory and project evidence. See:

   - `references/workflow.md`
   - `references/auto-screenshot-rules.md`
   - `references/auto-fill-rules.md`
   - `references/application-form-field-mapping.md`
   - `references/manual-and-application-rules.md`
   - `references/code-excerpt-rules.md`
   - `references/validation-rules.md`

10. Verify outputs:

   ```powershell
   python3 <skill>/scripts/verify_outputs.py --output-dir <package-dir>/输出 --report <package-dir>/报告/验证报告.md
   ```

11. In the final reply, include clickable links to the three final files and support reports.

## Hard Rules

- Never create or repair a materials package before the user provides the package directory. Do not use default paths such as the current workspace, `outputs/`, or the Unity project directory.
- After creating or repairing the user-selected package, always stop and tell the user to fill `软著基础信息.zh.yaml`, place screenshots under `截图/`, and reply exactly `已填好` when finished.
- Do not assume all Unity business code is Lua. Prefer real business code from C#, Lua, ToLua, or other project-specific scripts.
- Exclude `.meta`, `Library`, `Temp`, build output, minified files, and third-party libraries unless the user explicitly requests them.
- Code excerpts must not display line numbers and must include at least 3200 lines unless the user explicitly documents a different legal/agency requirement.
- Login/startup/entry screenshots must include a healthy-game notice or equivalent health/game announcement.
- If the login/startup/entry screen includes account, password, registration, or start-game entries, the manual must explain them.
- Try to include both battle exit and whole-app exit screenshots and explain the source entry for each.
- If a battle module exists, check before final generation whether victory, failure, and battle HP/blood-bar change screenshots are missing. If any are missing, tell the user what is missing, recommend supplementing it, and wait for user confirmation before output.
- If a screenshot shows a button or entry that the manual does not explain, warn the user that legal review may ask them to add explanation or remove the visual element.
- Missing user-supplied fields may be written as red `待补充` when the form allows it.
- Final material names, headers, and application form software name/version must be consistent.
- Generate the registration application form from `软著基础信息.zh.yaml` according to `references/application-form-field-mapping.md`; do not treat the YAML as only manual-writing context.
- Do not require legal-team applicant identity fields in the YAML. They are intentionally excluded from technical pre-review and should be completed by legal staff.
- Do not overwrite user-filled YAML text when auto-filling technical characteristics, development purpose, or main functions unless the user explicitly asks for rewriting.
- Do not add fixed section 7 sub-sections to the manual template. Section 7 details are generated from the final screenshot directory.
- Do not pre-fill the source code excerpt template with fixed modules. Generate code sections according to the screenshot-derived function list and real Unity project source code.

## Output Layout

Use the user-selected materials package directory:

```text
<package-dir>/
  软著基础信息.zh.yaml
  截图/
  输出/
    游戏软件说明书.docx
    源代码节选.docx
    计算机软件著作权登记申请表.docx
  报告/
    生成结果报告.md
    验证报告.md
```

## When Editing DOCX/DOC

Use the built-in `docx-toolkit` skill if available. For `.doc` application-form templates, use Word COM on Windows when needed, then save as `.doc` or `.docx` according to the user's requested final format.

Always verify:

- Comments and tracked revisions are removed from final `.docx` files.
- Required screenshots are embedded.
- Source code excerpt follows the user's line-number preference.
- Code can be traced back to project files, unless the user explicitly documents an exception.
