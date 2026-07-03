# Screenshot Rules

Use `<package-dir>/截图/` as the final user-provided screenshot directory.

## Inventory

Scan image files and write:

- file name;
- extension;
- byte size;
- last modified time;
- detected width and height when possible;
- SHA-256 hash.

## Required Reminders

Warn when:

- no screenshot looks like a login screenshot;
- no login/startup/entry screenshot filename or user evidence indicates a healthy-game notice or equivalent health/game announcement;
- no screenshot filename suggests exit, quit, or return;
- no screenshot filename suggests battle/combat;
- the user says login exists but no login image appears.
- screenshot filenames or user evidence suggest account/password/register/start-game entries but the manual plan does not explain them.

For these reminders, tell the user the material may fail review when the issue affects login compliance, exit coverage, or unexplained UI entries.

## Battle Screenshot Confirmation Gate

If screenshot filenames indicate a battle module, check whether the screenshot set includes:

- victory result/settlement screenshots;
- failure result/settlement screenshots;
- at least two battle screenshots that can reasonably show HP/blood-bar change, such as filenames containing blood/HP/health/change/countdown terms.

If any of these are missing, stop before generating final materials. Tell the user exactly which battle screenshots are missing, recommend supplementing them, and continue only after the user either adds the screenshots or explicitly confirms to proceed.

Do not infer detailed UI controls from pixels unless the user explicitly asks for visual inspection. Prefer filename and package YAML evidence.

## Embedding

When patching the manual, verify embedded image hashes when possible. A same filename can be updated; hash is the reliable signal.
