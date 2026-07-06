# Auto Screenshot Rules

This is an internal workflow. Do not add these strategy details to the user-facing YAML template, except optional screenshot settings such as desired resolution and screen orientation.

Use this only after the user confirms `软著基础信息.zh.yaml` is filled.

## User Choice Gate

After the YAML is filled, offer automatic screenshotting as an ordered workflow action:

```text
2. 智能运行游戏并生成候选截图
请选择自动截图执行模式：
2.1 创建临时工程副本自动截图：推荐，不接管当前 Unity，用户可正常操作电脑。如果出现 Unity 管理员风险弹窗，会自动点击 I wish to continue at my own risk。失败时必须继续做根因诊断并写报告，不能只说失败或直接改用旧截图。
2.2 接管当前 Unity 实例自动截图：会影响当前 Unity 状态，最好全局不要操控鼠标和电脑。执行前必须明确确认：我已保存 Unity 当前工作，并允许 Codex 接管当前 Unity 实例进行自动截图。默认仍应使用焦点无关的 Unity 内部截图；只有用户另行确认前台独占时，才允许使用 GameView 前台像素兜底。
2.3 使用 Codex MCP + Unity MCP 插件自动截图：需要用户确认本机已装 Codex MCP 插件，并确认 Unity 引擎也装了 MCP 插件。通过 MCP 插件走截图流程，不控制 OS 鼠标或桌面窗口，用户可正常操作电脑；如果 MCP 连接的是当前 Unity Editor，报告中必须说明是否可能影响 Play Mode、场景或运行状态。

三种方式都无法保证提供最完美的截图列表。生成后必须提醒用户查看 `报告/自动截图报告.md`，特别是战斗流程、退出战斗、退出 APP、胜利/失败结算和可点击二级界面。
```

If the user chooses automatic screenshots and `项目路径.Unity项目根目录` is empty, stop and ask the user to fill the Unity project root in YAML.

If the user chooses current-instance takeover mode, require this exact confirmation before proceeding:

```text
我已保存 Unity 当前工作，并允许 Codex 接管当前 Unity 实例进行自动截图。
```

If the user does not choose a mode, ask for the mode and stop.

If the user chooses MCP mode, require both confirmations before proceeding:

```text
确认1：本机已装 Codex MCP 插件
确认2：Unity 引擎也装了 MCP 插件
```

Then verify that callable MCP tools are available in the current client session. If no callable Unity MCP capability is exposed, stop and ask the user to enable/install the plugins or choose mode 2.1/2.2. Do not pretend MCP mode is available based only on the user's local installation statement.

## Project Assumptions

Default project architecture:

- Unity entry scene is `GameMain.unity`.
- PC/Editor builds usually do not have login or registration.
- Most games start from an entry screen with a start-like button, then enter battle or gameplay.

When no account/password/registration UI exists, treat the startup or entry screen as the login-equivalent audit screen. The entry screen should still be checked for a healthy-game notice, age notice, anti-addiction notice, or equivalent compliance prompt.

## Exploration Strategy

The goal is not to mechanically wait and screenshot. Try to discover a meaningful game flow and select review-friendly screenshots.

0. State probe and target validation:
   - Every automatic runner must include a lightweight UI state probe before and after each action. The probe should record active scene, Play Mode state, visible `UIView` objects, visible canvases, visible buttons, button transform paths, button text, interactable state, visible text snippets, top/root UI objects, and a stable state fingerprint.
   - Build an explicit scenario plan before capture. Each scenario must define: intended screenshot name, allowed precondition view/text, preferred action target paths, fallback labels, expected postcondition view/text, whether synthetic state is allowed, and save criteria.
   - Prefer project-specific transform paths discovered from scripts/prefabs over fuzzy text matching. Fuzzy labels are fallback only.
   - Do not save a semantic screenshot filename until its postcondition passes. If a target action cannot be found, a click does not change to the expected view/state, or the expected text is absent, skip that scenario and write a manifest record with `quality: "skipped"` or `quality: "target_not_reached"`.
   - A skipped scenario must not create a misleading final image such as `排行榜.png` that still shows the main screen. Diagnostic captures, if needed, go under `报告/` and are not final screenshot inputs.
   - If a scenario fingerprint or screenshot hash is unchanged from the pre-action state, reject it as `stale_frame` or `duplicate` and exclude it from recommended screenshots.

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
   - Before launching a temporary Unity instance, run an environment preflight. Detect whether the current assistant process is elevated/administrator, whether a target-project Unity instance is already open, whether the temporary copy has stale `Temp/UnityLockfile`, and whether the requested Unity executable/version matches `ProjectSettings/ProjectVersion.txt`.
   - If the assistant process is elevated, record the elevated context in the report. Do not let the run hang behind Unity's administrator-risk dialog.
   - If Unity shows the administrator-risk modal (`Unity is running as administrator` / `I wish to continue at my own risk`), automatically click `I wish to continue at my own risk` as the default workflow behavior. Record `admin_privilege_modal_detected: true`, `admin_privilege_modal_action: auto_clicked_continue_at_own_risk`, the matching Unity process id, and the click time in the report. Do not stop or ask for confirmation for this specific modal.
   - The launcher must actively poll for this modal immediately after starting Unity. Match either the window title `Unity is running as administrator` or dialog text containing `Administrator privileges`, then click the child button whose text is exactly `I wish to continue at my own risk`. Prefer Win32 `BM_CLICK` or an equivalent control-level click over mouse coordinates. If the first click does not dismiss the modal, retry briefly and then classify the failure as `unity_launch/admin_privilege_modal_auto_click_failed`.
   - In current-instance takeover mode, detect whether the target project root is already open in Unity. Use it only after the exact confirmation above. The runner may open `GameMain.unity`, enter/exit Play Mode, invoke UI events, and change game state. The user should not operate Unity until the action completes.
   - If the target project is not open and the user chose current-instance takeover mode, open the original project only after confirmation; otherwise ask whether to switch to temporary-copy mode.
   - In MCP mode, use callable Unity MCP tools to open or attach to the target Unity project, enter Play Mode when required, invoke project/UI actions, query scene/UI state, and capture screenshots through Unity-side APIs. Do not use OS mouse/keyboard control, desktop screenshots, or foreground-only GameView pixel capture as the normal MCP path. If MCP can only control the currently open Unity Editor, state that this mode does not take over the user's mouse/desktop but may still change Unity Play Mode, scene, or runtime state.
   - Default new-instance Game View resolution is `720x1280` for portrait games and `1280x720` for landscape games.
   - Determine portrait vs landscape from project settings, build orientation, common mobile UI/layout evidence, or existing screenshot dimensions. If orientation cannot be determined, default to portrait `720x1280` and report the assumption.
   - If the user specified a desired screenshot resolution in YAML or conversation, use that resolution instead of the default.

3. Temporary-copy diagnostic loop:
   - If temporary-copy mode fails, do not silently stop at the symptom and do not silently switch to current-instance screenshots.
   - Continue far enough to classify the failed stage:
     - `copy_integrity`: copied project missing `Assets`, `Packages`, `ProjectSettings`, `ProjectVersion.txt`, local packages, generated code, or required symlink/junction target.
     - `unity_launch`: Unity executable not found, wrong Unity version, licensing/login issue, administrator-risk modal auto-click failed, project path rejected, stale project lock, or process exits before import.
     - `mcp_connect`: Codex MCP plugin missing, Unity MCP plugin missing, callable MCP tools unavailable, Unity MCP connection rejected, target project mismatch, or MCP commands time out.
     - `import_compile`: package restore/import error, compile error, assembly definition issue, generated code missing, SDK initialization crash, or scene dependency missing.
     - `play_mode`: cannot open `GameMain.unity`, cannot enter Play Mode, Play Mode exits, or startup exception prevents UI.
     - `ui_flow`: top view/root canvas cannot be found, start button cannot be identified, a real UI action does not change state, the flow is only reachable through synthetic hooks, or reachable flow is too shallow.
     - `capture_hook`: Camera/RenderTexture/ScreenCapture/project hook cannot capture a valid frame, captures only the world/main camera without UI, or returns stale/duplicate pixels after UI state changes.
     - `copy_back`: screenshots were captured but not written under `<package-dir>/截图/自动截图/`.
     - `quality_gate`: screenshots are blank, pure-color, wrong project, wrong window, duplicate, loading-only, or low-information.
   - For the failed stage, record concrete evidence: Unity log path, last relevant error/warning lines, runner status, scene path, capture method, output path, and file hashes when applicable.
   - If the root cause can be repaired inside the temporary copy without touching the original project, make one minimal repair and rerun that stage. Examples: recreate missing output directory, adjust runner path, wait for compile completion, or copy an omitted local package that is still inside the original project root.
   - If the root cause would require changing the original project, logging into Unity, resolving package licensing, or hand-driving the game, stop automatic screenshotting and offer current-instance or manual screenshot fallback with the diagnostic report attached.

4. Capture mechanism:
   - Automatic screenshotting must use Unity-internal automation, such as a temporary Editor runner, a current-instance Editor runner, a project-provided screenshot hook, Camera/RenderTexture capture, runtime `ScreenCapture`, or verified Unity MCP tools.
   - Do not control the OS mouse or keyboard to click through the game for final automatic screenshots.
   - Do not use desktop/window screenshots as final automatic screenshot sources.
   - Preferred capture path: run a PlayMode coroutine and call runtime `ScreenCapture.CaptureScreenshotAsTexture()` only after `WaitForEndOfFrame`, then save the resulting texture. A call from an Editor update before end-of-frame is not valid evidence if it logs `CaptureScreenshotAsTexture() failed to generate texture`.
   - RenderTexture fallback must render all enabled cameras that participate in the current view, not only `Camera.main`. Discover active cameras, include UI cameras such as `UICamera`, sort by `Camera.depth`, render into the same target, and record the camera names/depths in the report. A capture that only renders the skybox/world layer while UI is visible in the game state must be rejected as `capture_hook/ui_camera_missing`.
   - For Screen Space Overlay canvases, use a capture method that includes overlay UI, or force a validated in-copy fallback that renders the Canvas correctly. Do not mark a camera-only image as pass when overlay UI is missing.
   - Treat `GameView ReadScreenPixel`, Win32 window capture, screen-region cropping, and any method that depends on Unity being the foreground focused window as foreground-only fallback. It is not valid for temporary-copy/background-capable mode.
   - In current-instance takeover mode, first attempt focus-independent Unity capture: project hook, Camera/RenderTexture, runtime `ScreenCapture`, or an Editor runner that captures from Unity render targets.
   - If only `GameView ReadScreenPixel` or foreground pixels are available, pause and ask for a separate confirmation such as `我确认本轮自动截图允许前台独占，期间不切换焦点、不操作其他应用。` Mark the report as foreground-only. If the user wants to keep using the computer, do not use this fallback.
   - If Unity-internal capture cannot be established without focus dependency, stop automatic screenshotting and ask the user to place manual screenshots in `<package-dir>/截图/`.
   - Never reuse screenshots from earlier failed rounds, report backup directories, unrelated packages, or outside `<package-dir>/截图/自动截图/` as a substitute for a failed capture round.

5. Runtime observation:
   - Open `GameMain.unity` in the chosen Unity Editor instance or a configured local build.
   - Capture the startup/entry screen after the game becomes visually stable.
   - Run the state probe and store a baseline UI state before the first capture.
   - Prefer a real-play interaction path. Discover visible `Button`, `Selectable`, text labels, tabs, and named UI objects, then invoke the same runtime event path a user would trigger, such as `Button.onClick.Invoke()` or an EventSystem pointer/click event on the target UI object. Record the visible label/object path and the resulting top view/state.
   - For every planned screenshot after the startup screen, use this loop: probe pre-state -> resolve target button by transform path first, label second -> invoke action -> wait for stable state -> probe post-state -> verify expected view/text/state -> capture -> verify hash/fingerprint. If any check fails, skip the screenshot and record why.
   - Do not continue a broken branch as if it succeeded. Example: if `RankButton` is missing or `UIRankView` does not open, skip rank screenshots and return to the next independent scenario when possible.
   - Click likely start/gameplay buttons first through Unity UI events. Do not use OS mouse movement/clicks.
   - Systematically explore visible second-level screens and switchable views. If a screen shows obvious tabs, toggles, menu buttons, list/detail entries, chest/reward entries, ranking/card/growth entries, pause/return controls, or other clearly clickable non-sensitive functions, try to open each distinct function at least once and capture the resulting interface.
   - For every visible clickable entry that is not captured, record why it was skipped, such as duplicate screen, unsafe entry, external link, payment/advertising/privacy risk, blocked runtime state, or automation could not reach it.
   - After each action, wait for a stable state, capture a candidate screenshot, and record the action that led there.
   - Use `UIManager.ShowView`, model mutation, direct scene object activation, debug menus, or injected settlement state only as a fallback when the real UI path cannot reach the target within the exploration budget. Mark these records with `interaction_method: synthetic_view_hook` or `state_injection: debug_state_injected` in the manifest and report. Synthetic records are useful candidate evidence, but they must not be described as naturally played screenshots.
   - Avoid repeating identical states by comparing scene name, visible UI text, and screenshot hash when available.
   - If battle has both victory and failure outcomes, attempt to capture both victory settlement and failure settlement. Use debug/test hooks when project evidence shows safe local hooks, or explore normal gameplay paths when reliable. If only one outcome is reachable automatically, report the missing outcome and recommend manual supplementation.

6. Candidate selection:
   - Prefer screenshots that show real game function instead of splash/loading-only states.
   - Prefer coverage of distinct clickable functions over many similar screenshots from one screen.
   - Keep screenshots for obvious second-level or switched interfaces when the entry is visible in another screenshot.
   - Keep candidates that show startup/entry, start button, battle/gameplay, state changes, victory/failure/settlement, pause/exit, and whole-app exit or back-to-entry flow.
   - If multiple screenshots are similar, keep the clearest and most function-rich one.
   - Reject pure-color, blank, loading-only, non-Unity, wrong-project, wrong-window, focus-lost, stale-frame, duplicate, or low-information screenshots. Record rejected screenshots and reasons in the report.
   - Reject semantically mislabeled screenshots. If the expected postcondition says `UIRankView`, `UILoadoutView`, `BattlePauseView`, or settlement state, but the probe shows another view/state, the screenshot must be skipped or renamed to the actual state before it can be considered.
   - Screenshots marked `duplicate`, `duplicate_or_low_value`, `wrong_window`, `focus_lost`, `blank`, `pure_color`, `loading_only`, or `low_information` must not be embedded in the final manual unless the user explicitly places them in `截图/` as manual evidence and confirms the risk.
   - Prefer screenshots reached through `natural_ui_event` over `synthetic_view_hook` when both exist for the same function. If a final screenshot requires synthetic hooks or debug state injection, report that clearly and pause when it affects legal-review confidence.
   - Before final selection, compare hashes and basic dimensions. If two files with different function names have the same hash, keep at most one and report the duplicate group.
   - If the manifest says the top UI view changed but the screenshot hash did not change, reject the later screenshot and classify it as `stale_frame`.

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

Images saved under `<package-dir>/报告/`, including `自动截图原始备份` folders, are diagnostic artifacts only. They are not final screenshot inputs. If one of those images is genuinely needed, ask the user to copy or move it into `<package-dir>/截图/` after reviewing it.

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
- execution mode: temporary-copy mode, current-instance takeover mode, or Codex MCP + Unity MCP mode;
- whether the original project or an isolated copy was used;
- launch privilege context, such as standard user or elevated administrator;
- launch method, whether an administrator-risk modal was detected, and whether `I wish to continue at my own risk` was auto-clicked;
- MCP mode prerequisites and connection status when applicable;
- current-instance takeover confirmation text when applicable;
- for temporary-copy failures, the failed stage, root cause or strongest hypothesis, log evidence, attempted repair, and recommended next action;
- Game View resolution used, and whether it came from the user-opened instance, YAML/conversation, or default orientation logic;
- capture method, such as Editor runner, project hook, GameView, Camera, RenderTexture, or ScreenCapture;
- cameras rendered when RenderTexture fallback is used, including camera names and depth values;
- whether the capture method is focus-independent or foreground-only;
- whether the selected mode may affect the current Unity Editor state;
- interaction method, such as natural UI button event, EventSystem click, project hook, synthetic `UIManager.ShowView`, or debug state injection;
- actions attempted;
- state probe snapshots before and after actions;
- target views/text expected and whether each postcondition passed;
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
  "expected_view": "UIBattleView",
  "expected_text": "3:00",
  "pre_state_fingerprint": "...",
  "post_state_fingerprint": "...",
  "postcondition_passed": true,
  "interaction_method": "natural_ui_event",
  "state_injection": "",
  "capture_method": "WaitForEndOfFrame ScreenCapture",
  "cameras_rendered": [],
  "focus_dependency": "focus_independent",
  "quality": "pass",
  "reason": "target view and screenshot hash changed",
  "sha256": "..."
}
```

Manifest records for rejected images must keep the file path, hash when available, `quality`, and rejection reason. A manifest with `quality` values other than `pass` is acceptable only if those records are clearly rejected and excluded from the final screenshot list.

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
- Temporary-copy mode must not rely on manual dismissal of Unity startup dialogs. The Unity administrator-risk dialog is the one exception: automatically click `I wish to continue at my own risk` and report it. License, missing module, project lock, and unsaved recovery prompts remain launch diagnostics, not hidden waits.
- Current-instance takeover mode may affect the user's Unity state; stop if unsaved-work prompts or project mismatch are detected.
- Do not claim that current-instance mode is safe for the user to operate other apps unless the capture method is focus-independent. Foreground-only fallback requires the user to leave Unity focused for the duration.
- If the project cannot open, cannot enter Play Mode, cannot find `GameMain.unity`, or cannot produce stable screenshots, stop automatic screenshotting and offer direct generation from existing screenshots.
- Automatic screenshotting is an assistant step, not a guarantee of complete legal-review compliance.
