# Workflow

## Inputs

At the start, ask whether the user wants to provide basic information in chat or through Excel. Recommend chat input because it is faster for iterative material generation.

Collect four user-confirmed inputs before generating final materials:

1. Basic information, either pasted in chat as Markdown/YAML or filled in the Excel form copied from `assets/templates/Unity游戏软著基础信息填写表模板.xlsx`.
2. One Unity project root.
3. One final screenshot directory.
4. One final output directory.

Chat input and Excel input should normalize to the same field set. The basic information exists mainly for:

- registration application fields;
- the first six chapters of the game software manual;
- project overview, user analysis, function summary, technical characteristics, and environment fields.

If Excel is used, its structure is column A field name, column B user value, column C required marker `*`, and column D note or recommended length.

Do not ask the user to fill code-function mapping tables unless the project evidence is insufficient.

## Generation Stages

1. Collect chat input or copy the Excel form into `<output-dir>/00-用户填写表单/`.
2. Normalize chat input or parse the filled form into JSON and Markdown.
3. Analyze Unity project code and produce a candidate source inventory.
4. Scan the screenshot directory and produce a screenshot inventory.
5. Draft a short generation plan that maps basic information fields and screenshots to the three templates.
6. Patch the three template materials:
   - game software manual;
   - source code excerpt;
   - software copyright registration application form.
7. Verify and write reports.

## Template Policy

Use the bundled templates as formatting and review-style baselines.

The manual template is intentionally sparse:

- header/title placeholders are replaced with the game name and version from the normalized basic information;
- the TOC contains only entries `1. 游戏名称` through `7. 游戏系统说明`;
- the body contains only headings `1. 游戏名称` through `7. 游戏系统说明`;
- there must be no fixed `7.1`, `7.2`, or other project-specific sub-sections in the template.

During generation, fill chapters 1-6 from the normalized basic information fields. Build chapter 7 from the screenshot inventory and project evidence.

The source code excerpt template is also sparse. Generate code sections dynamically from the screenshot-derived function list and the Unity project source inventory.

For iterative legal feedback, use the latest legal feedback document as the base if the user supplies one. Do not regenerate from an older version when the user says legal optimized the document.

## Stop Points

Stop for user confirmation when:

- neither chat input nor an Excel form has supplied the basic information;
- Unity project root is missing or does not look like a Unity project;
- screenshot directory is missing or empty;
- output directory is not confirmed;
- required application fields are empty and the user does not allow red `待补充`;
- a screenshot contains visible entries that are not covered by the manual and the intended handling is unclear.
