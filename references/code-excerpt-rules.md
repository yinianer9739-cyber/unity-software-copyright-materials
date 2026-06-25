# Code Excerpt Rules

## Source Authenticity

Use real project source code whenever possible. Code excerpts should be traceable to project files listed in the analysis report.

Do not restrict business code to Lua. C#, Lua, ToLua, ShaderLab, and other project-authored source files may be used if they show real game functions.

## Organization

Organize code by screenshot-derived functional module. Do not predefine fixed modules in the template. If the screenshot directory contains N user-facing function groups, generate N corresponding code excerpt sections when real source evidence exists.

Add a short Chinese function note before each module, such as:

```text
功能备注：本部分代码体现登录界面账号输入、服务器选择和登录协议处理。
```

Then include relevant file paths and code.

## Line Number Policy

Follow the filled form or user instruction. If the user says not to show line numbers, do not display per-line prefixes and do not add a visible total-line-count paragraph unless required elsewhere.

## Minimum Volume

If the user or agency requires a minimum source excerpt length, meet that requirement with business-relevant code first. Use framework code only as a supplement.

## Traceability Report

Write a source manifest containing:

- module name;
- source file path;
- language;
- included line range;
- selected line count;
- selection reason.
