# Auto Fill Rules

Use this optional internal workflow after the user confirms `软著基础信息.zh.yaml` is filled.

Offer this as the third user choice:

```text
3. 自动补充技术特点、开发目的、主要功能后再生成
如果这些字段为空，我会读取 Unity 工程内容，结合已填写信息、源码模块和截图信息生成建议文本。该选项需要 YAML 中已填写 Unity 项目根目录。
```

If `项目路径.Unity项目根目录` is empty, stop and ask the user to fill it before auto-filling.

## Fields

Auto-fill only fields that are empty:

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

`项目说明.主要功能` should be written for the registration application form. It should cover the user-visible software functions that can be supported by screenshots and project evidence, such as startup entry, main screen, gameplay/battle, role or item systems, score/reward/settlement, settings, pause, return, and exit.

## Reporting

When auto-fill is used, write to `报告/生成结果报告.md`:

- which fields were auto-filled;
- which evidence sources were used;
- which fields were not auto-filled and why;
- a reminder that the user should review generated text before final submission.
