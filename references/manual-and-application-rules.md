# Manual And Application Rules

## Required Manual Checks

- All screenshots used in the manual must resolve under `<package-dir>/截图/`. Do not use images found outside the package or silently copy external screenshots into the package.
- Login/startup/entry screen must include a healthy-game notice or equivalent health/game announcement. If the PC game has no login or registration, treat the startup or start-game entry screen as the login-equivalent audit screen.
- If account, password, registration, or start-game entries appear on the login/startup/entry screen, explain them in the manual.
- Try to include battle exit and whole-app exit. Explain the source entry for both, such as a battle exit button, main screen exit button, settings button, or mobile back key.
- When a battle module exists, confirm before final output that the screenshot set includes victory result, failure result, and battle HP/blood-bar or equivalent battle-state-change screenshots. If any are missing, pause and ask the user whether to supplement or continue.
- Screenshots should match the final project version supplied by the user.
- If a screenshot shows an unexplained button or function entry, warn that legal/software-copyright review may fail and recommend adding explanation or removing the visual element.
- If screenshots show obvious clickable entries, tabs, toggles, menus, card/list detail entries, rewards, rankings, pause/return controls, or similar second-level functions, the screenshot set should include the corresponding interface whenever safely reachable. If not, report the missing interface and either ask the user to supplement screenshots or explicitly confirm continuing with the risk.

## First Six Manual Chapters

Use the filled package YAML to write or replace chapters 1-6:

- `1. 游戏名称`;
- `2. 运行环境`;
- `3. 游戏类型`;
- `4. 用户分析`;
- `5. 游戏概述`;
- `6. 游戏特征`.

Keep the manual written for ordinary users and legal reviewers. Avoid framework-heavy implementation language in the manual.

## Chapter 7

The template should only contain the heading `7. 游戏系统说明`. Do not keep fixed `7.1` sub-sections in the template.

When generating final materials, create `7.x` sub-sections from the final screenshot directory. Usually each user-facing function screenshot group becomes one section. The section title should use the user-visible function name or a neutral software-copyright name, such as 登录与注册系统、主界面系统、卡牌系统、排行榜系统、宝箱系统、战斗系统、胜利结算、失败结算、退出系统.

## Registration Application Form

Use the package YAML as the source for the registration application form. Follow `references/application-form-field-mapping.md` for field-level mapping; do not rely on loose semantic matching when a mapped YAML field exists.

- software full name, short name, version;
- classification, development completion date, development method;
- hardware/software environment;
- programming languages;
- source program line count;
- development purpose;
- industry/domain;
- main functions;
- technical characteristics.

If the YAML allows missing values, write red `待补充` in final documents for unresolved fields. Report every unresolved field in `报告/生成结果报告.md`.

Legal-team applicant identity fields, such as copyright owner name, owner type, country/region, province/city, certificate type, and certificate number, are intentionally excluded from the technical YAML and should be completed by legal staff. Do not block technical pre-review because these fields are absent from YAML.

For checkbox/option fields such as software classification, development method, software statement, publication status, rights acquisition, and rights scope, select the corresponding option in the application form. Do not merely append the selected value as plain text if the template uses checkboxes or option markers.

Generate the application form after source analysis and source excerpt generation. If `登记信息.源程序总行数` is empty, fill the normalized generation data from the computed project-authored source program line count before patching the form. If the YAML value differs from the computed count, use the computed count for final-material consistency and list the mismatch in `报告/生成结果报告.md`.

## Template Protection

Generate all final Word files by copying the bundled templates and patching the copies in place:

- `assets/templates/游戏软件说明书模板.docx`;
- `assets/templates/源代码节选模板.docx`;
- `assets/templates/计算机软件著作权登记申请表模板.doc`.

Do not create final Word files from blank DOCX documents, Markdown conversion, HTML conversion, or rebuilt table layouts. For the registration application form, preserve the original template table structure, controls, checkbox/option markers, row/column counts, page setup, and spacing. If safe template-preserving editing is unavailable, stop and report the blocker instead of generating a visually different replacement.

## Consistency

The following must match across all final materials:

- software full name;
- version;
- source program line count where shown;
- page/line-number policy for source code excerpt.
