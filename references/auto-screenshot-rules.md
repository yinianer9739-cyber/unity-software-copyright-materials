# Auto Screenshot Rules

This is an internal workflow. Do not add these strategy details to the user-facing YAML template.

Use this only after the user confirms `软著基础信息.zh.yaml` is filled.

## User Choice Gate

After the YAML is filled, offer two choices:

1. Directly generate software copyright materials from the current `截图/` directory.
2. Intelligently run the Unity game, generate candidate screenshots, then generate materials.

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
   - Avoid payment, purchase, privacy, user agreement, advertisement, and external-link entries unless the user explicitly asks to capture them.

2. Runtime observation:
   - Open `GameMain.unity` in Unity Editor or a configured local build.
   - Capture the startup/entry screen after the game becomes visually stable.
   - Inspect available UI text/object names when possible.
   - Click likely start/gameplay buttons first.
   - After each action, wait for a stable state, capture a candidate screenshot, and record the action that led there.
   - Avoid repeating identical states by comparing scene name, visible UI text, and screenshot hash when available.

3. Candidate selection:
   - Prefer screenshots that show real game function instead of splash/loading-only states.
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
- actions attempted;
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
- victory, failure, or settlement if reachable;
- battle exit, pause, return, or back entry if reachable;
- whole-app exit or return-to-entry route if reachable;
- buttons or entries shown in screenshots are explainable in the manual.

If a required screenshot type is not found, warn the user that the material may fail review and recommend manual supplementation.

## Safety And Limits

- Use a maximum exploration step count to avoid getting stuck.
- Do not click payment, recharge, purchase, advertisement, privacy policy, user agreement, account deletion, real-name, or external-link actions unless the user explicitly requests it.
- If the project cannot open, cannot enter Play Mode, cannot find `GameMain.unity`, or cannot produce stable screenshots, stop automatic screenshotting and offer direct generation from existing screenshots.
- Automatic screenshotting is an assistant step, not a guarantee of complete legal-review compliance.
