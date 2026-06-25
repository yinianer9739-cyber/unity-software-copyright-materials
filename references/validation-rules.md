# Validation Rules

Run verification before reporting completion.

## File Checks

- Final manual exists and is non-empty.
- Final source code excerpt exists and is non-empty.
- Final application form exists and is non-empty.
- `生成报告.md` exists.
- `验证报告.md` exists.

## DOCX Checks

For `.docx` files:

- no `word/comments.xml`;
- no comment range markers;
- no tracked revision markers;
- images are embedded;
- required text such as software name and version appears.

## Source Code Checks

- Line-number display policy matches the form/user instruction.
- Source manifest traces code to project files.
- Excluded folders are not used unless explicitly allowed.

## Manual Checks

- healthy-game notice is represented in login section or unresolved warning is reported;
- login account/password/register/start-game entries are explained when relevant;
- battle exit and whole-app exit are either included or reported as missing/recommended;
- unresolved fields are listed.
