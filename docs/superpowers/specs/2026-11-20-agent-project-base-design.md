# 开发项目基座设计

## 设计状态

整体设计及包含 arc42 初步评估结论的书面版本均已获用户确认。用户接受实施计划，并新增“引入之前检查第三方 skill 是否符合标准”的门禁。实施计划保存在 `docs/superpowers/plans/2026-11-20-agent-project-base-implementation.md`。已在 `.validation/preflight/` 隔离核对固定来源并检查全部 29 个 skill：Superpowers 15 个格式通过，arc42 14 个格式失败。用户已选择暂停引入 arc42，其正式引入和 skill 运行试用均不继续；原有评估试用许可不代表成熟性认定或正式集成批准。用户随后要求执行计划，并选择新建 `feat/superpowers-base` 分支。Superpowers 固定版本安装、来源锁与原版资料、薄入口和 CLI 生成的项目级平台映射已完成，4 项模板测试通过。OpenCode 新会话验证出现实际 skill 来源混用，运行接入验收尚未完成；其他未运行项如实记录。未修改全局 IDE 配置，也未执行 Git 提交或推送。

## 目标与范围

提供可复制或克隆到新软件项目的开发模板，将成熟的 skill 和工作流随项目纳入版本管理。通用内容统一维护在 `.agents/`，不依赖模板作者本机的全局安装。

第一版覆盖：需求澄清 → 方案设计 → 实施计划 → 开发 → 测试验证 → 分支合并或 PR 交付。架构设计阶段增加第三方 arc42 toolkit 的评估与试用，未验证前不承诺已具备完整 arc42 自动化。arc42 的部署视图属于架构文档，不扩大第一版为生产部署自动化。

第一版不包含 CI/CD、生产部署、监控、回滚，以及具体语言、框架或业务领域的专用规范。测试命令与验收条件由实际业务项目提供，基座不预设所有项目使用同一种测试工具。

目标工具：Qoder、Claude Code、Cursor、Codex、GitHub Copilot、OpenCode。兼容性记录区分具体产品形态和版本，不能用 CLI 的支持结论替代 IDE 的支持结论。其他主流工具只在已有成熟接入方案且不扩大上述范围的情况下按需补充。

## 复用原则

- skill 和工作流均选用成熟的现成方案，不自行重写或开发新的流程编排。
- 核心选用 `obra/superpowers`；其上游文档已经定义开发工作流，不另行维护一份独立的 `.agents/workflows/` 自定义流程。
- 保留上游 skill 目录中的脚本、参考资料、模板等配套资源，不只复制 `SKILL.md`。
- 保留上游许可证、工作流说明及来源记录；不把本机已有文件直接视为可复现的上游发布版本。
- 使用成熟的 Skills CLI 管理项目级安装和更新，不编写自制安装、同步或工作流调度脚本。
- 如缺少成熟的 skill、工作流或平台接入方案，先说明已核实的缺口并征求用户意见，不用自行定制的内容补齐。
- arc42 已获第三方候选评估与试用许可，仍保持上游原样复用；该例外不授权自行编写 skill、拼接新工作流或同时引入 Spec Kit。
- 第三方 skill 正式安装、建立自动发现映射或运行试用前，先检查官方格式、必要资源和授权风险。不合规时停止受影响步骤并报告，不自行修改上游以通过门禁。

## 目录结构

```text
agent-project-base/
├── README.md
├── AGENTS.md
├── skills-lock.json
├── .agents/
│   ├── skills/
│   │   └── <上游 skill 名称>/
│   │       ├── SKILL.md
│   │       └── <上游配套资源>
│   └── upstream/
│       └── superpowers/
│           ├── LICENSE
│           └── README.md
└── docs/
    └── superpowers/
        ├── specs/
        └── plans/
```

- `README.md`：中文使用说明，说明项目初始化、现成流程的使用方式、更新方法和平台验证状态；不承担工作流编排。
- `AGENTS.md`：通用入口，只说明项目范围、引用上游 skill 与流程、声明用户授权边界；不复制或改写各阶段的上游实现。
- `.agents/skills/`：项目内 skill 的唯一权威来源；如工具需要其他发现路径，适配路径引用这里，不能成为第二份手工维护的源文件。
- `.agents/upstream/superpowers/`：与已固定 skill 版本相对应的上游原版许可证和 README。
- `skills-lock.json`：由安装工具生成和维护的来源、版本及内容校验记录，不手工伪造锁文件或摘要。
- `docs/superpowers/specs/`、`docs/superpowers/plans/`：本基座的设计和实施记录；实际业务项目沿用固定版本上游 skill 的产出物约定，不另建与之冲突的目录规则。

平台专用的薄入口或映射不在初始结构中预设。只有核实存在成熟接入方式后才增加，并记录具体用途。

## 现成开发流程

以下为已核实的上游能力说明，不另定义一套覆盖上游的阶段调度器。

| 开发活动 | 现成 skill |
| --- | --- |
| skill 使用入口 | `using-superpowers` |
| 轻量需求澄清、通用方案讨论 | `brainstorming`，不等同于完整需求工程或 arc42 |
| arc42 分章节架构文档 | `arc42-section-01` 至 `arc42-section-12`，获准评估试用的候选 |
| arc42 文档评审与约定一致性检查 | `arc42-review`、`arc42-lint`，获准评估试用的候选 |
| 工作空间隔离 | `using-git-worktrees` |
| 实施计划 | `writing-plans` |
| 执行计划 | `executing-plans` 或 `subagent-driven-development` |
| 测试驱动开发 | `test-driven-development` |
| 系统化调试 | `systematic-debugging` |
| 发起与接收评审 | `requesting-code-review`、`receiving-code-review` |
| 完成前验证 | `verification-before-completion` |
| 分支交付 | `finishing-a-development-branch` |
| 独立任务并行协作 | `dispatching-parallel-agents`，仅在适用且工具支持时使用 |

执行顺序、触发条件、设计确认、计划执行方式与验证要求，以固定版本的上游 skill 为准。TDD 与评审可能发生在执行过程中，调试是遇到异常时进入的流程，不将所有 skill 强制排成一条固定串行链。

## 需求澄清与 arc42 的责任边界

### 需求澄清

当前仍以 `brainstorming` 进行轻量需求讨论，确认目标、范围、约束和成功标准。独立需求基线、逐条验收条件、需求与测试追踪关系尚未由本基座明确保证。

GitHub Spec Kit 的规格说明、澄清和一致性检查流程是正式需求管理的现成候选，但本次 arc42 试用许可不包含引入 Spec Kit。正式需求管理及多套方法之间的成熟衔接，仍需单独选型和确认。

### arc42 候选与初步评估

- 来源：`MSiccDev/arc42-toolkit`，MIT 许可证，非 arc42 官方项目。
- 本次查询的上游 commit：`97492c34cdbdb87dc6ea97ae6edbd9673167aed5`。作为后续试用的可追溯候选，不代表已经安装或通过验证。
- 上游目录包含 12 个章节 skill，以及 `arc42-review` 和 `arc42-lint`。本次阅读了第 1、4 章 skill、review、lint、上游入口和目录清单，属于初步静态评估，尚未逐章运行。
- 第 1 章要求先询问业务目的、主要功能、质量目标、利益相关者、已有需求来源和文档深度，再生成草稿。质量目标需要具体可测场景及明确的确认责任，不能直接臆造指标。该章的需求概览不能替代详细需求规格。
- 第 4 章检查技术与拆分策略如何支持质量目标、是否违反约束，并标出需要第 9 章 ADR 记录的重大决策。
- review 提供内容和跨章节关系的评审清单，但属于 Agent 辅助评审，不是机器可证明的架构正确性验证。
- lint 仅检查上游 toolkit 的五类标识及引用约定，不代表通过了完整 arc42 质量评审；缺少章节或被跳过的规则不能视为通过。

### 已发现的试用限制

1. 自动 lint 的内置语言包只有 `en`、`de`、`fr`、`it`、`es`、`pt`，没有中文包。不能预先宣称支持中文自动检查，也不自行编写中文适配；试用时确认文档语言和检查方法。
2. 默认图形格式是独立的 C4 PlantUML `.puml` 文件。它是 toolkit 约定，不是 arc42 官方要求；生成文本不等于已经验证图形可渲染。
3. lint 脚本和语言包位于上游仓库根目录的 `scripts/`，不在单个 skill 目录里。仅用安装工具复制 skill 可能缺失这些资源；试用需验证上游完整布局或现成接入方式，不静默改写路径或编写安装脚本。
4. 上游 `AGENTS.md` 中仍有 `.agents/` 整体软链接的描述，但实际目录清单是 `.agents/skills/` 下各 skill 的软链接。不能照抄入口中未核实的目录和自动发现说明。
5. 上游 README 仍将真实项目验证列为后续阶段；本次目录清单未发现专门的自动测试或完整架构示例目录。候选继续标注为“评估试用”，不升级为“成熟已验证”。
6. 与 Superpowers 的原生衔接尚未核实。不得默认通过自定义流程把两套方法串起来，也不让普通设计文档未经确认就替代 arc42 架构文档。

### 引入前标准检查结果

本次以 <https://agentskills.io/specification> 为格式依据，使用官方 `skills-ref` 参考校验器逐项检查全部原版 skill。校验器固定 commit 为 `83021e2be457a9b6679148719c1f6074f0ad975e`，只在隔离目录运行，不作为正式模板依赖。该工具是参考/演示库，不是安全认证工具。

| 候选与固定版本 | 数量 | 官方格式检查 | 当前门禁 |
| --- | --- | --- | --- |
| Superpowers v7.0.2，`22f0b463e7a5e579904dd6211a520321035526f7` | 15 | 引入前及安装后全部通过 | 已安装且与上游资源全量比对无差异；IDE 运行验收未全部通过 |
| arc42 toolkit，`97492c34cdbdb87dc6ea97ae6edbd9673167aed5` | 14 | 全部失败 | 正式引入和 skill 运行试用暂停 |

- 所有 14 个 arc42 skill 原文含非标准顶层 `version`；13 项实际报 `Unexpected fields in frontmatter: version`。按官方格式，版本等扩展信息应放入 `metadata`。
- 第 5 章 `arc42-section-05/SKILL.md` 的 description 未加引号，且含 `toolkit convention: minimum expected output`，实际报 `Invalid YAML in frontmatter: mapping values are not allowed here`。解析失败，因此该项尚未进入字段校验。
- 本次校验汇总为 29 项、14 项失败，命令退出码 1。复现步骤及逐项错误类型记录在实施计划 Task 0，不将格式失败解释为工具未安装或测试跳过。
- 两个候选的固定来源、未修改的 checkout 和 MIT 许可证已核对。Superpowers 的兄弟 skill 脚本引用在全量集合中存在；安装后的完整目录及来源 README/LICENSE 已与固定上游比对，无差异。提交、清理等上游建议不能覆盖本项目授权限制。
- arc42 的仓库根目录 lint 资源和中文包缺失仍是独立接入限制；脚本对空目录或未检测到章节也返回 0，不能把这一结果当作架构校验通过。

用户已选择暂停引入 arc42，保留检查结果，不继续其 skill 运行试用或正式集成。不自行移动 `version` 或修补 YAML，也不自动发布 issue/PR。恢复 arc42、寻找成熟合规替代候选或仅将不合规原文作为参考继续隔离评估，均需另行确认；不能标注当前候选为合规 skill。格式校验不证明安全、行为效果、架构质量或跨 IDE 兼容性。

### 后续试用验收

以下步骤受前述门禁约束，当前未执行。用户处理不合规候选后，在实施计划中安排隔离的练习项目，验证第 1 章先问后写及质量目标确认，再验证方案策略、ADR、架构视图的关联。使用正反例分别检查 review 与 lint 的发现能力，记录跳过项和实际输出；不把缺少章节时的空检查或纯提示词阅读当作成功试用。

运行试用前保留上游配套资源和许可证，并核实安装映射、脚本路径及图形渲染条件。现阶段不创建正式业务架构文档，也不宣称目标 IDE 已验证。

## 平台接入与能力边界

读取文件、自动发现 skill、自动加载启动入口、支持子代理或 hooks，是不同的能力，分别核实和记录。

1. 优先使用目标工具原生的项目级 `.agents/skills/` 发现机制。
2. 不原生支持时，优先采用 Skills CLI 已有的项目级安装映射，或上游官方提供的项目级接入方式。
3. 不默认认为所有工具都会读取根目录 `AGENTS.md`，也不认为同一份 skill 能提供完全相同的 hooks 和子代理行为。
4. 如只能依赖全局插件、需要自定义运行时适配，或官方方案与项目自包含约束冲突，先报告并请求用户确认。
5. 同一环境已有全局 Superpowers 时，检查重复发现和来源冲突；不能将全局安装的触发结果当作项目级安装已生效的证据。
6. 没有实际运行条件的工具标注为“文档核实，未运行验证”或“未核实”，不能宣称已经验证通过。

本次实施证据（2026-11-20）：Claude Code/Qoder 各 15 个项目内相对链接已通过文件验收。Qoder 本会话的 Skill 工具显式加载了项目级入口与调试 skill，但新会话自动触发未验证。OpenCode 1.19.4 的原生发现列表指向项目 15 项；只读新会话实际加载 `using-superpowers` 为项目级、`brainstorming` 为用户级且内容不同，来源冲突导致后续流程验证停止，不能标注 OpenCode 完整接入通过。冲突根因及原生隔离机制未定位；不修改全局配置或添加自制适配。其余工具新会话、TDD/调试练习和克隆验证未完成，详见实施计划与根 README。

## 版本与更新

实施时从上游获取可追溯版本，固定具体 Git commit，使用安装工具生成锁文件，并保证 skill、许可证、上游说明对应同一版本。

skill 及其配套资源随模板一起纳入 Git，使普通复制或克隆即可取得内容。更新使用成熟安装工具进行，检查来源与变更差异，重新运行结构与平台验证后再接受更新，不自动追随上游最新版。

## 授权与异常处理

- 设计批准不等于授权提交、推送或创建 PR。
- skill 内建议提交、合并或清理工作树时，仍服从用户明确授权及宿主工具安全规则。
- 安装或接入失败时，保留已有用户内容并报告原因，不覆盖未知配置，不以自写脚本悄悄替换成熟方案。
- 引入前检查发现格式不合规、必要资源缺失或未经授权的危险行为时，暂停受影响任务并等待用户决定；不得用后续测试覆盖门禁失败。
- 本基座验证的是开发方法能否被发现和执行，不声称单凭 skill 就能保证业务项目质量或全部测试类型的覆盖。

## 验收要求

### 静态与可复现性

- 所有实际安装的第三方 skill 先通过官方 Agent Skills 格式检查；`SKILL.md` 可解析，配套资源完整，引用不指向模板作者的绝对路径。
- `.agents/skills/` 为唯一权威来源；新增映射无断链、无第二份手工维护的 skill。
- 来源、固定 commit、内容校验和许可证可核对；上游说明与 skill 版本一致。
- 普通复制或克隆不依赖作者全局 skill 目录即可取得项目内容。
- 无自定义 skill、自制工作流或未经确认的运行时适配。

### 运行验证

- 在具备运行条件的目标工具中确认项目 skill 的发现列表及实际加载来源。
- 使用隔离的练习项目提出一个小需求，确认先进入需求澄清和设计确认，而非直接修改业务代码。
- 在批准后的练习任务中确认测试驱动开发和完成前验证确实执行，并检查实际命令输出。
- 遇到测试失败时确认先定位根因，不跳过验证宣称完成。
- 检查提交、推送和 PR 行为仍受用户授权约束。
- 记录工具版本、接入方式、验证证据和未验证项；存在未验证工具时不得宣称所有目标工具兼容性均已通过。

## 已核实的上游参考

- Agent Skills 官方格式：<https://agentskills.io/specification>
- 官方参考校验器：<https://github.com/agentskills/agentskills/tree/83021e2be457a9b6679148719c1f6074f0ad975e/skills-ref>
- Superpowers：<https://github.com/obra/superpowers>
- Superpowers 原版 README：<https://raw.githubusercontent.com/obra/superpowers/main/README.md>
- Skills CLI：<https://github.com/vercel-labs/skills>
- Skills CLI 平台安装路径说明：<https://github.com/vercel-labs/skills/blob/main/docs/agents.md>
- arc42 官方模板概览：<https://arc42.org/overview>
- arc42 toolkit 候选：<https://github.com/MSiccDev/arc42-toolkit/tree/97492c34cdbdb87dc6ea97ae6edbd9673167aed5>
- GitHub Spec Kit 候选（尚未采纳）：<https://github.com/github/spec-kit>

上述在线资料会变化。实施时按固定版本重新核对，安装路径列表仅作为接入线索，不能替代目标工具官方文档和运行验证。
