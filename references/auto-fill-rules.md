# Auto Fill Rules

Use this optional internal workflow after the user confirms `软著基础信息.zh.yaml` is filled.

Offer this as the third user choice:

```text
3. 自动识别项目内容并补充空字段
如果支持的项目说明字段为空，我会读取 Unity 工程内容，结合已填写信息、源码模块和截图信息生成建议文本。该选项需要 YAML 中已填写 Unity 项目根目录。
```

If `项目路径.Unity项目根目录` is empty, stop and ask the user to fill it before auto-filling.

## Fields

Auto-fill only fields that are empty. Treat template placeholder text such as `请填写...` and a `功能特点` list containing only an empty string as empty.

- `项目说明.游戏概述`: 200-400 Chinese characters;
- `项目说明.用户分析`: 100-200 Chinese characters;
- `项目说明.核心玩法`: 150-300 Chinese characters;
- `项目说明.功能特点`: 4-8 items, each 50-100 Chinese characters;
- `项目说明.技术特点`: 50-100 Chinese characters;
- `项目说明.开发目的`: 50 Chinese characters or fewer;
- `项目说明.主要功能`: 500-1300 Chinese characters.

Do not overwrite user-filled content unless the user explicitly asks for rewriting.

## Evidence Sources

Use available evidence in this order:

1. YAML fields already filled by the user, such as software/game name, game type, overview, user analysis, core gameplay, function features, running platform, programming language.
2. Unity project analysis from `scripts/analyze_unity_project.py`, including module guesses, source languages, project folders, Unity version, and candidate files.
3. Screenshot inventory from `scripts/scan_screenshots.py`.
4. Conventional Unity game architecture only as a fallback.

## Generation Guidance

`项目说明.技术特点` should describe real implementation and runtime traits, such as Unity engine, C#, ShaderLab, UI management, resource loading, configuration, animation, physics, network, data persistence, or platform adaptation. Do not claim Lua/ToLua/hot-update unless project evidence supports it.

`项目说明.开发目的` should be concise and business-neutral, for example providing a high-quality game experience, entertainment, relaxation, and online game service. Avoid advertising language and exaggerated claims.

`项目说明.游戏概述` should describe the game background, product type, entry flow, and what the user mainly does after entering the game. It should be understandable to legal reviewers and ordinary users, not written as engineering documentation.

`项目说明.用户分析` should describe target users, usage scenarios, and suitable player types. Avoid claims about age groups or regulated demographics unless the YAML or project evidence supports them.

`项目说明.核心玩法` should describe the main play loop, such as entry, preparation, growth, battle/gameplay, reward, and return to the main flow.

`项目说明.主要功能` should be written for the registration application form. It should cover the user-visible software functions that can be supported by screenshots and project evidence, such as startup entry, main screen, gameplay/battle, role or item systems, score/reward/settlement, settings, pause, return, and exit.

`项目说明.功能特点` should be written as concrete feature bullets. Each bullet should match project evidence or screenshots, such as startup flow, battle interaction, card/growth, reward/settlement, ranking, resource loading, or platform adaptation. Do not fill it with generic marketing slogans.

## Reporting

When auto-fill is used, write to `报告/生成结果报告.md`:

- which fields were auto-filled;
- which evidence sources were used;
- which fields were not auto-filled and why;
- a reminder that the user should review generated text before final submission.
