# agent-project-base

可复制的软件开发基座：开发方法原样复用成熟 skill 和工作流，通用内容只在 `.agents/` 维护；明确授权的项目自定义能力单独注明来源和验证状态。

## 范围与来源

第一版覆盖需求澄清、设计、计划、开发、测试验证和合并/PR；不包含 CI/CD 或生产部署自动化。

正式上游 skill 集合为 Superpowers v7.0.2：`22f0b463e7a5e579904dd6211a520321035526f7`，共 15 个 skill。另有用户明确授权的 1 个项目自定义 skill `arc42-architecture`，当前共 16 个项目 skill 目录。Skills CLI 生成的 `skills-lock.json` 仅记录 15 个第三方 skill 的来源、commit 和内容校验值；不手写锁文件，也不为自定义 skill 伪造上游锁记录。

原版流程说明：[上游 README](.agents/upstream/superpowers/README.md)。
固定版本上游：https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7
许可证：[MIT 原文](.agents/upstream/superpowers/LICENSE)。上游 README 的插件安装方式和相对链接对应其完整仓库，不能直接当作本模板的安装指令；本模板未引入那些全局插件或 hooks。

arc42 toolkit 的评估试用候选固定为 `97492c34cdbdb87dc6ea97ae6edbd9673167aed5`。官方格式检查为 0/14 通过：顶层 `version` 非标准，第 5 章另有 YAML 解析错误。用户已决定暂停引入及运行试用，不修改上游原文。lint 依赖 skill 目录之外的根目录资源，没有中文语言包，且只检查部分引用约定，不能替代架构内容评审。普通 brainstorming 设计文档不等于 arc42；本次未引入 Spec Kit。

arc42 官方模板（Release `2026.10.19`，简体中文带写作说明的 Markdown 版，CC BY-SA 4.0）作为文档资产原样收录在 [docs/arc42-template](docs/arc42-template/README.md)，不是 skill，不改变上述 toolkit 暂停决定。来源、SHA-256、署名与许可证见该目录说明。

## 项目自定义 arc42 skill

[arc42-architecture](.agents/skills/arc42-architecture/SKILL.md) 根据用户提供的要求编写，不是 arc42 官方或第三方 toolkit 发布的 skill。权威来源在 `.agents/skills/`，Claude Code/Qoder 通过项目内相对软链接引用；不修改全局配置，不修改上游 Superpowers 原文。这项明确授权不恢复暂停的 toolkit，也不代表普遍允许自写替代 skill。

支持 `code`（从代码逆向现状）、`requirements`（按需求设计目标）和双输入对照三种用法；`code`、`requirements` 是模式标签，不是新增 CLI 命令。阶段流程、十二章结构、图形与一致性要求以 SKILL.md 为准，本文件不重复。

验证边界：本地格式与链接测试通过；只读子代理做过 Phase 1–3 的基线与带 skill 对比，结果未完全通过，正式十二章生成、跨章一致性、Mermaid 渲染和 IDE 新会话发现/加载均未验证。结构测试通过不等于行为通过。

## 在新项目中使用

复制或克隆模板，保留隐藏目录、相对软链接和锁文件；不要只复制可见文件。skill 内容随项目提供，不依赖作者本机的全局安装。克隆只能取得已提交内容；`feat/superpowers-base` 的提交尚未推送，远端无法取得完整模板。

在业务项目中补充自己的技术栈、测试命令和验收条件。本基座不预设所有项目使用同一种测试工具。

用目标工具的原生 skill 机制加载项目级 `using-superpowers`。需求讨论使用 `brainstorming`，执行计划、TDD、调试、评审与验证以上游说明为准；这些是能力索引，不是另造的串行调度器。没有原生加载条件时先报告缺口，不自行新增适配。

## 工具接入状态

| 工具 | 项目 skill 来源 | 当前证据状态 |
| --- | --- | --- |
| Qoder IDE | `.qoder/skills/` 引用 `.agents/skills/` | 16 个相对链接通过；本会话已显式加载上游项目入口；自定义 skill 的原生加载/新会话未验证 |
| Claude Code | `.claude/skills/` 引用 `.agents/skills/`；`CLAUDE.md` 导入入口 | 16 个相对链接通过；未运行会话验证 |
| Cursor | `.agents/skills/` | 项目级文件已安装；未运行 IDE 验证 |
| Codex | `.agents/skills/` | 项目级文件已安装；未运行会话验证 |
| GitHub Copilot | `.agents/skills/` | 项目级文件已安装；未运行会话验证 |
| OpenCode | `.agents/skills/` | 1.19.4 原生列表可发现项目 skill；默认启动仍受全局同名覆盖影响（根因已定位）；单进程隔离会话已验证 5 个 skill 的实际加载及 TDD/调试练习；自定义 skill 未验证 |

能读文件、能发现 skill、能自动启动入口和支持 hooks/子代理是不同能力。CLI 的安装路径与文件验证不能替代目标 IDE 实测；已有全局 skill 的触发结果也不能证明项目级来源生效。目标环境不支持软链接时停止并确认，不自动改成多份复制。

## 本地验证与更新

安装管理要求 Node.js >= 22.20.0，模板测试要求 Python >= 3.11；不代表所有上游配套脚本只需要这两种运行时。

```bash
python3 -m unittest discover -s tests -v
DISABLE_TELEMETRY=1 npx --yes skills@1.9.0 list --json
git diff --check
```

第三方引入前的官方格式检查及固定参考校验器命令见[实施计划 Task 0](docs/superpowers/plans/2026-11-20-agent-project-base-implementation.md)。参考校验器只在不入库的本地检查目录中临时运行，不是正式模板运行依赖；格式通过不等于安全认证。

更新属于显式维护操作：先审核新版本差异和标准，再固定新 commit，通过 Skills CLI 更新项目内容与锁文件，重跑资源、结构与接入验证。本次不自动追随 main，不使用实验性恢复/同步命令作为首次使用前提。

## 验证证据与限制

2026-11-20 skill 改名及说明同步后的本次本地验证：

| 命令（项目根目录） | 来源 | 实际输出 | 适用范围与限制 |
| --- | --- | --- | --- |
| `python3 -m unittest discover -s tests -v` | 本次执行 | `Ran 7 tests`、`OK` | 当前格式、锁记录、32 条相对链接、模板完整性；不验证架构生成行为 |
| `git diff --check` | 本次执行 | 退出 0，无空白错误诊断 | 仅已跟踪文件的差异，不覆盖未跟踪文件 |
| `git diff --no-index --check /dev/null <文件>` | 本次执行，分别检查三个文件 | 均退出 1，无空白错误诊断；`--no-index` 与空文件有差异时返回 1 | 补查未跟踪的 `AGENTS.md`、`.agents/skills/arc42-architecture/SKILL.md`、`tests/test_template_integrity.py`；未声称覆盖全部未跟踪资源 |

以下为初始安装阶段的历史证据：

2026-11-20 安装环境：Node.js v24.11.1、npm 11.6.2、Python 3.11.4、Skills CLI 1.9.0；经用户选择，在 `feat/superpowers-base` 分支执行。

- Superpowers 的 15 个正式 skill 在安装后再次通过官方格式检查；安装目录及来源 README/LICENSE 与固定上游全量比对，无差异。CLI 列表为 15 项、全部 `project`/`tracked`。
- 核心安装、来源文档和平台映射均记录了预期失败及随后通过的 RED → GREEN 输出。初始安装阶段的历史全量模板测试为 4/4 通过，验证锁文件、入口资料、30 个项目内相对链接与无自定义工作流；这不是新增自定义 skill 后的当前测试数量。
- Qoder Remote CLI 版本为 1.106.3；本会话的 Skill 工具返回项目 `.qoder/skills/using-superpowers` 和 `.qoder/skills/systematic-debugging`。这是显式加载证据，不代表新会话自动触发已通过。
- OpenCode 1.19.4（`--pure --agent plan`）新会话 `ses_e08fe16e4ffeBhYQvKH866rCVw` 中，`using-superpowers` 实际加载自本项目，`brainstorming` 却加载自用户级 `$HOME/.agents/skills/brainstorming`，两份内容不同。已停止后续练习；未修改全局配置、原版 skill 或添加适配。
- OpenCode 来源冲突根因已定位（固定 commit `148842ef7cb1bc34192b3fff57d0f9721ab9c801`）：`discoverSkills` 同时收集全局与项目目录的同名 skill，`loadSkills` 以无界并发解析后按名称覆盖共享表，最终来源取决于完成顺序。用单进程环境变量 `OPENCODE_DISABLE_EXTERNAL_SKILLS=true` 配合 `skills.paths` 重新登记项目路径后，新会话实际加载 5 个本项目 skill，并在隔离目录完成 TDD 与边界故障调试，练习测试 5/5 通过。该隔离只作用于单次命令，默认启动的同名覆盖仍存在。
- OpenCode 的普通管道发现输出曾被截断；在现有 `script` 伪终端中重跑后获得完整列表。这只是诊断输出采集方式，不是模板新增运行时适配，也不解决上述加载冲突。
- 第三方 arc42 toolkit 行为试用仍暂停，未创建或运行对应测试，不把暂停项计为通过。自定义 arc42 skill 的首版对比及双模式复测另见上文，不等于 toolkit 试用或正式文档生成通过。其余工具新会话、TDD/调试练习及图形渲染未验证。
- 克隆冒烟验证未执行。本地检查缓存被 `.gitignore` 忽略，不属于正式分发。

未经明确授权，不执行 Git 提交、推送或创建 PR。不修改全局配置，不清理用户工作树。发现没有成熟接入方案的缺口时先确认，不自行编写适配。
