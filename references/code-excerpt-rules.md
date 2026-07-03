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

## Source Program Line Count Closure

Before generating the registration application form:

1. Count project-authored source program lines from the source inventory. Exclude `.meta`, `Library`, `Temp`, build output, minified files, and third-party libraries unless explicitly allowed.
2. Count the actual selected lines included in the source code excerpt.
3. Write both values to `报告/生成结果报告.md`:
   - `源程序总行数`: total project-authored source program lines used for the application form;
   - `源代码节选行数`: selected excerpt lines, which must be at least 3200.
4. If the YAML field `登记信息.源程序总行数` is empty, fill the normalized generation data from `源程序总行数`.
5. If the YAML field is present but differs from the computed value, use the computed value in final documents and report the mismatch.

The registration application form must never be generated with an empty or stale source program line count.

## Traceability Report

Write a source manifest containing:

- module name;
- source file path;
- language;
- included line range;
- selected line count;
- selection reason.

The manifest must also include the final source program line count used in the application form and the selected excerpt line count used to verify the 3200-line minimum.
