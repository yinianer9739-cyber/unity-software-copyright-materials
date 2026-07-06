# Workflow

## Inputs

At the first-round generation entry only, run the remote `VERSION` check. If the remote version is newer, write the update checkpoint, update the local skill, stop, and tell the user to restart the client and reply `继续`. If the version check fails because the network or remote `VERSION` is unavailable, warn the user and continue with the local skill.

First-round generation entry means the user is starting a new software-copyright workflow from broad intent, such as `软著`, `生成软著`, `启动软著技能`, `software copyright materials`, or asking to create/prepare a materials package.

Do not run the remote `VERSION` check for downstream or resumed workflow actions. Examples: `已填好`, `继续`, `1`, `2`, `3`, `2,3,1`, `2.1`, `2.2`, `2.3`, automatic screenshots, MCP screenshots, auto-fill, screenshot report inspection, source analysis, validation, or final generation for a known materials package directory.

Then ask the user to choose one materials package directory. Create or repair this package:

```text
<package-dir>/
  软著基础信息.zh.yaml
  截图/
  输出/
  报告/
```

Collect these user-confirmed inputs before generating final materials:

1. Filled package YAML at `<package-dir>/软著基础信息.zh.yaml`.
2. Unity project root from `项目路径.Unity项目根目录` in the YAML.
3. Final screenshots placed in `<package-dir>/截图/`, or user confirmation to create candidate screenshots through the automatic screenshot workflow.

The package YAML exists mainly for:

- registration application fields;
- the first six chapters of the game software manual;
- project overview, user analysis, function summary, technical characteristics, and environment fields.

Do not ask the user to fill screenshot or output paths. Those are derived from the package directory.

Do not ask the user to fill code-function mapping tables unless the project evidence is insufficient.

After the user confirms the YAML is filled, offer ordered workflow actions:

1. Directly generate software copyright materials from the current `截图/` directory.
2. Intelligently run the Unity game and generate candidate screenshots.
3. Auto-fill empty project-description fields from project and screenshot evidence.

Tell the user they may reply with one action or an ordered sequence, such as `2,3,1`. Execute actions strictly in the order provided by the user. Do not imply that actions 2 or 3 automatically generate final materials unless action 1 is also selected or the user explicitly asks to generate afterward.

For action 2, ask the user to choose one execution mode before starting screenshots:

1. `2.1 创建临时工程副本自动截图`：recommended. Copy the Unity project to an isolated temporary working directory, excluding generated folders such as `Library`, `Temp`, `Logs`, `Build`, `obj`, and package/cache outputs. Run screenshot automation inside the copy. The user's currently opened Unity instance must not be touched, and the user may continue normal computer work. If Unity shows the administrator-risk modal `Unity is running as administrator`, automatically click `I wish to continue at my own risk` and record the action in the report. If the copy cannot capture valid screenshots, diagnose the failed stage and root cause before offering any fallback.
2. `2.2 接管当前 Unity 实例自动截图`：affects the current Unity state. Tell the user it is best not to operate the mouse or computer globally while this mode runs. Require the user to explicitly reply `我已保存 Unity 当前工作，并允许 Codex 接管当前 Unity 实例进行自动截图。` before proceeding. During this mode, the assistant may switch scenes, enter/exit Play Mode, trigger UI events, and change the current game state. The capture path should still be Unity-internal and focus-independent. If only foreground GameView pixel capture is available, ask for separate foreground-exclusive confirmation and clearly mark that the user must not switch focus.
3. `2.3 使用 Codex MCP + Unity MCP 插件自动截图`：require the user to confirm both `确认1：本机已装 Codex MCP 插件` and `确认2：Unity 引擎也装了 MCP 插件`. Verify callable MCP tools in the current client session before starting. Use MCP to drive Unity and capture screenshots without OS mouse or desktop control, so the user may continue normal computer work. If MCP controls the currently open Unity Editor, record whether Play Mode, scene, or runtime state may be affected.

For all three screenshot modes, warn the user that automatic screenshots are candidates and cannot provide a perfect screenshot list. Tell them to review `报告/自动截图报告.md`, especially battle flow, battle exit, app exit, victory/failure settlement, and clickable secondary interfaces.

If the user chooses automatic screenshots or auto-fill and `项目路径.Unity项目根目录` is empty, stop and ask the user to fill the Unity project root in YAML. Keep automatic screenshot and auto-fill strategy internal; do not expose those details in the YAML except for the optional `截图设置` fields used to choose resolution and screen orientation.

## Generation Stages

1. Run version check and stop for restart if an update is applied only when this request is the first-round generation entry. Skip version check for downstream or resumed workflow actions.
2. Create or repair the package directory.
3. Read and normalize the package YAML.
4. Offer ordered actions for direct generation, intelligent automatic screenshotting, and automatic text completion.
5. If automatic screenshotting is chosen, follow `references/auto-screenshot-rules.md` and write `报告/自动截图报告.md`. A failed temporary-copy run must write a diagnostic result with the failed stage, evidence, root cause or strongest hypothesis, attempted repair, and recommended next action. Real UI/event gameplay exploration is preferred; direct `UIManager.ShowView`, model mutation, or debug state injection is fallback evidence and must be marked in the screenshot manifest. Every planned screenshot must pass target-state validation before it is saved under a semantic filename; otherwise skip it and record the skipped reason.
6. If auto-fill is chosen, follow `references/auto-fill-rules.md`; do not overwrite user-filled text.
7. Analyze Unity project code and produce a candidate source inventory.
8. Scan `<package-dir>/截图/` and produce a screenshot inventory under `<package-dir>/报告/`. Reject any image whose resolved path is outside `<package-dir>/截图/`; final generation must not copy or reuse external screenshots. Images under `<package-dir>/报告/`, including automatic screenshot backups, are diagnostic artifacts and must not be used as final screenshot inputs.
9. Apply the mandatory audit gates and pause on high-risk gaps.
10. Draft a short generation plan that maps YAML fields and whitelisted screenshots to the three templates.
11. Copy each bundled Word template into `<package-dir>/输出/` and patch the copy in place. Never generate a replacement DOC/DOCX from a blank document, and never rebuild the registration-form tables.
12. Generate the source code excerpt, count project-authored source program lines and selected excerpt lines, and update the normalized generation data before generating the registration application form.
13. Patch the three copied template materials in `<package-dir>/输出/`:
   - game software manual;
   - source code excerpt;
   - software copyright registration application form.
14. For the registration application form, apply `references/application-form-field-mapping.md`, fill target cells and option markers inside the original form table, fill the source program line count from the normalized source count, and report every unresolved mapped field. Do not append a technical pre-review/YAML summary section after the form.
15. Verify and write support reports under `<package-dir>/报告/`.
16. Reply with clickable links to the three final files and both support reports.

## Mandatory Audit Gates

Audit these five items before final generation. If any item is missing, inconsistent, or likely non-compliant, warn the user that the material may fail review and recommend updating the material before continuing.

1. Code excerpts must not display line numbers, and the source code excerpt must include at least 3200 lines.
2. Login/startup/entry screen must include a healthy-game notice or equivalent health/game announcement.
3. If account, password, registration, or start-game entries appear on the login/startup/entry screen, explain them in the manual.
4. Recommend providing both battle-exit and whole-app-exit screenshots, plus the source entry or operation for each.
5. If a screenshot shows an unexplained button or entry, recommend adding an explanation or removing that visual element from the screenshot.
6. If screenshots or automatic exploration reveal obvious clickable entries, second-level screens, or switchable tabs, require corresponding screenshots or documented skip reasons.
7. If the battle module has both victory and failure outcomes, require both victory settlement and failure settlement screenshots or a documented reason one outcome could not be reached.

## Template Policy

Use the bundled templates and `references/formal-output-format-rules.md` as formatting and review-style baselines.

Template protection is mandatory:

- copy `assets/templates/游戏软件说明书模板.docx`, `assets/templates/源代码节选模板.docx`, and `assets/templates/计算机软件著作权登记申请表模板.doc` into `输出/` before editing;
- patch only the copied files;
- preserve original page setup, styles, tables, controls, checkbox/option markers, and row/column structure;
- do not use `docx-toolkit`, Markdown conversion, HTML conversion, or any other tool to recreate a new document from scratch;
- for the registration application form, never reconstruct the form table. If safe patching cannot be done, stop and report the blocker.
- for legacy `.doc` registration forms, use deterministic Word COM handling when needed: open a copied template, set `DisplayAlerts = 0`, save the output copy explicitly, close source/template with `DoNotSaveChanges`, release COM objects, and fail if `~$` lock files remain.
- if Word shows or would show a save/discard modal, stop and fix the save/close sequence; do not repeatedly try uncertain UI clicks.

The manual template is intentionally sparse:

- header/title placeholders are replaced with the game name and version from the normalized package YAML;
- the TOC contains only entries `1. 游戏名称` through `7. 游戏系统说明`;
- the body contains only headings `1. 游戏名称` through `7. 游戏系统说明`;
- there must be no fixed `7.1`, `7.2`, or other project-specific sub-sections in the template.

During generation, fill chapters 1-6 from the normalized package YAML fields. Build chapter 7 from the screenshot inventory and project evidence.

The source code excerpt template is also sparse. Generate code sections dynamically from the screenshot-derived function list and the Unity project source inventory.

The final manual and source code excerpt must read like formal submission material, not a generation report. Do not leave template instructions, raw screenshot paths as body copy, empty "功能说明" shells, generic function notes, raw object dumps such as `@{softwareFull=...}`, or section titles copied directly from numbered screenshot filenames.

The final source code excerpt must not include internal workflow/audit explanations such as `代码均来自项目工程源码`, `不显示行号`, `满足 3200 行`, or `根据资料包自动生成`. Keep those facts in reports/manifests, not in the document for reviewers.

Generate the source code excerpt before the registration application form. The source report must include both:

- `源程序总行数`: project-authored source program lines counted from the source inventory, excluding `.meta`, `Library`, `Temp`, build output, minified files, and third-party libraries unless explicitly allowed;
- `源代码节选行数`: actual selected lines included in the excerpt, which must be at least 3200.

If `登记信息.源程序总行数` is empty, fill it in the normalized generation data from `源程序总行数`. If it conflicts with the computed value, use the computed value for final-material consistency and record the mismatch in `报告/生成结果报告.md`.

For iterative legal feedback, use the latest legal feedback document as the base if the user supplies one. Do not regenerate from an older version when the user says legal optimized the document.

## Stop Points

Stop for user confirmation when:

- remote version check updated the local skill and the client must restart;
- package YAML is missing or has not been filled;
- Unity project root is missing or does not look like a Unity project;
- direct generation is requested but the screenshot directory is missing or empty and automatic screenshotting was not selected earlier in the ordered actions;
- the user chose automatic screenshots or auto-fill but Unity project root is missing;
- the user chose automatic screenshots but has not selected mode 2.1/2.2/2.3, has not explicitly confirmed current-instance takeover mode 2.2 when selected, or has not confirmed both MCP plugin prerequisites for mode 2.3;
- automatic screenshots cannot be captured through Unity-internal automation and would require OS mouse control or desktop screenshots;
- temporary-copy Unity launch is blocked by a license, project-lock, missing-module, or recovery modal. The administrator-risk modal must be handled by automatically clicking `I wish to continue at my own risk`; stop only if that auto-click fails or Unity still cannot continue afterward;
- RenderTexture fallback captures only the main/world camera while the actual game UI is on another camera or overlay canvas;
- automatic screenshot state probing shows the expected view/text/state was not reached, the screenshot hash did not change, or the image would be semantically mislabeled; skip that screenshot and continue only with independent scenarios or manual supplementation;
- current-instance automatic screenshots can only be captured through focus-dependent GameView pixels and the user has not explicitly confirmed foreground-exclusive fallback;
- MCP screenshot mode was selected but callable Codex MCP or Unity MCP tools are unavailable in the current client session;
- temporary-copy automatic screenshot mode failed and no diagnostic root cause report has been written;
- a candidate screenshot source resolves outside `<package-dir>/截图/`;
- a candidate screenshot source is under `<package-dir>/报告/` or any other diagnostic/output directory instead of `<package-dir>/截图/`;
- required application fields are empty and the user does not allow red `待补充`;
- source program line count cannot be computed or reconciled before application-form generation;
- bundled Word templates cannot be copied and patched while preserving template structure;
- the registration application form would require appending mapped YAML data outside the original table instead of filling target cells;
- final manual/source/application output contains placeholder/template/report prose flagged by `references/formal-output-format-rules.md`;
- any mandatory audit gate has a high-risk warning and the user has not confirmed how to proceed;
- a screenshot contains visible entries that are not covered by the manual and the intended handling is unclear.
- battle victory/failure settlement or obvious clickable second-level interface screenshots are missing and the user has not confirmed whether to supplement or continue with risk.
