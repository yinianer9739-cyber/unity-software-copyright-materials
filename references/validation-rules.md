# Validation Rules

Run verification before reporting completion.

## File Checks

- Final manual exists and is non-empty.
- Final source code excerpt exists and is non-empty.
- Final application form exists and is non-empty.
- `报告/生成结果报告.md` exists.
- `报告/验证报告.md` exists.

## DOCX Checks

For `.docx` files:

- no `word/comments.xml`;
- no comment range markers;
- no tracked revision markers;
- images are embedded;
- required text such as software name and version appears.

## Source Code Checks

- Source code excerpt does not display line numbers.
- Source code excerpt includes at least 3200 selected lines, unless the user documents a different agency requirement.
- Source manifest traces code to project files.
- Excluded folders are not used unless explicitly allowed.

## Manual Checks

- healthy-game notice is represented in login/startup/entry section or unresolved warning is reported;
- login/startup/entry account/password/register/start-game entries are explained when relevant;
- battle exit and whole-app exit are either included or reported as missing/recommended;
- unresolved fields are listed.

## Application Form Checks

- registration application form fields follow `references/application-form-field-mapping.md`;
- empty mapped YAML fields are either written as `待补充` according to the YAML setting or block generation;
- `报告/生成结果报告.md` lists every unresolved mapped application-form field;
- software full name, version, and source program line count match the YAML and all final materials.
- legal-team applicant identity fields are not treated as missing YAML fields during technical pre-review.
- checkbox/option fields are selected according to `references/application-form-field-mapping.md`, or any failed selection is reported in `报告/生成结果报告.md`.
