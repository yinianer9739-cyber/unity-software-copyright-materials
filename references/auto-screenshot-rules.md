# Auto Screenshot Rules

This is an internal workflow. Do not add these strategy details to the user-facing YAML template, except optional screenshot settings such as desired resolution and screen orientation.

Use this only after the user confirms `软著基础信息.zh.yaml` is filled.

## User Choice Gate

After the YAML is filled, offer automatic screenshotting as an ordered workflow action:

```text
2. 智能运行游戏并生成候选截图
如果当前 Unity 项目已打开，请提前设置好 Game View 窗口分辨率；自动截图会优先沿用该窗口分辨率。
```

If the user chooses automatic screenshots and `项目路径.Unity项目根目录` is empty, stop and ask the user to fill the Unity project root in YAML.

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

2. Unity instance and Game View resolution:
   - First detect whether the target Unity project root is already open in a Unity Editor instance.
   - If the target project is already open, do not start a second Unity instance for automatic screenshots. Trigger the automatic screenshot workflow in the existing instance and preserve the user's current Game View resolution.
   - Before triggering screenshots in an already-open project, remind the user to set the Game View to a fixed resolution rather than `Free Aspect`.
   - If the target project is not open, start a Unity Editor instance for the project and set the Game View resolution before entering Play Mode.
   - Default new-instance Game View resolution is `720x1280` for portrait games and `1280x720` for landscape games.
   - Determine portrait vs landscape from project settings, build orientation, common mobile UI/layout evidence, or existing screenshot dimensions. If orientation cannot be determined, default to portrait `720x1280` and report the assumption.
   - If the user specified a desired screenshot resolution in YAML or conversation, use that resolution instead of the default.

3. Runtime observation:
   - Open `GameMain.unity` in the chosen Unity Editor instance or a configured local build.
   - Capture the startup/entry screen after the game becomes visually stable.
   - Inspect available UI text/object names when possible.
   - Click likely start/gameplay buttons first.
   - Systematically explore visible second-level screens and switchable views. If a screen shows obvious tabs, toggles, menu buttons, list/detail entries, chest/reward entries, ranking/card/growth entries, pause/return controls, or other clearly clickable non-sensitive functions, try to open each distinct function at least once and capture the resulting interface.
   - For every visible clickable entry that is not captured, record why it was skipped, such as duplicate screen, unsafe entry, external link, payment/advertising/privacy risk, blocked runtime state, or automation could not reach it.
   - After each action, wait for a stable state, capture a candidate screenshot, and record the action that led there.
   - Avoid repeating identical states by comparing scene name, visible UI text, and screenshot hash when available.
   - If battle has both victory and failure outcomes, attempt to capture both victory settlement and failure settlement. Use debug/test hooks when project evidence shows safe local hooks, or explore normal gameplay paths when reliable. If only one outcome is reachable automatically, report the missing outcome and recommend manual supplementation.

4. Candidate selection:
   - Prefer screenshots that show real game function instead of splash/loading-only states.
   - Prefer coverage of distinct clickable functions over many similar screenshots from one screen.
   - Keep screenshots for obvious second-level or switched interfaces when the entry is visible in another screenshot.
   - Keep candidates that show startup/entry, start button, battle/gameplay, state changes, victory/failure/settlement, pause/exit, and whole-app exit or back-to-entry flow.
   - If multiple screenshots are similar, keep the clearest and most function-rich one.

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
- whether an already-open Unity instance was reused or a new Unity instance was started;
- Game View resolution used, and whether it came from the user-opened instance, YAML/conversation, or default orientation logic;
- actions attempted;
- clickable entries discovered, clicked, captured, skipped, and the reason for each skipped entry;
- screenshots captured;
- recommended screenshots for the manual;
- screenshots rejected as duplicate/loading/low-value;
- audit risks still needing user attention.

Do not overwrite user-provided screenshots. If a final screenshot set needs to mix user and automatic screenshots, explain that in `报告/生成结果报告.md`.

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
- If the project cannot open, cannot enter Play Mode, cannot find `GameMain.unity`, or cannot produce stable screenshots, stop automatic screenshotting and offer direct generation from existing screenshots.
- Automatic screenshotting is an assistant step, not a guarantee of complete legal-review compliance.
