# 开发项目基座实施计划

> **执行者要求：** 使用 `superpowers:executing-plans` 或 `superpowers:subagent-driven-development` 按 Task 执行；工具不支持命名空间时使用对应裸 skill 名称。每个任务有独立验收点。提交、推送、创建 PR 不在本计划的自动授权范围内。

**目标：** 建立项目自包含的 Superpowers 开发基座，并完成第三方 arc42 toolkit 的隔离试用和限制记录。

**架构：** `.agents/skills/` 保存唯一权威 skill 内容，成熟 Skills CLI 负责安装、来源锁定和工具目录映射。根入口仅引用上游方法，不创建新工作流。arc42 保留在隔离试用环境，即使试用通过，也必须另获用户明确批准才能加入正式分发的 skill 集合。

**技术栈：** Git、Skills CLI 1.9.0、Node.js >= 22.20.0、Python >= 3.11、标准库 `unittest`；上游 skill 原版 Markdown 与配套资源。

## 全局约束

- 设计来源：`docs/superpowers/specs/2026-11-20-agent-project-base-design.md`，书面版本已获用户确认。
- 第一版覆盖需求澄清、设计、计划、开发、测试验证和合并/PR 交付；不包含生产部署自动化或 CI/CD。
- skill、工作流、安装映射复用现成方案；不编写自定义 skill、调度器、安装或同步脚本。
- 本计划中的测试只验证模板完整性和第三方工具行为，不是新的 skill 或工作流。
- 不修改全局 skill、IDE 用户配置或 Git 配置；不使用全局安装、全工具安装、复制模式或重命名模式。
- 没有成熟接入方式、资源缺失、软链接不可用时停止对应接入任务并说明缺口，不静默增加自制适配。
- arc42 仅获评估试用许可；不默认引入 Spec Kit，不自行生成中文语言适配，不拼接两套方法的自动化流程。
- 工具未运行验证时明确标注未验证，不用全局安装的触发结果冒充项目级结果。
- 不提交、推送、创建 PR 或清理用户工作树；所有步骤完成后保留变更供用户选择。
- 所有相对路径命令在当前执行工作树根目录运行；不在全局 skill 或插件缓存目录运行。
- 用户新增引入门禁：第三方 skill 在正式安装、自动发现映射或运行试用之前先检查标准；格式不合规、缺少必要资源或存在未获授权的危险行为时停止受影响任务，报告并等待用户决定。
- 当前固定版本、测试数量和工具接入状态以根 `README.md` 为准；本文件保留执行当时的值，不随升级同步改写。

## 已核实的基线与固定版本

- 本仓库已初始化，当前 HEAD 为 `ac1225a`；不是待初始化的空 Git 仓库。已跟踪内容为 README，设计和本计划位于尚未跟踪的 `docs/`；不擅自提交这些文档。
- 本次环境检查：Node.js `v24.11.1`、npm `11.6.2`、Python `3.11.4`。执行前重新检查，不把此记录代替新环境的检查。
- Skills CLI：npm 包 `skills@1.9.0`，对应源码 commit `50894c1d98bc45ca1ab127213e59d6525065b5e7`。核实命令为 `npm view skills@1.9.0 version engines gitHead --json`；实际输出确认版本、Node.js 下限和 commit。
- Superpowers：稳定发布 `v7.0.2`，解引用后的 commit `22f0b463e7a5e579904dd6211a520321035526f7`，不是其 annotated tag 对象 SHA。
- arc42 toolkit：候选 commit `97492c34cdbdb87dc6ea97ae6edbd9673167aed5`。
- 以上版本作为本次安装和试用输入；网络获取失败时报告失败，不自动退回本机旧版或浮动 main。

## 文件边界

正式模板新增：
- `.agents/skills/`：安装工具生成的 15 个 Superpowers skill 及配套资源。
- `skills-lock.json`：安装工具生成；禁止手工编写。
- `.agents/upstream/superpowers/LICENSE`、`.agents/upstream/superpowers/README.md`：固定版本的上游原文。
- `AGENTS.md`：通用薄入口。
- `CLAUDE.md`：使用 Claude Code 官方文件导入机制引用 `AGENTS.md`。
- `.claude/skills/`、`.qoder/skills/`：安装工具生成的项目内相对软链接，不是第二份源文件。
- `.gitignore`：忽略验证缓存和 Python 缓存。
- `tests/__init__.py`、`tests/test_template_integrity.py`：标准库测试。

修改：`README.md`。除更新确认状态外，不改变已确认设计的范围。

隔离内容：`.validation/` 是被 `.gitignore` 忽略的临时检查目录，其中的原版 checkout、测试样本、日志和 Agent 草稿均不分发，也不加入正式 skill 锁文件或 IDE 发现路径。Task 4 暂停后该目录不再保留；`.validation/arc42-toolkit/` 从未获取。需要复现检查时按 Task 0 的命令重建，用完可删。

## Task 0: 第三方 skill 引入前标准检查

**文件：** 按 Task 1 的完整内容提前创建 `.gitignore` 以保护检查缓存；使用 `.validation/preflight/superpowers/`、`.validation/preflight/arc42-toolkit/`、`.validation/preflight/agentskills-ref/` 和 `.validation/preflight/python-deps/`。只更新本计划和设计状态，不改写第三方 skill。

**接口：** 消费前述固定来源；产出逐 skill 的官方格式校验结果、资源和授权风险清单。Task 1 的正式安装与 Task 4 的运行试用均受本门禁约束。

### 检查标准

- 硬性格式以 <https://agentskills.io/specification> 为准：有效 YAML frontmatter，必需 `name` 与 `description`；name 为 1–64 字符、小写字母或数字与连字符、不含连续连字符、与目录同名；description 非空且不超过 1024 字符。
- 顶层可选字段为 `license`、`compatibility`、`metadata`、`allowed-tools`；compatibility 不超过 500 字符，metadata 为字符串键值映射。版本等扩展信息放入 metadata，不将非标准顶层字段默认为跨工具兼容。
- `SKILL.md` 少于 500 行、描述触发清晰、渐进加载与相对资源引用属于指导性检查，不把上游风格偏好冒充硬性格式规定。
- 配套脚本、模板、许可证和跨 skill 引用必须按本次实际分发集合核对。完整 checkout 中存在文件，不代表单个 skill 安装后资源仍存在。
- 静态检查提交/推送/删除、全局配置修改、网络下载执行、凭据读取上传等指令及脚本；区分示例、用户确认后的操作与未经授权行为。格式校验不证明安全、业务效果或 IDE 兼容性。
- 官方 `skills-ref` 是参考/演示库，并非生产安全认证工具；仅在隔离检查目录运行，不成为模板的正式运行依赖。

### 可复现步骤

- [x] **获取检查样本并核对来源。** 在目标路径不存在时执行以下命令；已有 checkout 必须先检查来源和工作树，不覆盖。官方参考工具在本次检查中固定为 commit `83021e2be457a9b6679148719c1f6074f0ad975e`。

```bash
git clone --branch v7.0.2 --single-branch https://github.com/obra/superpowers.git .validation/preflight/superpowers
git clone https://github.com/MSiccDev/arc42-toolkit.git .validation/preflight/arc42-toolkit
git clone --depth 1 https://github.com/agentskills/agentskills.git .validation/preflight/agentskills-ref
```

分别执行 `git -C .validation/preflight/superpowers rev-parse HEAD`、`git -C .validation/preflight/arc42-toolkit rev-parse HEAD` 和 `git -C .validation/preflight/agentskills-ref rev-parse HEAD`。本次实际输出与固定 SHA 一致；重新获取时若 ref 发生变化，停止而不是检查浮动版本。

- [x] **检查官方校验器源码与依赖后，在隔离目录准备依赖。** 本次使用 Python 3.11.4、现有 click 8.3.3；以下依赖只写入 `.validation/`，不进行全局安装。

```bash
python3 -m pip install --target .validation/preflight/python-deps --no-deps --no-compile --disable-pip-version-check strictyaml==1.7.3 python-dateutil==2.9.0.post0 six==1.17.0
```

- [x] **逐项运行官方校验，不跳过失败项。** 直接调用参考库自带 CLI，不编写自制 schema 校验器。所有相对路径在项目根目录运行。

```bash
export PYTHONPATH="$PWD/.validation/preflight/agentskills-ref/skills-ref/src:$PWD/.validation/preflight/python-deps"
export PYTHONDONTWRITEBYTECODE=1
failed=0
for skill in .validation/preflight/{superpowers,arc42-toolkit}/skills/*; do
  python3 -m skills_ref.cli validate "$skill" || failed=$((failed+1))
done
printf '验证失败的 skill 数量：%s\n' "$failed"
test "$failed" -eq 0
```

### 本次实际结果与门禁状态

| 固定候选 | 数量 | 官方格式校验 | 当前处理 |
| --- | --- | --- | --- |
| Superpowers v7.0.2 | 15 | 15 通过、0 失败 | Task 1–3 已实施并通过文件验收；安装后格式复检通过；IDE 流程未全部验证 |
| arc42 toolkit | 14 | 0 通过、14 失败 | 用户已选择暂停引入；正式引入和 skill 运行试用均不继续 |

实际命令退出码为 1，输出 `验证失败的 skill 数量：14`，不是工具安装失败或测试跳过：

- 13 个 arc42 skill 报 `Unexpected fields in frontmatter: version`。所有 14 个原文均包含顶层 `version`，其中第 5 章尚未进入字段检查。
- `arc42-section-05/SKILL.md` 第 4 行的未引号 description 含 `toolkit convention: minimum expected output`，冒号后空格导致 YAML 解析失败，输出 `Invalid YAML in frontmatter: mapping values are not allowed here`。
- arc42 lint 引用根目录 `scripts/arc42-lint.py` 和 `scripts/languages/`；单独安装其 skill 目录无法保留自动检查资源。中文包缺失；以上问题不能以手工检查或空输入退出码 0 冒充自动 lint 通过。
- 两个候选的 MIT 许可证及固定 SHA 已核对。Superpowers 全量保留时，`executing-plans` 引用的兄弟 `subagent-driven-development/scripts/sdd-workspace` 确实存在；这是跨 skill 依赖，不是本次全量集合的已证实断链。
- Superpowers 的 worktree/执行流程包含提交或清理建议；项目“不提交、不清理用户工作树”约束仍优先。brainstorming 可启动本地服务，未获可视化许可不启动，不将无认证开发服务公开暴露。没有执行这些候选的脚本或 Agent 交互。

- [x] **已报告不合规项并取得用户决定：暂停引入 arc42。** 保留检查结果，不继续 Task 4 的 skill 运行试用或正式集成，不移动 version 字段、不替上游补引号，也不自动发布 issue/PR。恢复 arc42、寻找替代候选或仅作参考继续评估均需另行确认；不得将当前候选标注为合规 skill。

## Task 1: 固定版本的项目级 skill 集合

**文件：** 创建 `tests/__init__.py`（空文件）、`tests/test_template_integrity.py`、`.gitignore`；由 Skills CLI 生成 `.agents/skills/` 和 `skills-lock.json`。

**接口：** 消费固定的 Superpowers commit；产出 15 个保持上游名称的 skill、来源锁文件及完整性测试。Task 2 和 Task 3 使用同一个测试类。

- [x] **检查工作树和依赖。** 已核对版本和现有未提交文档。用户明确选择新建实施分支，已从 main 创建并切换到 `feat/superpowers-base`，保留当前全部文件；未创建 worktree、提交或修改全局配置。后续环境重新执行时仍需检查工作树和目标路径，不覆盖未知内容。
- [x] **创建失败测试。** 已创建空 `tests/__init__.py` 和 `tests/test_template_integrity.py`；内容以仓库文件为准，此处不保存副本。Task 1 先仅运行 `test_core`，其余方法供后续任务验收。
- [x] **确认 RED。** 实际运行 `test_core -v`，因缺少安装工具生成的 `skills-lock.json` 断言失败，退出码 1；不是模块导入错误。
- [x] **创建忽略规则。** Task 0 已提前创建以下规则，本次保留并验证，不覆盖原文件。

```gitignore
/.validation/
__pycache__/
*.pyc
```

- [x] **先列出上游集合，不安装。** 已运行以下命令，实际列出相同固定 commit 的 15 个名称，退出码 0：

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.9.0 add obra/superpowers@22f0b463e7a5e579904dd6211a520321035526f7 --list
```

预期列表是测试中的 15 个名称。命令、名称或固定 ref 不被支持时停止，不使用浮动版本或修改上游 skill 名称。

- [x] **安装唯一权威来源。** 已运行以下项目级安装命令，安装工具生成 15 个实目录及锁文件，退出码 0：

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.9.0 add obra/superpowers@22f0b463e7a5e579904dd6211a520321035526f7 --skill '*' --agent universal --yes
```

预期只进行项目级安装，安装工具生成锁文件，`.agents/skills/` 的目录是实际内容而非通向作者全局目录的链接。

- [x] **确认 GREEN 和来源。** `test_core` 实际通过，退出码 0；CLI 列表实际为 15 项、全部 `project`/`tracked`，无 `modified`、`missing` 或 `untracked`。
- [x] **检查配套资源。** `git diff --no-index --exit-code .validation/preflight/superpowers/skills .agents/skills` 实际退出码 0；全量脚本、参考资料和模板均与固定上游目录无差异。未改写路径，未提交。

## Task 2: 原版来源资料和薄入口

**文件：** 创建 `.agents/upstream/superpowers/LICENSE`、`.agents/upstream/superpowers/README.md`、`AGENTS.md`、`CLAUDE.md`；修改 `README.md`。

**接口：** 消费 Task 1 的唯一 skill 集合和 commit；产出可读的使用说明、明确授权边界和原文引用。入口不替代上游工作流。

- [x] **确认 RED。** 实际运行 `test_docs -v`，因上游许可证尚不存在断言失败，退出码 1。
- [x] **取得固定版本原文。** 本次读取已核实 SHA 且未修改的隔离 Git checkout，原样保存 README/LICENSE；两份文件分别与上游执行 `git diff --no-index --exit-code`，均无差异且退出码 0。未使用网页 HTML、行号或摘要。

```text
https://raw.githubusercontent.com/obra/superpowers/22f0b463e7a5e579904dd6211a520321035526f7/LICENSE
https://raw.githubusercontent.com/obra/superpowers/22f0b463e7a5e579904dd6211a520321035526f7/README.md
```

若网络读取失败，使用已有成熟 Git 获取方式读取同一 commit 的文件；不可退回本机安装的不同版本。README 中相对链接对应上游仓库，使用说明提供固定版本的上游网页链接。

- [x] **写入 `AGENTS.md`。** 已保存薄入口：项目范围、指向 `.agents/skills/` 的唯一来源、Superpowers 原文入口、第三方引入前门禁、arc42 暂停状态与授权边界。内容以仓库文件为准，此处不保存副本。

- [x] **写入 `CLAUDE.md`。** 已使用官方导入语法，完整内容只有一行 `@AGENTS.md`。

- [x] **修改根 `README.md`。** 已加入范围与来源、新项目用法、工具接入状态、本地验证与更新、验证证据与限制五节，并把固定版本与当前状态作为单一事实源。内容以仓库文件为准，此处不保存副本。

- [x] **确认 GREEN。** `test_docs` 和 `test_core` 实际均通过；来源原文无差异，未改变上游 skill。

## Task 3: 用成熟安装工具生成平台映射

**文件：** 安装工具生成 `.claude/skills/`、`.qoder/skills/`；使用已创建的 `tests/test_template_integrity.py`。

**接口：** 消费 Task 1 同一 commit 和 canonical skill；产出项目内相对链接。Cursor、Codex、Copilot、OpenCode 的项目路径本身为 `.agents/skills/`。

- [x] **确认 RED。** `test_portable_links -v` 实际因尚不存在 `.claude/`、`.qoder/` 的 30 个软链接断言失败，退出码 1。
- [x] **检查现有工具目录。** 实施前用文件工具确认目标目录不存在，未覆盖未知配置；后续安装工具只管理本次生成的路径。
- [x] **生成明确目标的映射。** 已执行以下命令，实际生成 Claude Code/Qoder 相对软链接，退出码 0：

```bash
DISABLE_TELEMETRY=1 npx --yes skills@1.9.0 add obra/superpowers@22f0b463e7a5e579904dd6211a520321035526f7 --skill '*' --agent claude-code qoder cursor codex github-copilot opencode --yes
```

不传 `--copy`、`--all`、`--global` 或 `--rename`。预期 `.agents/skills/` 仍为唯一实目录，额外工具路径只建立相对链接。

- [x] **确认 GREEN。** 全量模板测试当时 4 项全部通过（后续扩展到 7 项，当前值见 README）；CLI 列表实际 15 项、全部 `project`/`tracked`。
- [x] **确认工具边界。** 两组共 30 个链接均为项目内相对链接、无断链，canonical 为实目录。这里只认定文件映射通过；自动启动、hooks、子代理和跨工具流程不能据此认定通过。

## Task 4: arc42 固定版本的隔离行为试用

**状态：已暂停，不再执行。** 用户在 Task 0 门禁后决定暂停该候选的正式引入和运行试用，本任务不再作为待办；保留本节只记录结论，供后续恢复时参考。

- 暂停依据：官方格式检查 0/14 通过（13 个含非标准顶层 `version`，第 5 章另有 YAML 解析错误）；lint 依赖 skill 目录之外的根目录脚本，没有中文语言包，且只检查五类引用约定。详见 Task 0 与设计文档。
- 未执行项：未获取 `.validation/arc42-toolkit/` checkout，未创建 `tests/test_arc42_lint_trial.py`，未运行正反例、Agent 交互试用或图形渲染。这些项目一律不计为通过。
- 恢复条件：用户另行确认替代候选，或授权处理上游不合规问题；不自行修改上游原文，不编写中文适配，不拼接 Superpowers 与 arc42 两套流程。
- 与官方模板的区别：`docs/arc42-template/` 收录的是 arc42 官方中文模板（文档资产），不是本任务候选的 skill，二者的存在互不授权。

## Task 5: 可复现性、接入证据与交付

**文件：** 修改 `README.md` 的证据状态和试用结论；仅在已有明确事实时更新，不创建另一套工作流或自制验证脚本。

**接口：** 消费 Task 1–4 的文件、锁文件和实测结果；产出可复制模板、验证命令输出、逐工具证据和仍需用户决定的缺口。

**当前状态：** 本地文件验收和证据记录已执行；运行接入验收未全部完成。OpenCode 默认启动仍存在全局同名覆盖，已在单进程隔离会话中完成 TDD 与调试练习；arc42 仍暂停，克隆验证待分支推送后另行授权执行。

- [x] **执行全量本地验证。**

```bash
python3 -m unittest discover -s tests -v
DISABLE_TELEMETRY=1 npx --yes skills@1.9.0 list --json
git diff --check
git status --short
```

当前适用范围为 7 项模板测试，实际全部通过；arc42 的 7 项行为测试因用户暂停而未创建、未运行，不计为通过。15 个正式 skill 为 `tracked`，自定义 `arc42-architecture` 不写入锁文件。交互试用未完成，结构测试不能替代缺失证据。对明确新增的手写文件，另行执行以下命令；上游原文不为格式检查而改写。

```bash
git diff --no-index --check /dev/null AGENTS.md
git diff --no-index --check /dev/null CLAUDE.md
git diff --no-index --check /dev/null .gitignore
git diff --no-index --check /dev/null tests/__init__.py
git diff --no-index --check /dev/null tests/test_template_integrity.py
```

预期无 whitespace 报错；如命令仅因文件存在差异返回 1，不将其误报为测试失败。

- [ ] **验证相对链接和真正克隆，区分授权条件。** 当前先通过 `test_portable_links` 验证全部映射为项目内相对链接。真正克隆只能取得已提交内容：模板已提交 `0db625b`，但分支未推送，“克隆冒烟验证”仍记为未完成，不擅自推送，也不编写复制脚本绕过。用户授权推送后再执行：确认 `.validation/template-copy/` 不存在，`git clone --no-hardlinks . .validation/template-copy`，再执行 `python3 -m unittest discover -s .validation/template-copy/tests -p test_template_integrity.py -v`；预期 7 项通过，全部链接指向克隆自己的 `.agents/skills/`。本地 clone 不读取网络或全局 skill。
- [ ] **运行可用工具的接入验证。** 对 Qoder IDE、Claude Code、Cursor、Codex、Copilot、OpenCode 分别记录实际版本、产品形态、发现列表、加载的项目文件路径及新会话行为。先确认项目级 `using-superpowers` 和 `brainstorming`，再验证批准后的练习任务执行 TDD 和完成前验证。没有工具或会话权限的条目保留“未运行验证”。不擅自关闭用户的全局 skill；若无法排除全局来源影响，标注验证无效或受影响。
  - 固定合成练习输入：“仅在 `.validation/development-smoke/` 中实现 `clamp(value: int, low: int, high: int) -> int`，低于下限返回下限，高于上限返回上限，范围内返回原值；`low > high` 时抛出 `ValueError`。使用标准库 unittest，不提交、不修改全局配置。先澄清并展示设计，不立即编码。”预期先出现澄清和设计确认点。
  - 试验执行者批准该合成设计后，至少验证 `clamp(-2, 0, 5) == 0`、`clamp(7, 0, 5) == 5`、`clamp(3, 0, 5) == 3` 和反向边界异常。执行命令为 `python3 -m unittest discover -s .validation/development-smoke -v`；必须保留实现前失败、实现后通过的实际输出。
  - 随后在同一隔离练习中提供故障输入：“当前实现误用 `low >= high` 作为异常条件，新增 `clamp(3, 2, 2) == 2` 后测试失败，请按项目 skill 定位并修复。”只改本次合成练习，预期先进入 `systematic-debugging`、确认边界条件根因，再修复并重跑全量练习测试；修复前失败和修复后通过均需记录。无法构造或运行此故障时明确标注未验证。
- [x] **更新证据记录。** 根 README 和以下执行记录写明实际版本、来源、结果和失败/暂停项；未将未运行项目填为通过。
- [ ] **报告集成门槛。** arc42 仍是隔离候选，即使本次正反例通过，也不自动加入正式 `.agents/skills/`。报告资源布局、中文自动检查、图形依赖及与 Superpowers 衔接的结果，由用户明确决定是否正式集成或接受限制。完整需求工程或 Spec Kit 的引入仍单独确认。
- [ ] **交付而不提交。** 给出实际变更路径、验证输出、未运行工具和已知缺口。仅用户另外批准后，才选择提交、推送、PR 或合并。不得用 `finishing-a-development-branch` 的建议代替授权。

## 本次实施记录（2026-11-20）

- 用户选择新建 `feat/superpowers-base` 分支，实施结果已提交为 `0db625b`；分支未推送，未创建 worktree，未修改全局配置。提交后的清理与说明更新仍为未提交改动。
- Task 1–3 已完成：15 个固定版本 skill、工具生成锁文件、原版 README/LICENSE、薄入口、根说明和 30 个项目内相对链接。安装与映射命令实际额外设置 `npm_config_cache="$PWD/.validation/npm-cache"` 和 `TMPDIR="$PWD/.validation/preflight"`，使 CLI 检查缓存留在忽略目录；同时 `DISABLE_TELEMETRY=1`。
- RED → GREEN：核心安装前因缺少锁文件失败，安装后通过；来源资料前因缺少许可证失败，保存后通过；映射前有 30 个链接断言失败，映射后通过。当时全量模板测试 4/4 通过（后续扩展到 7 项），CLI 状态 15 项均为 `project`/`tracked`；正式 skill 的官方格式复检 15/15 通过。
- 完整 `skills/` 目录和来源 README/LICENSE 使用 `git diff --no-index --exit-code` 与固定 checkout 比对，无差异。未修改原版 skill 或手写锁文件。
- Qoder Remote CLI `1.106.3`：本会话通过 Skill 工具显式加载 `.qoder/skills/using-superpowers` 和 `.qoder/skills/systematic-debugging`，对应项目 canonical；未验证 Qoder 新会话自动触发。
- OpenCode CLI `1.19.4`：`debug skill --pure` 原生列表将 15 项指向项目 `.agents/skills/`。普通管道输出曾被截断，现有 `script` 伪终端采集后得到完整列表；这只是诊断采集，不是新增模板适配。
- OpenCode 的只读合成新会话 `ses_e08fe16e4ffeBhYQvKH866rCVw` 使用 `--pure --agent plan --format json`，输入为本计划 clamp 练习，并明确禁止写文件、提交、修改全局配置、服务器和可视化。实际 skill 工具 metadata 表明 `using-superpowers` 来自项目，但 `brainstorming` 来自 `$HOME/.agents/skills/brainstorming`，两份内容不同。命令退出码 0 不代表流程通过：来源冲突已证实。后续在固定源码（commit `148842ef7cb1bc34192b3fff57d0f9721ab9c801`）定位根因：`discoverSkills` 同时收集全局与项目同名 skill，`loadSkills` 以无界并发解析后按名称覆盖共享表，最终来源取决于完成顺序。用单进程 `OPENCODE_DISABLE_EXTERNAL_SKILLS=true` 与 `skills.paths` 重做练习会话 `ses_e08eea6b9ffelxIWsaVLdujOds`：实际加载 5 个本项目 skill，先澄清设计再编码，完成 TDD 与 `low >= high` 边界故障调试，练习测试 5/5 通过，写入仅限合成目录。默认启动的同名覆盖仍存在。
- Claude Code、Cursor、Codex、Copilot 的会话运行条件未在本次环境中找到；仍标注未运行验证。没有额外安装这些运行时或修改用户全局设置。
- Task 4 及 Task 5 的 arc42 行为验证暂停。克隆冒烟验证未执行（分支未推送），不擅自推送以凑验收。整体运行验收未完成。
- 后续变更：新增用户授权的自定义 skill `arc42-architecture`，项目共 16 个 skill 目录，锁文件仍只记 15 个第三方；`docs/arc42-template/` 删除发布包副本，改为逐文件 SHA-256 校验；README 作为状态与版本的单一事实源。

## 计划自检与执行停机条件

- 覆盖：正式基座、上游原文与锁、平台映射、arc42 候选评估与暂停记录、复制验证、授权边界分别对应 Task 0–5；运行验证包含先问后写、TDD 和边界故障诊断，章节交互试用已取消。
- Task 0 检查及 Task 1–3 的安装、来源资料和文件映射已完成；Task 5 本地验证通过。OpenCode 默认启动仍受同名覆盖影响，已用单进程隔离开关完成一次 TDD/调试练习；其余工具新会话和克隆仍未验证。Task 4 已暂停。不能宣称整体计划或全部工具验收完成，也不能用结构测试覆盖运行来源冲突。
- 固定输入：所有正式安装使用 Superpowers commit；arc42 在自己的隔离 checkout 中固定 commit；不依赖 main 或作者全局内容。
- 验收边界：结构测试不等于 IDE 运行验证；脚本正反例不等于架构正确性或中文支持；隔离候选不等于正式集成。
- 停机条件：第三方格式不合规、来源或资源不可复现、需要自制适配、安装覆盖未知文件、无法排除全局来源、脚本反例未检出时，停止受影响步骤并报告，不扩大授权。
- 不执行实验性同步/恢复命令作为首次使用前提，不创建自定义流程目录，不默认引入 Spec Kit。

## 已核实的实现参考

- Agent Skills 官方格式：https://agentskills.io/specification
- 官方参考校验器：https://github.com/agentskills/agentskills/tree/83021e2be457a9b6679148719c1f6074f0ad975e/skills-ref
- Skills CLI 1.9.0 文档：https://github.com/vercel-labs/skills/blob/50894c1d98bc45ca1ab127213e59d6525065b5e7/docs/commands.md
- 安装路径：https://github.com/vercel-labs/skills/blob/50894c1d98bc45ca1ab127213e59d6525065b5e7/docs/agents.md
- 项目锁文件 v2、commit 与 computedHash 字段：https://github.com/vercel-labs/skills/blob/50894c1d98bc45ca1ab127213e59d6525065b5e7/src/local-lock.ts
- Superpowers 稳定发布：https://github.com/obra/superpowers/releases/tag/v7.0.2
- Qoder IDE skill 机制：https://docs.qoder.com/extensions/skills
- Claude Code 文件导入机制：https://code.claude.com/docs/en/memory
- arc42 原版脚本：https://github.com/MSiccDev/arc42-toolkit/blob/97492c34cdbdb87dc6ea97ae6edbd9673167aed5/scripts/arc42-lint.py
- arc42 英文解析模式：https://github.com/MSiccDev/arc42-toolkit/blob/97492c34cdbdb87dc6ea97ae6edbd9673167aed5/scripts/languages/en.json
