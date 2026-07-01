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
  agents/
    openai.yaml
  assets/
    templates/
      Unity游戏软著基础信息填写表模板.xlsx
      游戏软件说明书模板.docx
      源代码节选模板.docx
      计算机软件著作权登记申请表模板.doc
  references/
    workflow.md
    unity-project-analysis.md
    screenshot-rules.md
    manual-and-application-rules.md
    code-excerpt-rules.md
    validation-rules.md
  scripts/
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

## 从 latest zip 安装

从 GitHub Releases 下载 `unity-software-copyright-materials-latest.zip` 后，解压得到 `unity-software-copyright-materials/` 目录，并放到：

```text
%USERPROFILE%\.codex\skills\unity-software-copyright-materials
```

发布 zip 应包含 `SKILL.md`、`README.md`、`LICENSE`、`RELEASE_NOTES.md`、`agents/`、`assets/`、`references/` 和 `scripts/`，不需要包含 `.git/` 或本地生成的输出材料。

## 基本工作流

1. 选择基础信息输入方式，推荐直接在聊天里粘贴 Markdown/YAML。
2. 确认 Unity 项目根目录、最终功能截图目录和输出目录。
3. 如需文件化交接，再生成或复制基础信息 Excel 表单。
4. 整理聊天输入或解析 Excel 表单。
5. 分析 Unity 项目源码。
6. 扫描功能截图。
7. 基于模板生成说明书、代码节选和申请表。
8. 校验输出并生成验证报告。

## 聊天输入模板

推荐直接向 Codex 粘贴以下字段。暂时不知道的内容可以留空，后续可按设置标红为 `待补充`：

```yaml
软件全称:
软件简称:
版本号: V1.0
著作权人名称:
开发完成日期: YYYY-MM-DD
源程序总行数:

游戏名称:
游戏类型:
游戏概述:
开发目的:
用户分析:
核心玩法:
主要功能:
功能特点:
技术特点:
运行平台:
编程语言:

Unity项目根目录:
功能截图目录:
最终软著材料输出目录:
是否允许缺失字段标红待补充: 是
其他特别要求: 代码不显示行号、源代码节选不少于 3200 行
```

功能截图建议按功能命名，例如 `登录.png`、`主界面.png`、`战斗_血量变化_1.png`、`战斗_胜利结算.png`、`战斗_失败结算.png`、`退出.png`。

## 常用脚本

Excel 表单是备选输入方式，适合需要交给同事或代理机构填写的场景。

生成填写表：

```powershell
python scripts/create_input_form.py --out-dir <output-dir>
```

解析填写表：

```powershell
python scripts/parse_input_form.py --form <xlsx> --out-dir <output-dir>/00-表单解析
```

分析 Unity 项目：

```powershell
python scripts/analyze_unity_project.py --project <Unity project root> --out-dir <output-dir>/01-项目分析
```

扫描截图目录：

```powershell
python scripts/scan_screenshots.py --screenshots <screenshot-dir> --out-dir <output-dir>/02-截图清单
```

校验正式材料：

```powershell
python scripts/verify_outputs.py --output-dir <output-dir>/04-正式材料 --report <output-dir>/验证报告.md
```

## 输出目录建议

```text
<output-dir>/
  00-用户填写表单/
  00-表单解析/
  01-项目分析/
  02-截图清单/
  03-草稿/
  04-正式材料/
  生成报告.md
  验证报告.md
```

## 重要规则

- 不默认假设 Unity 业务代码全部是 Lua。
- 优先使用真实项目源码作为代码节选来源。
- 排除 `.meta`、`Library`、`Temp`、构建输出、压缩混淆文件和第三方库。
- 登录截图应包含健康游戏公告或等效提示。
- 如果截图里出现按钮或入口，说明书中应有对应说明。
- 说明书、申请表、代码节选中的软件名称和版本应保持一致。
- 最终 `.docx` 文件应移除批注和修订痕迹。

## 许可证

MIT License。详见 `LICENSE`。
