# Unity Project Analysis

## Recognize Project Shape

A Unity project usually contains:

- `Assets/`
- `ProjectSettings/`
- `Packages/`

Relevant code may live in:

- `Assets/Scripts/**/*.cs`
- `Assets/**/Runtime/**/*.cs`
- `Assets/**/Lua/**/*.lua`
- `Assets/**/ToLua/**/*.lua`
- `Assets/**/Shader/**/*.shader`
- project-specific hot-update or resource-loading folders.

Do not assume ToLua or Lua is present.

## Prefer Business Code

Prefer code that shows user-facing game behavior:

- login/register;
- home/main scene;
- battle;
- card/role/formation;
- inventory/equipment/item;
- shop/payment simulation if present;
- mail/reward;
- settings/exit;
- network/protocol models when tied to those features.

Use framework, SDK, generated, or low-level component code only when it directly explains a material requirement or when business code is insufficient.

## Exclusions

Exclude by default:

- `.meta`;
- `Library/`, `Temp/`, `Obj/`, `Build/`, `Builds/`, `Logs/`;
- third-party libraries and SDKs;
- minified generated files;
- binary resources.

Record exclusions in the analysis report.
