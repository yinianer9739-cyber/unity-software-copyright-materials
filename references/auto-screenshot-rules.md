# Auto Screenshot Rules

This is an internal workflow. Do not add these strategy details to the user-facing YAML template, except optional screenshot settings such as desired resolution and screen orientation.

Use this only after the user confirms `软著基础信息.zh.yaml` is filled.

## User Choice Gate

After the YAML is filled, offer automatic screenshotting as an ordered workflow action:

```text
2. 智能运行游戏并生成候选截图
请选择自动截图执行模式：
1. 创建临时工程副本自动截图：推荐，较慢，不接管当前 Unity，用户可正常操作电脑。
2. 接管当前 Unity 实例自动截图：较快，但会影响当前 Unity 状态；执行前必须保存工作并明确确认。
```

If the user chooses automatic screenshots and `项目路径.Unity项目根目录` is empty, stop and ask the user to fill the Unity project root in YAML.

If the user chooses current-instance takeover mode, require this exact confirmation before proceeding:

```text
我已保存 Unity 当前工作，并允许 Codex 接管当前 Unity 实例进行自动截图。
```

If the user does not choose a mode, ask for the mode and stop.

## Project Assumptions

Default project architecture:

- Unity entry scene is `GameMain.unity`.
- PC/Editor builds usually do not have login or registration.
- Most games start from an entry screen with a start-like button, then enter battle or gameplay.

When no account/password/registration UI exists, treat the startup or entry screen as the login-equivalent audit screen. The entry screen should still be checked for a healthy-game notice, age notice, anti-addiction notice, or equivalent compliance prompt.

## Exploration Strategy

The goal is not to mechanically wait and screenshot. Try to discover a meaningful game flow and select review-friendly screenshots.

1. Static scan:
   - Find `GameMain.unity`.
   - Scan scenes, prefabs, scripts, UI object names, and text assets for likely flow terms.
   - Favor terms such as `开始`, `开始游戏`, `进入游戏`, `挑战`, `战斗`, `继续`, `下一关`, `暂停`, `返回`, `退出`, `胜利`, `失败`, `结算`, `血量`, `HP`, `分数`, `倒计时`.
   - Build a candidate interaction map for visible or likely clickable entries, including bottom tabs, menu buttons, mode toggles, card/list entries, chest/reward entries, settings, pause, return, and battle/settlement buttons.
   - Mark clearly clickable entries that should have corresponding screenshots for software-copyright review.
   - Avoid payment, purchase, privacy, user agreement, advertisement, and external-link entries unless the user explicitly asks to capture them.

2. Execution mode and Game View resolution:
   - Default to temporary-copy mode when the user accepts it. Do not take over the user's already-open Unity project by default.
   - In temporary-copy mode, create an isolated project copy in a temporary/cache directory. Exclude generated or heavy folders such as `Library`, `Temp`, `Logs`, `Build`, `Builds`, `obj`, `.git`, `.vs`, and local package/cache output when safe. Inject any temporary Editor runner only into the copy. Run Unity against the copy and write screenshots back to `<package-dir>/截图/自动截图/`.
   - In current-instance takeover mode, detect whether the target project root is already open in Unity. Use it only after the exact confirmation above. The runner may open `GameMain.unity`, enter/exit Play Mode, invoke UI events, and change game state. The user should not operate Unity until the action completes.
   - If the target project is not open and the user chose current-instance takeover mode, open the original project only after confirmation; otherwise ask whether to switch to temporary-copy mode.
   - Default new-instance Game View resolution is `720x1280` for portrait games and `1280x720` for landscape games.
   - Determine portrait vs landscape from project settings, build orientation, common mobile UI/layout evidence, or existing screenshot dimensions. If orientation cannot be determined, default to portrait `720x1280` and report the assumption.
   - If the user specified a desired screenshot resolution in YAML or conversation, use that resolution instead of the default.

3. Capture mechanism:
   - Automatic screenshotting must use Unity-internal automation, such as a temporary Editor runner, a project-provided screenshot hook, Camera/RenderTexture capture, `ScreenCapture`, or GameView capture from the Unity process.
   - Do not control the OS mouse or keyboard to click through the game for final automatic screenshots.
   - Do not use desktop/window screenshots as final automatic screenshot sources.
   - If Unity-internal capture cannot be established, stop automatic screenshotting and ask the user to place manual screenshots in `<package-dir>/截图/`.

4. Runtime observation:
   - Open `GameMain.unity` in the chosen Unity Editor instance or a configured local build.
   - Capture the startup/entry screen after the game becomes visually stable.
   - Inspect available UI text/object names when possible.
   - Click likely start/gameplay buttons first.
   - Systematically explore visible second-level screens and switchable views. If a screen shows obvious tabs, toggles, menu buttons, list/detail entries, chest/reward entries, ranking/card/growth entries, pause/return controls, or other clearly clickable non-sensitive functions, try to open each distinct function at least once and capture the resulting interface.
   - For every visible clickable entry that is not captured, record why it was skipped, such as duplicate screen, unsafe entry, external link, payment/advertising/privacy risk, blocked runtime state, or automation could not reach it.
   - After each action, wait for a stable state, capture a candidate screenshot, and record the action that led there.
   - Avoid repeating identical states by comparing scene name, visible UI text, and screenshot hash when available.
   - If battle has both victory and failure outcomes, attempt to capture both victory settlement and failure settlement. Use debug/test hooks when project evidence shows safe local hooks, or explore normal gameplay paths when reliable. If only one outcome is reachable automatically, report the missing outcome and recommend manual supplementation.

5. Candidate selection:
   - Prefer screenshots that show real game function instead of splash/loading-only states.
   - Prefer coverage of distinct clickable functions over many similar screenshots from one screen.
   - Keep screenshots for obvious second-level or switched interfaces when the entry is visible in another screenshot.
   - Keep candidates that show startup/entry, start button, battle/gameplay, state changes, victory/failure/settlement, pause/exit, and whole-app exit or back-to-entry flow.
   - If multiple screenshots are similar, keep the clearest and most function-rich one.
   - Reject pure-color, blank, loading-only, non-Unity, wrong-project, wrong-window, or low-information screenshots. Record rejected screenshots and reasons in the report.

## Screenshot Source Whitelist

Final materials may only use image files whose resolved paths are under:

```text
<package-dir>/截图/
```

Automatic screenshots must be saved under:

```text
<package-dir>/截图/自动截图/
```

Never use screenshots discovered outside the package, including images from the Unity project directory, previous package directories, browser downloads, caches, search results, build output, or unrelated workspace folders. Symlink/reparse-point escapes outside `<package-dir>/截图/` are also prohibited.

If a screenshot is useful but outside the package, stop and ask the user to copy it into `截图/`; do not copy it silently.

## Output

Save automatic screenshots under:

```text
<package-dir>/截图/自动截图/
```

Write the report:

```text
<package-dir>/报告/自动截图报告.md
```

The report must include:

- Unity project root;
- entry scene found or missing;
- execution mode: temporary-copy mode or current-instance takeover mode;
- whether the original project or an isolated copy was used;
- current-instance takeover confirmation text when applicable;
- Game View resolution used, and whether it came from the user-opened instance, YAML/conversation, or default orientation logic;
- capture method, such as Editor runner, project hook, GameView, Camera, RenderTexture, or ScreenCapture;
- actions attempted;
- clickable entries discovered, clicked, captured, skipped, and the reason for each skipped entry;
- screenshots captured;
- recommended screenshots for the manual;
- screenshots rejected as duplicate/loading/low-value;
- audit risks still needing user attention.

Do not overwrite user-provided screenshots. If a final screenshot set needs to mix user and automatic screenshots, explain that in `报告/生成结果报告.md`.

Write `报告/自动截图manifest.json` with one record per captured or rejected screenshot:

```json
{
  "file": "截图/自动截图/003-战斗界面.png",
  "source": "unity_editor_runner",
  "project_root": "D:/Project/Game",
  "working_project_root": "D:/Temp/Game-copy",
  "scene": "Assets/Scenes/GameMain.unity",
  "action": "点击 开始游戏",
  "capture_method": "GameView",
  "quality": "pass"
}
```

## Audit Scoring

Score and select screenshots against these needs:

- startup/entry screen;
- healthy-game notice or equivalent prompt on the startup/entry screen;
- start-game entry;
- battle or core gameplay;
- battle/gameplay state change, such as HP, score, countdown, enemy count, progress, or result changing;
- both victory settlement and failure settlement when battle has both outcomes;
- battle exit, pause, return, or back entry if reachable;
- whole-app exit or return-to-entry route if reachable;
- visible clickable entries have corresponding screenshots or documented skip reasons;
- buttons or entries shown in screenshots are explainable in the manual.

If a required screenshot type is not found, warn the user that the material may fail review and recommend manual supplementation.

## Safety And Limits

- Use a maximum exploration step count to avoid getting stuck.
- Do not click payment, recharge, purchase, advertisement, privacy policy, user agreement, account deletion, real-name, or external-link actions unless the user explicitly requests it.
- Do not take over a currently opened Unity instance without the exact user confirmation.
- Temporary-copy mode must not modify the original Unity project, except reading it to create the copy.
- Current-instance takeover mode may affect the user's Unity state; stop if unsaved-work prompts or project mismatch are detected.
- If the project cannot open, cannot enter Play Mode, cannot find `GameMain.unity`, or cannot produce stable screenshots, stop automatic screenshotting and offer direct generation from existing screenshots.
- Automatic screenshotting is an assistant step, not a guarantee of complete legal-review compliance.
