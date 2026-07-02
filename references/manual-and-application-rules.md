# Manual And Application Rules

## Required Manual Checks

- Login screen must include a healthy-game notice or equivalent health/game announcement.
- If account, password, registration, or start-game entries appear on the login screen, explain them in the manual.
- Try to include battle exit and whole-app exit. Explain the source entry for both, such as a battle exit button, main screen exit button, settings button, or mobile back key.
- When a battle module exists, confirm before final output that the screenshot set includes victory result, failure result, and battle HP/blood-bar change screenshots. If any are missing, pause and ask the user whether to supplement or continue.
- Screenshots should match the final project version supplied by the user.
- If a screenshot shows an unexplained button or function entry, warn that legal/software-copyright review may fail and recommend adding explanation or removing the visual element.

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

When generating final materials, create `7.x` sub-sections from the final screenshot directory. Usually each user-facing function screenshot group becomes one section. The section title should use the user-visible function name or a neutral software-copyright name, such as 登录与注册系统、主界面系统、战斗系统、退出系统.

## Registration Application Form

Use the package YAML as the source for the registration application form. Follow `references/application-form-field-mapping.md` for field-level mapping; do not rely on loose semantic matching when a mapped YAML field exists.

- software full name, short name, version;
- classification, development completion date, development method;
- copyright owner fields;
- hardware/software environment;
- programming languages;
- source program line count;
- development purpose;
- industry/domain;
- main functions;
- technical characteristics.

If the YAML allows missing values, write red `待补充` in final documents for unresolved fields. Report every unresolved field in `报告/生成结果报告.md`.

## Consistency

The following must match across all final materials:

- software full name;
- version;
- copyright owner where shown;
- source program line count where shown;
- page/line-number policy for source code excerpt.
