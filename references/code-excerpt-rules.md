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

Fixed requirement: code excerpts must not display line numbers. Do not display per-line prefixes such as `001:` and do not add visible line-number columns.

## Minimum Volume

Fixed requirement: the source code excerpt must include at least 3200 lines. Meet this requirement with business-relevant code first. Use framework code only as a supplement.

If either the no-line-number rule or the 3200-line minimum is not satisfied, warn the user that the material may fail review and recommend updating the material before continuing.

## Traceability Report

Write a source manifest containing:

- module name;
- source file path;
- language;
- included line range;
- selected line count;
- selection reason.
