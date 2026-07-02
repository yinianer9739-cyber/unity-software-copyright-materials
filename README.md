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
    application-form-field-mapping.md
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

## 从 latest zip 安装

从 GitHub Releases 下载 `unity-software-copyright-materials-latest.zip` 后，解压得到 `unity-software-copyright-materials/` 目录，并放到：

```text
%USERPROFILE%\.codex\skills\unity-software-copyright-materials
```

发布 zip 应包含 `SKILL.md`、`README.md`、`LICENSE`、`RELEASE_NOTES.md`、`agents/`、`assets/`、`references/` 和 `scripts/`，不需要包含 `.git/` 或本地生成的输出材料。

## 资料包工作流

1. 选择一个软著资料包目录。
2. Codex 检查线上 `VERSION`，如有新版则自动更新本地 skill，写入断点并提示重启。
3. Codex 创建或修复资料包目录结构；已有 YAML 不会被覆盖。
4. 用户填写 `软著基础信息.zh.yaml`，并把功能截图放入 `截图/`。
5. Codex 读取 YAML 中的 Unity 项目根目录，分析项目源码。
6. Codex 扫描 `截图/`，并审核固定风险项。
7. Codex 基于模板生成三份正式材料到 `输出/`。
8. Codex 生成辅助报告到 `报告/`，并在回答中给出可点击文件链接。

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

## 固定审核要求

生成材料前必须审核以下事项。不满足时应提醒用户可能过不了审，并建议更新材料：

- 代码不显示行号，源代码节选不少于 3200 行。
- 登录界面必须包含健康游戏公告或等效提示。
- 如果有账号、密码、注册、开始游戏入口，需要在说明书中对应说明。
- 建议提供退出战斗和退出整个 APP 的截图与说明来源。
- 截图中出现但未说明的按钮或入口，建议用户补充说明或删除该视觉元素。
- 登记申请表必须按 `references/application-form-field-mapping.md` 从 `软著基础信息.zh.yaml` 写入字段；YAML 不只是说明书素材。

## 常用脚本

以下脚本需要 Python 3。Windows 上如果 `python3` 不可用，请替换为实际可用的 Python 3 路径。

检查线上版本并按需自动更新：

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

## 重要规则

- 不默认假设 Unity 业务代码全部是 Lua。
- 优先使用真实项目源码作为代码节选来源。
- 排除 `.meta`、`Library`、`Temp`、构建输出、压缩混淆文件和第三方库。
- 代码不显示行号，源代码节选不少于 3200 行。
- 登录截图应包含健康游戏公告或等效提示。
- 如果截图里出现按钮或入口，说明书中应有对应说明。
- 说明书、申请表、代码节选中的软件名称和版本应保持一致。
- 最终 `.docx` 文件应移除批注和修订痕迹。

## 许可证

MIT License。详见 `LICENSE`。
