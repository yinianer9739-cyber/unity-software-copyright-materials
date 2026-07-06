# Unity Software Copyright Materials Skill

一个用于辅助生成 Unity 游戏软件著作权登记材料的 Codex skill。

该 skill 面向中国软件著作权登记场景，围绕 Unity 游戏项目、用户基础信息、功能截图和项目源码，辅助生成或整理：

- 游戏软件说明书
- 源代码节选
- 计算机软件著作权登记申请表
- 项目分析报告
- 截图清单
- 输出验证报告

> 注意：本项目用于材料整理与生成辅助，不构成法律意见。正式提交前请结合登记平台要求、代理机构意见或法务意见复核。

## 适用场景

适合在以下情况下使用：

- Unity 游戏项目需要准备软著材料
- 项目包含 C#、Lua、ToLua、热更新或混合业务代码
- 需要从 Unity 工程中筛选业务源码作为源代码节选
- 需要根据游戏截图生成软件说明书功能章节
- 需要保持说明书、申请表、代码节选的软件名称和版本一致

## 目录结构

```text
unity-software-copyright-materials/
  SKILL.md
  VERSION
  agents/
    openai.yaml
  assets/
    templates/
      软著基础信息.zh.yaml
      Unity游戏软著基础信息填写表模板.xlsx
      游戏软件说明书模板.docx
      源代码节选模板.docx
      计算机软件著作权登记申请表模板.doc
  references/
    workflow.md
    auto-screenshot-rules.md
    auto-fill-rules.md
    application-form-field-mapping.md
    formal-output-format-rules.md
    unity-project-analysis.md
    screenshot-rules.md
    manual-and-application-rules.md
    code-excerpt-rules.md
    validation-rules.md
  scripts/
    check_version_and_update.py
    create_materials_package.py
    create_input_form.py
    parse_input_form.py
    analyze_unity_project.py
    scan_screenshots.py
    verify_outputs.py
```

## 安装

将整个目录复制到 Codex skills 目录：

```text
%USERPROFILE%\.codex\skills\unity-software-copyright-materials
```

复制后重启 Codex，使 skill 被重新发现。

## 从 Release zip 安装

从 GitHub Releases 下载对应版本包，例如 `unity-software-copyright-materials-v0.6.0.zip`，解压得到 `unity-software-copyright-materials/` 目录，并放到：

```text
%USERPROFILE%\.codex\skills\unity-software-copyright-materials
```

发布 zip 应包含 `SKILL.md`、`VERSION`、`README.md`、`LICENSE`、`RELEASE_NOTES.md`、`agents/`、`assets/`、`references/` 和 `scripts/`，不需要包含 `.git/`、`release/` 或本地生成的输出材料。

## 资料包工作流

1. 选择一个软著资料包目录。
2. 只有从 `软著`、`生成软著`、`启动软著技能` 这类第一轮入口开始新流程时，Codex 才检查线上 `VERSION`；如果是 `已填好`、`继续`、自动截图、MCP 截图、自动补全、直接生成或指定已有资料包目录跑后续流程，则不做版本检查。
3. Codex 创建或修复资料包目录结构；已有 YAML 不会被覆盖。
4. 用户填写 `软著基础信息.zh.yaml`，并把功能截图放入 `截图/`。
5. 用户确认 YAML 填完后，Codex 提供三个选择：直接生成、智能运行游戏生成候选截图后再生成，或自动补充技术特点/开发目的/主要功能后再生成。
6. 如选择自动截图，Codex 会要求用户选择“临时工程副本自动截图”“接管当前 Unity 实例自动截图”或“Codex MCP + Unity MCP 插件自动截图”。默认推荐临时副本模式；当前实例模式必须先保存工作并明确确认；MCP 模式必须确认 Codex MCP 插件和 Unity 引擎 MCP 插件都已安装并可用。
7. 临时工程副本截图失败时，Codex 必须输出失败阶段、日志证据和根因诊断；如果 Unity 启动出现管理员风险弹窗，默认自动点击 `I wish to continue at my own risk` 并写入报告；许可弹窗、项目锁、缺模块、恢复提示等其他启动弹窗仍必须作为启动诊断处理，不能无限等待或盲目点掉。当前实例截图优先使用焦点无关的 Unity 内部截图，焦点依赖的 GameView 像素截图只能作为明确确认的前台独占兜底。
8. Codex 分析项目源码，扫描 `截图/`，并审核固定风险项。
9. Codex 只使用资料包 `截图/` 内的图片，外部图片、`报告/` 备份图、缓存图和旧资料包图片禁止参与最终材料。
10. Codex 复制技能自带 Word 模板后在副本内填充，不重建登记表或修改原始表格结构。登记表字段必须填入原表格目标单元格，不能追加 YAML 汇总段落。
11. Codex 生成源代码节选后统计代码行数，自动写入登记申请表并校验一致性。
12. Codex 校验说明书、源代码节选、登记表的正式格式，拒绝空壳功能说明、模板说明残留、登记表尾部追加信息、Word 锁文件和焦点依赖截图混入。
13. Codex 生成辅助报告到 `报告/`，并在回答中给出可点击文件链接。

资料包结构：

```text
<软著资料包目录>/
  软著基础信息.zh.yaml
  截图/
  输出/
    游戏软件说明书.docx
    源代码节选.docx
    计算机软件著作权登记申请表.docx
  报告/
    生成结果报告.md
    验证报告.md
```

`输出/` 只放正式交付的三份材料。`报告/` 用于存放生成结果、缺失字段、截图风险、源码选择和验证信息。

## 正式材料格式

后续生成资料按正式提交材料模式处理，不把生成过程、审核证明或内部规则写进交付给审核人员看的 Word 正文。

- 游戏软件说明书应接近人工整理案例的版式：标题页、目录、编号章节、功能系统小节、说明段落、截图和图注。
- 说明书第 7 章按最终截图和真实功能生成，例如主界面系统、战斗系统、结算系统、退出系统等，不能只使用截图文件名或空壳“功能说明”。
- 源代码节选只保留正式模块说明、项目相对代码路径和真实代码，不写“代码来自工程源码”“不显示行号”“满足 3200 行”等内部校验话术。
- 源代码节选的行数、来源清单、是否满足规则等证明信息写入 `报告/生成结果报告.md` 和验证报告，不写入源码附件正文。
- 登记申请表必须在模板原表格和选项标记内填值，不能在表格后追加 YAML 汇总或技术预审说明。

## 固定审核要求

生成材料前必须审核以下事项。不满足时应提醒用户可能过不了审，并建议更新材料：

- 代码不显示行号，源代码节选不少于 3200 行。
- 登录/启动/入口界面必须包含健康游戏公告或等效提示。
- 如果有账号、密码、注册、开始游戏入口，需要在说明书中对应说明。
- 建议提供退出战斗和退出整个 APP 的截图与说明来源。
- 截图中出现但未说明的按钮或入口，建议用户补充说明或删除该视觉元素。
- 登记申请表必须按 `references/application-form-field-mapping.md` 从 `软著基础信息.zh.yaml` 写入字段；YAML 不只是说明书素材。
- 法务主体/证件类字段不在 YAML 中填写，不参与技术预审核，由法务在登记表中完成。
- 截图来源必须在资料包 `截图/` 内，不能使用资料包外、`报告/` 备份、缓存、下载、其他项目或旧资料包中的图片。
- 三份正式 Word 文件必须基于技能自带模板复制后填充，不能从空白文档重建，登记表表格结构必须保留。
- 登记申请表必须在原表格目标单元格/选项标记内填值，不能把 YAML 内容追加到表格后面。
- 说明书第 7 章必须使用功能系统名称、说明文字和图号图注，不能只写原始截图文件名或空壳“功能说明”。
- 源代码节选必须按功能模块组织，不能保留模板说明文字或重复泛化功能备注。
- 源代码节选不能写入内部流程或审核证明话术，例如“代码均来自项目工程源码”“不显示行号”“满足 3200 行”“根据资料包自动生成”等。
- 源程序总行数必须在源代码节选生成后自动统计并写入登记申请表，最终校验一致性。

## 智能自动截图

自动截图是可选增强流程，不需要用户在 YAML 里填写额外策略。用户确认 YAML 填完后，可以选择让 Codex 尝试运行 Unity 游戏并自动生成候选截图。

默认策略：

- 从 YAML 的 `项目路径.Unity项目根目录` 读取 Unity 工程。
- 用户可选择临时工程副本模式、当前 Unity 实例接管模式，或 Codex MCP + Unity MCP 插件模式。
- 临时工程副本模式为推荐方式，不会接管当前 Unity，用户可正常操作电脑。
- 临时工程副本模式启动前会检查管理员/elevated 环境、Unity 版本、旧锁文件和启动弹窗。若出现 `Unity is running as administrator` 风险弹窗，默认自动点击 `I wish to continue at my own risk`，并在报告中记录检测到弹窗、匹配的 Unity 进程和点击结果。
- 临时工程副本模式如果失败，必须输出根因诊断报告，包括失败阶段、日志证据、尝试修复和建议下一步。
- 当前 Unity 实例接管模式会影响当前 Unity 状态，必须先保存工作并明确确认；执行期间最好全局不要操控鼠标和电脑。
- 当前 Unity 实例模式优先使用 Camera/RenderTexture、ScreenCapture 或项目截图 Hook 等焦点无关方式；如果只能使用 GameView 前台像素截图，需要另行确认前台独占，且用户切换焦点会导致截图无效。
- MCP 模式必须确认 `确认1：本机已装 Codex MCP 插件` 和 `确认2：Unity 引擎也装了 MCP 插件`，并在当前客户端会话中能调用 Unity MCP 工具。MCP 模式不控制 OS 鼠标或桌面窗口，用户可正常操作电脑；如果连接的是当前 Unity Editor，报告中会说明是否可能影响 Play Mode、场景或运行状态。
- 优先查找并运行 `GameMain.unity`。
- 运行中优先通过真实 Unity UI 事件游玩，例如触发可见按钮的 `onClick` 或 EventSystem 点击；直接调用 `UIManager.ShowView`、修改 model 或注入结算状态只能作为兜底，并会在 manifest/report 中标记为合成钩子或调试注入。
- 截图优先在 PlayMode 的 `WaitForEndOfFrame` 后使用 runtime `ScreenCapture`；RenderTexture 兜底必须按深度渲染所有启用相机，包括 `Main Camera`、`UICamera` 等 UI 相机，不能只截主相机导致 UI 丢失。
- 必须做目标状态校验：每个计划截图先探测当前 UI、按钮和文本，点击后确认目标 View/文本/状态真的到达，截图哈希也发生变化。未到达就跳过并写入报告，不生成“主界面却命名为排行榜/阵容/暂停”的误导文件。
- 优先捕获启动/入口、开始游戏、战斗过程、状态变化、结算、暂停/退出等截图。
- 自动截图保存到 `截图/自动截图/`，不会覆盖用户手动截图。
- 自动截图报告写入 `报告/自动截图报告.md`。
- 三种自动截图方式都不能保证提供最完美的截图列表；正式生成前必须查看自动截图报告，特别是战斗流程、退出战斗、退出 APP、胜利/失败结算和可点击二级界面。
- 自动截图必须来自 Unity 内部截图机制或项目截图 Hook，不使用系统鼠标控制、桌面截图、错窗口截图或旧备份图作为正式截图来源。
- 如果工程地址缺失、Unity 无法运行、找不到入口场景或截图质量不足，会提示用户手动补充截图。

## 自动补全文案

自动补全文案是可选增强流程，不需要用户在 YAML 里填写额外策略。用户确认 YAML 填完后，可以选择让 Codex 在 `技术特点`、`开发目的`、`主要功能` 为空时，根据 Unity 工程、截图清单和已填写 YAML 自动生成建议文本。

规则：

- 需要填写 `项目路径.Unity项目根目录`。
- 只补空字段，不覆盖用户已填写内容。
- `技术特点` 控制在 50-100 字。
- `开发目的` 控制在 50 字以内。
- `主要功能` 控制在 500-1300 字。
- 自动补全文案会记录到 `报告/生成结果报告.md`，正式提交前建议人工复核。

## 常用脚本

以下脚本需要 Python 3。Windows 上如果 `python3` 不可用，请替换为实际可用的 Python 3 路径。

检查线上版本并按需自动更新。该脚本只应在第一轮入口流程中自动调用；后续单独触发的截图、补全、验证或生成阶段不应自动调用：

```powershell
python3 scripts/check_version_and_update.py --package-dir <package-dir> --stage start
```

创建或修复资料包：

```powershell
python3 scripts/create_materials_package.py --package-dir <package-dir>
```

Excel 表单是兼容输入方式，适合需要交给同事或代理机构填写的场景。

生成填写表：

```powershell
python3 scripts/create_input_form.py --out-dir <output-dir>
```

解析填写表：

```powershell
python3 scripts/parse_input_form.py --form <xlsx> --out-dir <output-dir>/00-表单解析
```

分析 Unity 项目：

```powershell
python3 scripts/analyze_unity_project.py --project <Unity project root> --out-dir <package-dir>/报告/01-项目分析
```

扫描截图目录：

```powershell
python3 scripts/scan_screenshots.py --screenshots <package-dir>/截图 --out-dir <package-dir>/报告/02-截图清单
```

校验正式材料：

```powershell
python3 scripts/verify_outputs.py --output-dir <package-dir>/输出 --report <package-dir>/报告/验证报告.md
```

`verify_outputs.py` 会把以下情况判为高风险并停止：登记表后追加 `技术预审填写信息`、说明书存在空壳功能说明、原始截图路径、对象 dump 或报告式正文、源代码节选残留模板说明或内部审核话术、自动截图使用焦点/窗口依赖捕获、自动截图重复哈希、自动截图缺少 UI 相机或使用未说明的合成钩子、Word 锁文件未清理等。

## 重要规则

- 不默认假设 Unity 业务代码全部是 Lua。
- 优先使用真实项目源码作为代码节选来源。
- 排除 `.meta`、`Library`、`Temp`、构建输出、压缩混淆文件和第三方库。
- 代码不显示行号，源代码节选不少于 3200 行。
- 登录/启动/入口截图应包含健康游戏公告或等效提示。
- 如果截图里出现按钮或入口，说明书中应有对应说明。
- 说明书、申请表、代码节选中的软件名称和版本应保持一致。
- 最终材料只能使用资料包 `截图/` 内的图片。
- 最终 Word 文件只能通过复制并填充技能模板生成，不能重建登记表表格。
- 说明书、源代码节选和登记表必须通过正式格式门禁，不能输出生成报告式正文、模板说明残留或登记表尾部追加信息。
- 登记表中的源程序总行数必须与源码分析/代码节选报告一致。
- 最终 `.docx` 文件应移除批注和修订痕迹。

## 许可证

MIT License。详见 `LICENSE`。
