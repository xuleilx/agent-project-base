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

当前名称为 `arc42-architecture`（原名 `arc42-architecture-recovery`，旧名称不再保留入口），支持两种输入模式及双输入对照；`code`、`requirements` 是模式标签，不是新增 CLI 命令。

| 输入与目的 | 文档视角与依据 | 调用示例 |
| --- | --- | --- |
| `code`：从已有代码逆向 | 现状；已读源码、配置、入口和实际验证记录 | “使用 arc42-architecture，按当前代码分析现状架构，先到 Phase 3 给事实清单。” |
| `requirements`：从需求/PRD 设计，无代码也可开始 | 目标；需求 ID、约束、质量场景与带状态的设计方案 | “使用 arc42-architecture，按以下需求设计目标架构。我还没有代码，先列需求、缺口和备选方案，等我确认。” |
| 双输入：现状与目标对照 | 分列现状、目标、差异及迁移/验证待办 | “代码是现状，PRD 是目标；分别记录现状、目标和差异，不把目标组件写成已实现。” |

用目标 IDE 的原生 skill 机制调用。宿主未发现新 skill 时先重新加载项目或开启新会话；是否支持 `/arc42-architecture` 取决于宿主，不宣称已验证自动触发。

该 skill 保留六阶段工作流、十二章中文 Markdown、Mermaid/C4 图及一致性审查。代码事实引用真实路径与符号；需求保留或分配稳定 ID，建立 `需求 → 设计/ADR → 构建块/接口/图 → 质量验收` 追踪。先给资料清单，默认在 Phase 3 等待确认；需求模式还须比较方案、确认选定方案与假设。用户明确要求直接给草案时，未确认方案仍标“提议”。需求、已确认设计、已实现和实测结果不能互相替代，独立项目/场景不能自动继承指标或批准状态。

正式文档目标为 `docs/architecture/`。双输入使用同一套十二章，按适用性分“现状”“目标”“差异与迁移待办”，图源用 `asis-*.mmd`、`target-*.mmd` 区分；只有用户现状说明时标“用户报告，实现未核实”。本次仅创建和扩展 skill，没有生成实际项目的十二章架构文档，也未修改应用源码或已有 OpenSpec 规格。

2026-11-20 首版轻量验证记录（代码入口，历史记录）：
- 新增格式/链接测试先失败（缺少 skill 和两条映射），创建后全量 `python3 -m unittest discover -s tests -v` 为 `Ran 7 tests`、`OK`；检查 15 个上游锁记录、32 条项目相对链接、自定义 skill 的单行 frontmatter/命名/字段长度/正文，以及官方模板完整性。此为本地格式/结构检查，不是官方认证。
- 按用户选择各执行一次只读子代理基线/带 skill 对比，限定 Phase 1–3，不产生正式架构文档。基线未先列事实/确认缺口，并在 C4Context 中把目录和锁文件直接画成 Container；带 skill 输出了事实清单并停在 Phase 3，但仍把历史测试数量/通过记录当当前结果，遗漏配套脚本并作出超出证据范围的断言。**单轮行为对比未完全通过。**
- 首版针对偏差收紧了入口清单、负面结论检索范围、本次/历史验证分列及本地部署适用性规则，当时未复测；双模式扩展后的复测见下文。正式十二章生成、跨章节一致性检查、Mermaid 渲染和 IDE 新会话发现/加载均未验证；不能把结构测试通过等同完整行为通过。
- Agent Skills 官网全文两次抓取超时，仅获得官方搜索摘要及已有创建 skill 指南；未运行官方参考校验器。C4 官方容器说明已核对：应用或数据存储才是容器，文件目录在有存储职责证据时可以表示数据存储，但不能自动视为服务。

2026-11-20 双模式扩展复测记录（仍限定 Phase 1–3）：
- 旧版基线缺少无代码需求入口、需求 ID 追踪及方案比较/确认。扩展规则后，首次复测产出了需求清单与两个备选，混合输入也区分了未核实的现状与目标；但混合场景错误继承了另一独立场景的 500ms 指标和方案 ID，代码回归仍遗漏配套脚本。因此不能判为全部通过。
- 增加资料范围隔离和固定入口表后，最后定向复测读取了 `brainstorming/scripts/helper.js`，识别 `nextReconnectDelay`、`connect`、`sendEvent`，并核对当前 7 个测试方法、标注未运行。这仅证明该已知入口的取证改善，不代表全仓库入口已覆盖。
- 最后纯需求场景未产出要求的需求表和两个方案，混合场景也未产出完整差异表；只读 Search 子代理返回了规范/仓库调查，而非所需场景产物。其自评“通过”与实际输出不符，不能采信。**双模式规则已写入，但执行型行为验证尚未通过；现有只读测试方法不足以完成验收。**
- 方案批准后的状态流转、完整十二章生成、跨章一致性、图形渲染及 IDE 原生发现/加载仍未验证。最终文本的本地结构测试与差异检查另见下文；结构通过不能消除这些行为限制。

## 在新项目中使用

复制或克隆模板，保留隐藏目录、相对软链接和锁文件；不要只复制可见文件。skill 内容随项目提供，不依赖作者本机的全局安装。克隆只能取得已提交内容；本次实施变更尚未提交，不能直接从远端克隆得到完整模板。

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
| OpenCode | `.agents/skills/` | 历史记录：1.19.4 原生列表发现 15 个上游项，新会话实际加载发生全局来源混用，流程验证阻塞；新增自定义 skill 未验证 |

能读文件、能发现 skill、能自动启动入口和支持 hooks/子代理是不同能力。CLI 的安装路径与文件验证不能替代目标 IDE 实测；已有全局 skill 的触发结果也不能证明项目级来源生效。目标环境不支持软链接时停止并确认，不自动改成多份复制。

## 本地验证与更新

安装管理要求 Node.js >= 22.20.0，模板测试要求 Python >= 3.11；不代表所有上游配套脚本只需要这两种运行时。

```bash
python3 -m unittest discover -s tests -v
DISABLE_TELEMETRY=1 npx --yes skills@1.9.0 list --json
git diff --check
```

第三方引入前的官方格式检查及固定参考校验器命令见[实施计划 Task 0](docs/superpowers/plans/2026-11-20-agent-project-base-implementation.md)。参考校验器仅在 `.validation/` 中隔离运行，不是正式模板运行依赖；格式通过不等于安全认证。

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
- OpenCode 1.19.4（`--pure --agent plan`）新会话 `ses_e08fe16e4ffeBhYQvKH866rCVw` 中，`using-superpowers` 实际加载自本项目，`brainstorming` 却加载自用户级 `$HOME/.agents/skills/brainstorming`，两份内容不同。已停止后续练习；未修改全局配置、原版 skill 或添加适配。发现列表不能覆盖实际加载冲突，具体根因尚未定位。
- OpenCode 的普通管道发现输出曾被截断；在现有 `script` 伪终端中重跑后获得完整列表。这只是诊断输出采集方式，不是模板新增运行时适配，也不解决上述加载冲突。
- 第三方 arc42 toolkit 行为试用仍暂停，未创建或运行对应测试，不把暂停项计为通过。自定义 arc42 skill 的首版对比及双模式复测另见上文，不等于 toolkit 试用或正式文档生成通过。其余工具新会话、TDD/调试练习及图形渲染未验证。
- 克隆冒烟验证未执行，需用户先另行授权并完成模板提交。`.validation/` 为被忽略的检查缓存，不属于正式分发。

未经明确授权，不执行 Git 提交、推送或创建 PR。不修改全局配置，不清理用户工作树。发现没有成熟接入方案的缺口时先确认，不自行编写适配。
