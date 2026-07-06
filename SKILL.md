---
name: unity-software-copyright-materials
description: Use when the user mentions 软著, 生成软著, 启动软著技能, software copyright materials, 游戏软件说明书, 源代码节选, 计算机软件著作权登记申请表, or Unity/C#/Lua game copyright submission materials.
---

# Unity 游戏软著材料生成

Use this skill for Unity game software copyright materials. It is package-driven and evidence-driven:

- Check the remote `VERSION` only when the user starts the first-round software-copyright generation workflow.
- Prefer one user-selected materials package directory.
- Store user input in `<package-dir>/软著基础信息.zh.yaml`.
- Derive screenshots from `<package-dir>/截图/`.
- Generate only the three final formal files in `<package-dir>/输出/`.
- Write support reports in `<package-dir>/报告/`.
- Use the three bundled Word templates:
  - `assets/templates/游戏软件说明书模板.docx`
  - `assets/templates/源代码节选模板.docx`
  - `assets/templates/计算机软件著作权登记申请表模板.doc`
- Treat the generated Word files as formal legal-review documents: preserve template structure, fill mapped fields in place, and reject placeholder-like or report-like prose in the final files.

If the user only says a broad keyword such as `软著` and it is unclear whether they want to generate materials, ask whether to start the software copyright generation workflow before creating or editing package content.

## Version Check Gate

Run the GitHub repository version check only for the first-round generation entry, before collecting or generating materials:

```powershell
python3 <skill>/scripts/check_version_and_update.py --stage <current-stage>
```

If `python3` is unavailable on Windows, use an available Python 3 runtime explicitly. Do not use Python 2.

If a materials package directory is already known, also pass `--package-dir <package-dir>` so the checkpoint can resume with more context.

Remote repository: `https://github.com/yinianer9739-cyber/unity-software-copyright-materials.git`.

First-round generation entry means the user is starting a new software-copyright workflow from broad intent, such as `软著`, `生成软著`, `启动软著技能`, `software copyright materials`, or asking to create/prepare a materials package.

Do not run the version check for downstream or resumed workflow actions, even if the skill is triggered. Examples that must skip version check:

- the user replies `已填好`;
- the user replies `继续` after a previous checkpoint or local interruption;
- the user selects ordered actions such as `1`, `2`, `3`, `2,3,1`, `2.1`, `2.2`, or `2.3`;
- the user asks only for automatic screenshots, MCP screenshots, auto-fill, screenshot report inspection, source analysis, validation, or final generation for a known materials package directory;
- the user provides an existing materials package directory and asks to run a later stage directly.

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

- stop immediately after the conditional version check when this is a first-round generation entry;
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
- screenshots are always read from `截图/`; do not ask the user to fill screenshot paths. Never use images outside the user-selected package directory.
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
6. If screenshots or automatic exploration reveal obvious clickable entries, second-level screens, or switchable tabs, require corresponding screenshots or documented skip reasons.
7. If the battle module has both victory and failure outcomes, require both victory settlement and failure settlement screenshots or a documented reason one outcome could not be reached.

## Required Workflow

1. Run the version check gate only when this request is the first-round generation entry. Skip it for downstream or resumed workflow actions.
2. If the user has not provided a materials package directory in this conversation or resume checkpoint, stop and ask for the directory. Do not choose a default path.
3. Create or repair the user-selected materials package directory.
4. Stop until the user fills `软著基础信息.zh.yaml` and optionally places screenshots under `截图/`. Tell the user they may place existing screenshots now, or wait and choose the later automatic screenshot workflow. The stop message must include the exact package paths and this exact instruction: `填写完成后请回复：已填好`.
5. After the user replies `已填好` or otherwise clearly confirms the YAML is filled, offer these ordered workflow actions:

   - `1. 直接生成软著资料`: use the current `截图/` directory.
   - `2. 智能运行游戏并生成候选截图`: try to run the Unity project through Unity-internal automation, explore the game flow, and capture candidate screenshots. After the user chooses this action, ask them to choose one screenshot execution mode:
     - `2.1 创建临时工程副本自动截图`: recommended. Do not take over the user's currently opened Unity instance; the user may continue normal computer work. If Unity shows the administrator-risk dialog, automatically click `I wish to continue at my own risk`. If this mode fails, diagnose and report the failed stage and root cause before offering any fallback.
     - `2.2 接管当前 Unity 实例自动截图`: affects the current Unity state. Tell the user it is best not to operate the mouse or computer globally while this mode runs. Require explicit confirmation: `我已保存 Unity 当前工作，并允许 Codex 接管当前 Unity 实例进行自动截图。` First try Unity-internal capture that is independent of OS focus. If only foreground GameView pixel capture is possible, ask for a separate foreground-exclusive confirmation before using it.
     - `2.3 使用 Codex MCP + Unity MCP 插件自动截图`: require the user to confirm both `确认1：本机已装 Codex MCP 插件` and `确认2：Unity 引擎也装了 MCP 插件`. Use MCP tools to drive Unity and capture screenshots. Do not control the OS mouse or desktop; the user may continue normal computer work. If the MCP connection controls the currently open Unity Editor, record whether Play Mode, scene, or runtime state may be affected.
   - `3. 自动识别项目内容并补充空字段`: if supported YAML fields are empty, infer suggested text from the Unity project, screenshots, and existing YAML fields.

   Tell the user they may reply with one action or an ordered sequence, for example `2,3,1` means first capture screenshots, then auto-fill empty fields, then generate final materials.

   If the user chooses automatic screenshots or auto-fill and `项目路径.Unity项目根目录` is empty, stop and ask the user to fill the Unity project root in YAML.

   Tell the user that all three automatic screenshot modes can miss important review evidence and cannot guarantee a perfect screenshot list. The user must review `报告/自动截图报告.md`, especially battle, battle exit, app exit, victory/failure settlement, and clickable secondary interfaces.

   Automatic screenshot strategy is internal; do not add it to the user YAML except optional `截图设置` resolution/orientation fields. Follow `references/auto-screenshot-rules.md`. Do not use OS mouse control, desktop screenshots, wrong-window screenshots, stale backup screenshots, or focus-dependent GameView pixel captures as normal final automatic screenshot sources.
   Auto-fill strategy is internal; do not add it to the user YAML. Follow `references/auto-fill-rules.md`.

6. Read `项目路径.Unity项目根目录` from YAML and analyze the Unity project:

   ```powershell
   python3 <skill>/scripts/analyze_unity_project.py --project <Unity project root> --out-dir <package-dir>/报告/01-项目分析
   ```

7. Scan screenshots:

   ```powershell
   python3 <skill>/scripts/scan_screenshots.py --screenshots <package-dir>/截图 --out-dir <package-dir>/报告/02-截图清单
   ```

   Screenshot source whitelist is mandatory: final material generation may only use image files whose resolved paths are under `<package-dir>/截图/`. External directories, copied-in guesses from unrelated workspaces, search results, caches, build folders, report backups under `<package-dir>/报告/`, or screenshots outside the package are prohibited. If an image source cannot be traced to the package screenshot directory, stop and ask the user to place the image under `截图/`.

8. Apply the mandatory audit gates. Pause when a gate has a high-risk warning unless the user explicitly confirms to continue.

9. Generate the source code excerpt before the registration application form. Count the project-authored source program lines from the source inventory, count the actual selected excerpt lines, and write both values to `报告/生成结果报告.md`. If `登记信息.源程序总行数` is empty, fill the normalized generation data with the computed source program line count before generating the application form. If it is present but differs from the computed value, use the computed value for final-material consistency and report the mismatch.

10. Generate materials from the bundled templates in template-protection mode. First copy each bundled template into `<package-dir>/输出/`, then patch only placeholders, text runs, checkbox/option markers, table target cells, and image insertion points inside the copied file. Do not rebuild DOC/DOCX files from scratch. Do not recreate, resize, reorder, or replace the registration-form tables. The registration form must be filled in the original table cells/option markers, never by appending a YAML summary section after the form. `docx-toolkit` may only be used for in-template patching. If the legacy `.doc` registration form cannot be safely patched while preserving structure, use Word COM on Windows with deterministic no-prompt save/close handling; if that is unavailable, stop and report the blocker. See:

   - `references/workflow.md`
   - `references/auto-screenshot-rules.md`
   - `references/auto-fill-rules.md`
   - `references/application-form-field-mapping.md`
   - `references/formal-output-format-rules.md`
   - `references/manual-and-application-rules.md`
   - `references/code-excerpt-rules.md`
   - `references/validation-rules.md`

11. Verify outputs:

   ```powershell
   python3 <skill>/scripts/verify_outputs.py --output-dir <package-dir>/输出 --report <package-dir>/报告/验证报告.md
   ```

12. In the final reply, include clickable links to the three final files and support reports.

## Hard Rules

- Do not run the remote `VERSION` check for downstream or resumed workflow actions. If the user provides a known materials package directory, replies with a workflow choice, or asks for screenshots, auto-fill, validation, or final generation from existing package content, treat it as a later-stage action even when the phrase `生成软著` appears in the request.
- Never create or repair a materials package before the user provides the package directory. Do not use default paths such as the current workspace, `outputs/`, or the Unity project directory.
- After creating or repairing the user-selected package, always stop and tell the user to fill `软著基础信息.zh.yaml`, optionally place existing screenshots under `截图/`, or wait for the later automatic screenshot workflow, and reply exactly `已填好` when finished.
- Do not assume all Unity business code is Lua. Prefer real business code from C#, Lua, ToLua, or other project-specific scripts.
- Exclude `.meta`, `Library`, `Temp`, build output, minified files, and third-party libraries unless the user explicitly requests them.
- Code excerpts must not display line numbers and must include at least 3200 lines unless the user explicitly documents a different legal/agency requirement.
- Automatic screenshots must be captured through Unity-internal automation such as a project screenshot hook, Camera/RenderTexture, runtime `ScreenCapture`, temporary Editor runner, current-instance Editor runner, or verified Unity MCP tools. Do not use OS mouse control or desktop/window screenshots as final automatic screenshot evidence. Treat `GameView ReadScreenPixel`, Win32 window capture, and any other focus-dependent pixel capture as foreground-only fallback, not as background-capable capture.
- When automatic screenshotting is requested, offer the three execution modes: temporary project copy (recommended, user may keep using the computer), current Unity instance takeover (requires exact confirmation and the user should avoid operating the mouse/computer while it runs), or Codex MCP + Unity MCP plugin mode (requires both plugin confirmations and callable MCP tools).
- Temporary project copy mode must produce a diagnostic report if it fails. The report must identify the failed stage, log evidence, root cause or strongest hypothesis, and whether the issue is project import, compile error, Play Mode entry, UI flow, capture hook, output copy-back, or screenshot quality.
- Temporary project copy mode must not hang behind Unity startup dialogs. If Unity shows the administrator-risk dialog `Unity is running as administrator`, automatically click `I wish to continue at my own risk` and record the click in the report. License, project-lock, missing-module, and recovery prompts are still launch diagnostics and must not be blindly accepted.
- Runtime `ScreenCapture` should be called after PlayMode `WaitForEndOfFrame`. RenderTexture fallback must render all active game/UI cameras in depth order, including `UICamera` or other UI cameras; a main-camera-only image that misses visible UI is invalid.
- Automatic exploration should prefer real gameplay through Unity UI events such as `Button.onClick` or EventSystem clicks. Direct `UIManager.ShowView`, model mutation, or debug state injection is fallback evidence only and must be marked in the manifest/report.
- Automatic exploration must validate the target state before saving a semantic screenshot filename. Probe visible views/buttons/text before and after every planned action; if the expected view/text/state is not reached, skip that screenshot and record `skipped`, `target_not_reached`, `duplicate`, or `stale_frame` in the manifest. Do not save or keep misleading files such as a main-screen image named as a rank/loadout/pause screenshot.
- Current Unity instance mode must first attempt focus-independent Unity-internal capture. If it can only capture the GameView foreground pixels, pause and ask the user whether to run a foreground-exclusive fallback; if focus changes or the captured frame does not match Unity state, reject the screenshots.
- MCP screenshot mode must verify that both the Codex-side MCP capability and the Unity-side MCP plugin are installed and callable in the current client session before starting. If callable MCP tools are unavailable, stop and ask the user to install/enable the plugins or choose mode 2.1/2.2. MCP mode must still write the same automatic screenshot report and manifest, and must state that automatic screenshots are candidates rather than a complete legal-review guarantee.
- Final materials may only use screenshots from the resolved `<package-dir>/截图/` tree. External image paths, screenshots found outside the package, screenshots under `<package-dir>/报告/`, symlink escapes, web images, caches, and unrelated project folders are prohibited.
- Login/startup/entry screenshots must include a healthy-game notice or equivalent health/game announcement.
- If the login/startup/entry screen includes account, password, registration, or start-game entries, the manual must explain them.
- Try to include both battle exit and whole-app exit screenshots and explain the source entry for each.
- If a battle module exists, check before final generation whether victory, failure, and battle HP/blood-bar change screenshots are missing. If any are missing, tell the user what is missing, recommend supplementing it, and wait for user confirmation before output.
- If obvious clickable entries, second-level screens, or switchable tabs appear in screenshots or automatic exploration, require corresponding interface screenshots or document why they were skipped before final output.
- If a screenshot shows a button or entry that the manual does not explain, warn the user that legal review may ask them to add explanation or remove the visual element.
- Missing user-supplied fields may be written as red `待补充` when the form allows it.
- Final material names, headers, and application form software name/version must be consistent.
- Generate the registration application form from `软著基础信息.zh.yaml` according to `references/application-form-field-mapping.md`; do not treat the YAML as only manual-writing context.
- Generate the application form after source analysis and source excerpt generation so the source program line count can be filled automatically and verified for consistency.
- Do not require legal-team applicant identity fields in the YAML. They are intentionally excluded from technical pre-review and should be completed by legal staff.
- Do not overwrite user-filled YAML text when auto-filling project overview, user analysis, core gameplay, main functions, function features, technical characteristics, or development purpose unless the user explicitly asks for rewriting.
- Do not add fixed section 7 sub-sections to the manual template. Section 7 details are generated from the final screenshot directory.
- Do not pre-fill the source code excerpt template with fixed modules. Generate code sections according to the screenshot-derived function list and real Unity project source code.
- Use template-protection mode for all final Word files: copy bundled templates first, patch copies in place, and never reconstruct the registration form or its tables from a blank document.
- Final manual text must not contain placeholder fragments such as `功能说明：该界面用于展示` without a complete explanation, raw `截图来源：` report prose, or section titles that are merely screenshot filenames.
- Final manual text must not contain raw object dumps such as `@{softwareFull=...}` or all-blue/report-like body prose. It should look like formal reviewer-facing material with a title page, TOC, numbered chapters, functional section headings, explanatory paragraphs, screenshots, and captions.
- Final source code excerpt must not contain template instructions, generic module notes, internal audit/process prose, or visible line numbers. It should use formal module headings, reviewer-facing module notes, file paths, and real source code.
- Do not write internal rules such as `代码均来自项目工程源码`, `不显示行号`, `满足 3200 行`, or `根据资料包自动生成` into final source-code attachment text. Put compliance evidence only in reports/manifests.
- Final registration application form must not contain appended sections such as `技术预审填写信息`. Mapped YAML values belong in the form's existing table cells and option markers.

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

Use the built-in `docx-toolkit` skill only for template-preserving patching. For `.doc` application-form templates, use Word COM on Windows when needed, then save as `.doc` or `.docx` according to the user's requested final format. If preserving the original template structure cannot be guaranteed, stop instead of generating a replacement document.

Always verify:

- Final documents were created by copying bundled templates and patching the copies, not by reconstructing new documents.
- The registration form table layout, controls, option markers, and row/column structure were preserved.
- The registration form mapped YAML values were written into existing target table cells/checkboxes, not appended after the form.
- Word automation used `DisplayAlerts = 0`, saved the output copy deterministically, closed the source/template without save prompts, and left no `~$` lock files in the template or output directories.
- Comments and tracked revisions are removed from final `.docx` files.
- Required screenshots are embedded.
- Manual and source-code excerpt formatting follows `references/formal-output-format-rules.md`.
- Source code excerpt follows the user's line-number preference.
- Source program line count is filled in the registration form and matches the generated source report/normalized data.
- Code can be traced back to project files, unless the user explicitly documents an exception.
