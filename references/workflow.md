# Workflow

## Inputs

At the start, run the remote `VERSION` check. If the remote version is newer, write the update checkpoint, update the local skill, stop, and tell the user to restart the client and reply `继续`. If the version check fails because the network or remote `VERSION` is unavailable, warn the user and continue with the local skill.

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

For action 2, include this user-facing note: `如果当前 Unity 项目已打开，请提前设置好 Game View 窗口分辨率；自动截图会优先沿用该窗口分辨率。`

If the user chooses automatic screenshots or auto-fill and `项目路径.Unity项目根目录` is empty, stop and ask the user to fill the Unity project root in YAML. Keep automatic screenshot and auto-fill strategy internal; do not expose those details in the YAML except for the optional `截图设置` fields used to choose resolution and screen orientation.

## Generation Stages

1. Run version check and stop for restart if an update is applied.
2. Create or repair the package directory.
3. Read and normalize the package YAML.
4. Offer ordered actions for direct generation, intelligent automatic screenshotting, and automatic text completion.
5. If automatic screenshotting is chosen, follow `references/auto-screenshot-rules.md` and write `报告/自动截图报告.md`.
6. If auto-fill is chosen, follow `references/auto-fill-rules.md`; do not overwrite user-filled text.
7. Analyze Unity project code and produce a candidate source inventory.
8. Scan `<package-dir>/截图/` and produce a screenshot inventory under `<package-dir>/报告/`.
9. Apply the mandatory audit gates and pause on high-risk gaps.
10. Draft a short generation plan that maps YAML fields and screenshots to the three templates.
11. Patch the three template materials into `<package-dir>/输出/`:
   - game software manual;
   - source code excerpt;
   - software copyright registration application form.
12. For the registration application form, apply `references/application-form-field-mapping.md` and report every unresolved mapped field.
13. Verify and write support reports under `<package-dir>/报告/`.
14. Reply with clickable links to the three final files and both support reports.

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

Use the bundled templates as formatting and review-style baselines.

The manual template is intentionally sparse:

- header/title placeholders are replaced with the game name and version from the normalized package YAML;
- the TOC contains only entries `1. 游戏名称` through `7. 游戏系统说明`;
- the body contains only headings `1. 游戏名称` through `7. 游戏系统说明`;
- there must be no fixed `7.1`, `7.2`, or other project-specific sub-sections in the template.

During generation, fill chapters 1-6 from the normalized package YAML fields. Build chapter 7 from the screenshot inventory and project evidence.

The source code excerpt template is also sparse. Generate code sections dynamically from the screenshot-derived function list and the Unity project source inventory.

For iterative legal feedback, use the latest legal feedback document as the base if the user supplies one. Do not regenerate from an older version when the user says legal optimized the document.

## Stop Points

Stop for user confirmation when:

- remote version check updated the local skill and the client must restart;
- package YAML is missing or has not been filled;
- Unity project root is missing or does not look like a Unity project;
- direct generation is requested but the screenshot directory is missing or empty and automatic screenshotting was not selected earlier in the ordered actions;
- the user chose automatic screenshots or auto-fill but Unity project root is missing;
- required application fields are empty and the user does not allow red `待补充`;
- any mandatory audit gate has a high-risk warning and the user has not confirmed how to proceed;
- a screenshot contains visible entries that are not covered by the manual and the intended handling is unclear.
- battle victory/failure settlement or obvious clickable second-level interface screenshots are missing and the user has not confirmed whether to supplement or continue with risk.
