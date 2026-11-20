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
- `tests/__init__.py`、`tests/test_template_integrity.py`、`tests/test_arc42_lint_trial.py`：标准库测试。

修改：`README.md`。除更新确认状态外，不改变已确认设计的范围。

隔离内容：`.validation/arc42-toolkit/` 为上游试用 checkout；`.validation/` 中的测试样本、日志和 Agent 草稿均不分发，不加入正式 skill 锁文件。新增 `.validation/preflight/` 只用于引入前检查：两个候选的原版 checkout、官方参考校验器和隔离依赖；不加入 `.agents/skills/` 或 IDE 发现路径。

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
- [x] **创建失败测试。** 已创建空 `tests/__init__.py` 和以下测试；Task 1 先仅运行 `test_core`，其余方法供后续任务验收。

```python
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "22f0b463e7a5e579904dd6211a520321035526f7"
NAMES = {
    "brainstorming", "diagnosing-superpowers", "dispatching-parallel-agents",
    "executing-plans", "finishing-a-development-branch", "receiving-code-review",
    "requesting-code-review", "subagent-driven-development", "systematic-debugging",
    "test-driven-development", "using-git-worktrees", "using-superpowers",
    "verification-before-completion", "writing-plans", "writing-skills",
}


class TemplateIntegrityTests(unittest.TestCase):
    def test_core(self):
        lock_path = ROOT / "skills-lock.json"
        self.assertTrue(lock_path.is_file(), "缺少安装工具生成的 skills-lock.json")
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertEqual(lock["version"], 2)
        self.assertEqual(set(lock["skills"]), NAMES)
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                folder = ROOT / ".agents" / "skills" / name
                self.assertTrue(folder.is_dir())
                self.assertFalse(folder.is_symlink())
                text = (folder / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                header = text.split("---", 2)[1]
                self.assertRegex(header, rf"(?m)^name:\s*['\"]?{re.escape(name)}['\"]?\s*$")
                entry = lock["skills"][name]
                self.assertIn("obra/superpowers", entry["source"])
                self.assertEqual(entry["commit"], COMMIT)
                self.assertRegex(entry["computedHash"], r"^[0-9a-f]{64}$")

    def test_docs(self):
        upstream = ROOT / ".agents" / "upstream" / "superpowers"
        self.assertTrue((upstream / "LICENSE").is_file(), "缺少上游许可证")
        license_text = (upstream / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT", license_text)
        self.assertTrue((upstream / "README.md").is_file())
        agent_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("using-superpowers", agent_text)
        self.assertIn("未经明确授权，不执行 Git 提交、推送或创建 PR。", agent_text)
        self.assertEqual((ROOT / "CLAUDE.md").read_text(encoding="utf-8").strip(), "@AGENTS.md")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(COMMIT, readme)
        self.assertIn("评估试用", readme)
        self.assertIn("工具接入状态", readme)

    def test_portable_links(self):
        for agent_dir in (".claude", ".qoder"):
            for name in sorted(NAMES):
                with self.subTest(agent=agent_dir, skill=name):
                    link = ROOT / agent_dir / "skills" / name
                    target = ROOT / ".agents" / "skills" / name
                    self.assertTrue(link.is_symlink())
                    self.assertFalse(os.path.isabs(os.readlink(link)))
                    self.assertEqual(link.resolve(), target.resolve())

    def test_no_custom_workflow(self):
        self.assertFalse((ROOT / ".agents" / "workflows").exists())
        ignores = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("/.validation/", ignores)
        self.assertIn("__pycache__/", ignores)
```

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

- [x] **写入 `AGENTS.md`。** 已保存以下薄入口，并加入已批准的第三方标准门禁、arc42 暂停和可视化授权约束；没有新增工作流。

```markdown
# 项目级 Agent 入口

本项目是可复制的开发基座，第一版终点为测试验证和合并/PR 交付，不包含生产部署自动化。

## 上游能力入口

项目 skill 的唯一来源是 `.agents/skills/`。执行任务前检查适用 skill，并通过宿主工具支持的机制加载 `using-superpowers`。

开发方法沿用 Superpowers 原版：`.agents/upstream/superpowers/README.md`。触发条件、阶段确认和产出物约定以上游 skill 为准，本文件不定义新工作流。

需求澄清当前使用 `brainstorming`，不宣称已覆盖完整需求工程。arc42 toolkit 仅评估试用，未正式加入项目 skill 集合，也未采纳 Spec Kit。

## 项目约束

- 保留上游 skill 原文及配套资源，不自行重写或拼接流程。
- 需要尚未核实的适配或额外工具时，先说明缺口并向用户确认。
- 不修改全局 skill、IDE 用户配置或 Git 配置。
- 未经明确授权，不执行 Git 提交、推送或创建 PR。
- 不覆盖未知用户内容，不删除或清理用户工作树。
- 完成前提供实际测试输出；未运行的验证明确标注。
```

- [x] **写入 `CLAUDE.md`。** 已使用官方导入语法，完整内容只有一行：

```text
@AGENTS.md
```

- [x] **修改根 `README.md`。** 已保留项目标题，通过精确编辑加入以下使用说明的范围、来源、使用方式及授权边界；实际文件同时记录 arc42 暂停和最新验证证据，未照抄已过时的状态。以下为实施前的说明基线，当前状态以根 README 和本计划执行记录为准。

```markdown
# agent-project-base

可复制的软件开发基座：原样复用成熟 skill 和工作流，通用内容只在 `.agents/` 维护。

## 范围与来源

第一版覆盖需求澄清、设计、计划、开发、测试验证和合并/PR；不包含 CI/CD 或生产部署自动化。

正式 skill 集合为 Superpowers v7.0.2：`22f0b463e7a5e579904dd6211a520321035526f7`，共 15 个 skill。来源和内容校验由 `skills-lock.json` 记录。

原版流程说明：`.agents/upstream/superpowers/README.md`。
固定版本上游：https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7
许可证：`.agents/upstream/superpowers/LICENSE`。

arc42 toolkit 是评估试用候选：`97492c34cdbdb87dc6ea97ae6edbd9673167aed5`，尚未正式集成。自动 lint 没有中文语言包，且只检查部分引用约定，不能替代架构内容评审。

## 在新项目中使用

复制或克隆模板，保留隐藏目录、相对软链接和锁文件；不要只复制可见文件。skill 内容随项目提供，不依赖作者本机的全局安装。

在业务项目中补充自己的技术栈、测试命令和验收条件。本基座不预设所有项目使用同一种测试工具。

用目标工具的原生 skill 机制加载 `using-superpowers`。需求讨论使用 `brainstorming`，执行计划、TDD、调试、评审与验证以上游说明为准；这些是能力索引，不是另造的串行调度器。

## 工具接入状态

| 工具 | 项目 skill 来源 | 当前证据状态 |
| --- | --- | --- |
| Qoder IDE | `.qoder/skills/` 引用 `.agents/skills/` | 官方安装路径已核实，未运行验证 |
| Claude Code | `.claude/skills/` 引用 `.agents/skills/`；`CLAUDE.md` 导入入口 | 官方接入机制已核实，未运行验证 |
| Cursor | `.agents/skills/` | 安装工具路径已核实，未运行验证 |
| Codex | `.agents/skills/` | 安装工具路径已核实，未运行验证 |
| GitHub Copilot | `.agents/skills/` | 安装工具路径已核实，未运行验证 |
| OpenCode | `.agents/skills/` | 安装工具路径已核实，未运行验证 |

能发现 skill 不等于能自动启动全部工作流、hooks 或子代理。运行验证后逐项更新证据状态；CLI 结论不能替代 IDE 结论。

## 本地验证与更新

要求 Node.js >= 22.20.0、Python >= 3.11。安装管理使用固定的 `skills@1.9.0`。

核心完整性测试：`python3 -m unittest tests.test_template_integrity -v`。
查看来源及内容状态：`npx --yes skills@1.9.0 list --json`。
arc42 行为测试依赖隔离 checkout，按实施计划准备后执行 `python3 -m unittest tests.test_arc42_lint_trial -v`。

更新属于显式维护操作：先审核新版本差异，再固定新 commit，通过 Skills CLI 更新项目内容和锁文件，重跑测试与接入验证。本次不自动追随 main，也不依赖实验性恢复/同步命令完成模板首次使用。

未经明确授权，不执行 Git 提交、推送或创建 PR。发现没有成熟接入方案的缺口时先确认，不自行编写适配。
```

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

- [x] **确认 GREEN。** 全量模板测试实际 4/4 通过；CLI 列表实际 15 项、全部 `project`/`tracked`。
- [x] **确认工具边界。** 两组共 30 个链接均为项目内相对链接、无断链，canonical 为实目录。这里只认定文件映射通过；自动启动、hooks、子代理和跨工具流程不能据此认定通过。

## Task 4: arc42 固定版本的隔离行为试用

**文件：** 创建 `tests/test_arc42_lint_trial.py`；获取 `.validation/arc42-toolkit/` 完整上游 checkout。试用资料、Agent 草稿和输入样本保留在 `.validation/`，不进入正式锁文件。

**接口：** 消费固定 arc42 commit 的原版 `scripts/arc42-lint.py` 及其 `languages/`；产出正例、五条规则的反例、空输入行为证据。没有中文支持结论或正式集成结论。

- [ ] **创建以下完整测试。** 测试夹具保留上游英文解析关键字和 ID，正文可使用中文；这是已知英文结构的基线试验，不代表中文自动 lint 已得到支持。测试样本是合成数据，不是用户业务需求或已批准架构。

```python
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".validation" / "arc42-toolkit" / "scripts" / "arc42-lint.py"
DOCS = {
    "01-introduction.md": "# 1. 引言与目标\n\n| Priority | Quality Goal | Scenario |\n| --- | --- | --- |\n| 1 | #efficient | 合成负载下 p95 <= 200ms |\n",
    "03-context.md": "# 3. 上下文\n\n| ID | Partner | Purpose |\n| --- | --- | --- |\n| IF-01 | 调用者 | 提交输入 |\n",
    "05-building-blocks.md": "# 5. 构建块\n\n| Name | Responsibility | Interfaces |\n| --- | --- | --- |\n| AgentBase | 处理输入 | IF-01 |\n",
    "07-deployment.md": "# 7. 部署视图\n\nAgentBase 部署在示范进程中。\n",
    "09-decisions.md": "# 9. 架构决策\n\n## ADR-001: 示例选择\n\nRisks created: RISK-01\n",
    "10-quality.md": "# 10. 质量要求\n\n### QS-01: 示例延迟\n\n| Field | Value |\n| --- | --- |\n| Quality property | #efficient |\n\n| ID | Description | Current State | Target |\n| --- | --- | --- | --- |\n| QS-02 | 尚未测量的场景 | not measured | 200ms |\n",
    "11-risks.md": "# 11. 风险与技术债\n\n| ID | Description |\n| --- | --- |\n| RISK-01 | 示例风险 |\n\nQS-02 尚未达到，需要后续测量。\n",
}


class Arc42LintTrialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT / ".validation").mkdir(exist_ok=True)
        if not SCRIPT.is_file():
            raise RuntimeError("缺少固定版本 arc42 checkout；不能跳过试用并报告通过")

    def invoke(self, documents):
        case = Path(tempfile.mkdtemp(prefix="arc42-case-", dir=ROOT / ".validation"))
        for name, content in documents.items():
            (case / name).write_text(content, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(case), "--lang", "en", "--format", "text", "--strict"],
            capture_output=True, text=True, timeout=30,
        )
        return result.returncode, result.stdout + result.stderr

    def assert_rule_failure(self, rule, name, content):
        documents = dict(DOCS)
        documents[name] = content
        code, output = self.invoke(documents)
        self.assertEqual(code, 1, output)
        self.assertIn(rule, output)
        self.assertNotIn("nothing to lint", output)

    def test_valid_reference_set(self):
        code, output = self.invoke(DOCS)
        self.assertEqual(code, 0, output)
        self.assertIn("all consistency rules passed", output)
        self.assertNotIn("nothing to lint", output)

    def test_interface_mismatch(self):
        self.assert_rule_failure("RULE-1", "05-building-blocks.md", DOCS["05-building-blocks.md"].replace("IF-01", "IF-02"))

    def test_missing_deployment_mapping(self):
        self.assert_rule_failure("RULE-2", "07-deployment.md", "# 7. 部署视图\n\n没有组件映射。\n")

    def test_quality_tag_mismatch(self):
        self.assert_rule_failure("RULE-3", "10-quality.md", DOCS["10-quality.md"].replace("#efficient", "#reliable"))

    def test_unregistered_adr_risk(self):
        self.assert_rule_failure("RULE-4", "09-decisions.md", DOCS["09-decisions.md"].replace("RISK-01", "RISK-99"))

    def test_unlinked_aspirational_scenario(self):
        self.assert_rule_failure("RULE-5", "11-risks.md", DOCS["11-risks.md"].replace("QS-02", "QS-03"))

    def test_empty_input_is_not_architecture_validation(self):
        code, output = self.invoke({})
        self.assertEqual(code, 0, output)
        self.assertIn("nothing to lint", output)
```

测试样本暂留忽略目录用于核实证据，不调用删除或清理用户文件的命令。最后一项只记录上游的空输入行为，不把退出码 0 当作架构检查完成。

- [ ] **确认 RED。** 执行 `python3 -m unittest tests.test_arc42_lint_trial -v`。预期缺少固定版本 checkout 而失败，而不是跳过所有测试。
- [ ] **获取原版完整试用布局。** 首先确认 `.validation/arc42-toolkit/` 不存在；已有目录时先核对来源和改动，不覆盖。随后执行：

```bash
git clone https://github.com/MSiccDev/arc42-toolkit.git .validation/arc42-toolkit
git -C .validation/arc42-toolkit fetch origin 97492c34cdbdb87dc6ea97ae6edbd9673167aed5
git -C .validation/arc42-toolkit status --short
git -C .validation/arc42-toolkit switch --detach 97492c34cdbdb87dc6ea97ae6edbd9673167aed5
git -C .validation/arc42-toolkit rev-parse HEAD
```

只有新 clone 工作树干净时才切换，最后一条输出必须是固定 SHA。保留整个上游布局，避免仅安装 skill 而遗失根目录脚本。这里切换的是本次创建的隔离上游仓库，不是用户项目分支。

- [ ] **确认 GREEN。** 重跑 `tests.test_arc42_lint_trial`。预期 7 项通过，代表正例和特定反例的脚本行为被验证，不代表全部架构质量合格。反例未检出时记录缺陷，不修改上游代码以凑出通过。
- [ ] **核实完整资源与中文边界。** 使用文件工具检查 14 个 skill、许可证、脚本、六个语言包和独立图形约定。执行 `python3 .validation/arc42-toolkit/scripts/arc42-lint.py --help`，确认实际只支持 `text` 和 `github` 输出，不假设存在 JSON 模式。中文包仍标注缺失，不编写补丁。
- [ ] **进行 Agent 交互试用。** 在具备运行条件的工具中打开隔离 checkout，按上游 README 已有方式发现或引用原版 skill；无法原生发现时只采用其文档中的文件上下文引用方式，不新增运行时适配。按以下固定合成案例验证：
  - 先只提出“为一个项目内 AI 开发基座生成 arc42 第 1 章”，不给质量指标；预期第 1 章询问目的、利益相关者、质量目标、已有需求和深度，而不是直接臆造指标生成完整文档。
  - 明确这是试验，提供五个功能：项目内 skill、原版流程引用、版本锁定、工具发现映射、验证证据。提供三个合成目标：项目内容中作者家目录绝对引用为 0；15 个 skill 的来源可追溯率为 100%；未经授权的全局修改和提交次数为 0。确认者为本次试验执行者，深度为 ESSENTIAL。预期形成第 1 章草稿及确认点；不能把试验执行者确认冒充用户业务签字。
  - 引用原版第 4 章 skill，提供“所有内容项目内保存、禁止全局安装”的约束，要求比较目录映射策略并标出重大 ADR；预期策略关联质量目标和约束，而非无依据生成技术选型。
  - 引用原版第 9 章 skill，将第 4 章中的“项目内唯一来源＋相对软链接”作为试验决定，备选为全局插件和多份复制；提供已确认的三个合成目标与禁止全局安装约束。要求形成 `ADR-001`，说明备选取舍、可移植性代价和 `RISK-01`（目标环境不支持软链接），并指出第 11 章需登记该风险。预期决策可回溯至目标和约束，不把合成决定当作正式基座新增授权。
  - 分别引用原版第 3、5、7 章 skill，明确合成上下文为“调用者通过 IF-01 请求 AgentBase；AgentBase 在示范进程中运行”，要求各章保持同一个接口 ID、组件名称与部署对应关系，并关联 `ADR-001`。预期视图互相一致；没有实际业务拓扑的内容只标注为示范。
  - 用原版 `arc42-review` 检查一份故意将“禁止全局安装”与“采用全局插件”同时写入的试验稿，以及未量化的“速度快”质量目标和缺少 ADR 的重大决定；预期报告冲突、质量场景不足和决策记录缺口。再评审补齐量化目标和 `ADR-001`、去除全局安装矛盾的修正版，记录同类问题是否消失；不能将 Agent 的意见当作架构正确性证明。
  - 在工具支持时用上游章节 skill 生成 C4 PlantUML 文件，使用该环境已有渲染器验证；没有渲染器时记录“图形已生成、未验证渲染”，不自行安装未经确认的运行时。

交互验证没有运行条件时记录阻塞，不用阅读 skill 内容代替运行结果。实际 Agent 行为、脚本正反例和图形渲染三个维度分别报告。

## Task 5: 可复现性、接入证据与交付

**文件：** 修改 `README.md` 的证据状态和试用结论；仅在已有明确事实时更新，不创建另一套工作流或自制验证脚本。

**接口：** 消费 Task 1–4 的文件、锁文件和实测结果；产出可复制模板、验证命令输出、逐工具证据和仍需用户决定的缺口。

**当前状态：** 本地文件验收和证据记录已执行；运行接入验收未全部完成。OpenCode 新会话存在来源混用，后续合成练习已停止；arc42 仍暂停，克隆验证待另行提交授权。

- [x] **执行全量本地验证。**

```bash
python3 -m unittest discover -s tests -v
DISABLE_TELEMETRY=1 npx --yes skills@1.9.0 list --json
git diff --check
git status --short
```

当前适用范围为 4 项模板测试，实际全部通过；arc42 的 7 项行为测试因用户暂停而未创建、未运行，不计为通过。15 个正式 skill 为 `tracked`。交互试用未完成，结构测试不能替代缺失证据。对明确新增的手写文件，另行执行以下命令；上游原文不为格式检查而改写。

```bash
git diff --no-index --check /dev/null AGENTS.md
git diff --no-index --check /dev/null CLAUDE.md
git diff --no-index --check /dev/null .gitignore
git diff --no-index --check /dev/null tests/__init__.py
git diff --no-index --check /dev/null tests/test_template_integrity.py
```

预期无 whitespace 报错；如命令仅因文件存在差异返回 1，不将其误报为测试失败。

- [ ] **验证相对链接和真正克隆，区分授权条件。** 当前先通过 `test_portable_links` 验证全部映射为项目内相对链接。真正克隆只能取得已提交内容：用户尚未授权提交时，将“克隆冒烟验证”明确记录为未完成，不擅自提交，也不编写复制脚本绕过。用户另外授权并完成模板提交后，确认 `.validation/template-copy/` 不存在，执行 `git clone --no-hardlinks . .validation/template-copy`，再执行 `python3 -m unittest discover -s .validation/template-copy/tests -p test_template_integrity.py -v`；预期 4 项通过，全部链接指向克隆自己的 `.agents/skills/`。本地 clone 不读取网络或全局 skill，也不包含被忽略的试用 checkout。
- [ ] **运行可用工具的接入验证。** 对 Qoder IDE、Claude Code、Cursor、Codex、Copilot、OpenCode 分别记录实际版本、产品形态、发现列表、加载的项目文件路径及新会话行为。先确认项目级 `using-superpowers` 和 `brainstorming`，再验证批准后的练习任务执行 TDD 和完成前验证。没有工具或会话权限的条目保留“未运行验证”。不擅自关闭用户的全局 skill；若无法排除全局来源影响，标注验证无效或受影响。
  - 固定合成练习输入：“仅在 `.validation/development-smoke/` 中实现 `clamp(value: int, low: int, high: int) -> int`，低于下限返回下限，高于上限返回上限，范围内返回原值；`low > high` 时抛出 `ValueError`。使用标准库 unittest，不提交、不修改全局配置。先澄清并展示设计，不立即编码。”预期先出现澄清和设计确认点。
  - 试验执行者批准该合成设计后，至少验证 `clamp(-2, 0, 5) == 0`、`clamp(7, 0, 5) == 5`、`clamp(3, 0, 5) == 3` 和反向边界异常。执行命令为 `python3 -m unittest discover -s .validation/development-smoke -v`；必须保留实现前失败、实现后通过的实际输出。
  - 随后在同一隔离练习中提供故障输入：“当前实现误用 `low >= high` 作为异常条件，新增 `clamp(3, 2, 2) == 2` 后测试失败，请按项目 skill 定位并修复。”只改本次合成练习，预期先进入 `systematic-debugging`、确认边界条件根因，再修复并重跑全量练习测试；修复前失败和修复后通过均需记录。无法构造或运行此故障时明确标注未验证。
- [x] **更新证据记录。** 根 README 和以下执行记录写明实际版本、来源、结果和失败/暂停项；未将未运行项目填为通过。
- [ ] **报告集成门槛。** arc42 仍是隔离候选，即使本次正反例通过，也不自动加入正式 `.agents/skills/`。报告资源布局、中文自动检查、图形依赖及与 Superpowers 衔接的结果，由用户明确决定是否正式集成或接受限制。完整需求工程或 Spec Kit 的引入仍单独确认。
- [ ] **交付而不提交。** 给出实际变更路径、验证输出、未运行工具和已知缺口。仅用户另外批准后，才选择提交、推送、PR 或合并。不得用 `finishing-a-development-branch` 的建议代替授权。

## 本次实施记录（2026-11-20）

- 用户选择新建 `feat/superpowers-base` 分支；当前变更全部保留为未提交内容，未创建 worktree，未推送或修改全局配置。
- Task 1–3 已完成：15 个固定版本 skill、工具生成锁文件、原版 README/LICENSE、薄入口、根说明和 30 个项目内相对链接。安装与映射命令实际额外设置 `npm_config_cache="$PWD/.validation/npm-cache"` 和 `TMPDIR="$PWD/.validation/preflight"`，使 CLI 检查缓存留在忽略目录；同时 `DISABLE_TELEMETRY=1`。
- RED → GREEN：核心安装前因缺少锁文件失败，安装后通过；来源资料前因缺少许可证失败，保存后通过；映射前有 30 个链接断言失败，映射后通过。全量模板测试 4/4 通过，CLI 状态 15 项均为 `project`/`tracked`；正式 skill 的官方格式复检 15/15 通过。
- 完整 `skills/` 目录和来源 README/LICENSE 使用 `git diff --no-index --exit-code` 与固定 checkout 比对，无差异。未修改原版 skill 或手写锁文件。
- Qoder Remote CLI `1.106.3`：本会话通过 Skill 工具显式加载 `.qoder/skills/using-superpowers` 和 `.qoder/skills/systematic-debugging`，对应项目 canonical；未验证 Qoder 新会话自动触发。
- OpenCode CLI `1.19.4`：`debug skill --pure` 原生列表将 15 项指向项目 `.agents/skills/`。普通管道输出曾被截断，现有 `script` 伪终端采集后得到完整列表；这只是诊断采集，不是新增模板适配。
- OpenCode 的只读合成新会话 `ses_e08fe16e4ffeBhYQvKH866rCVw` 使用 `--pure --agent plan --format json`，输入为本计划 clamp 练习，并明确禁止写文件、提交、修改全局配置、服务器和可视化。实际 skill 工具 metadata 表明 `using-superpowers` 来自项目，但 `brainstorming` 来自 `$HOME/.agents/skills/brainstorming`，两份内容不同。命令退出码 0 不代表流程通过：来源冲突已证实，具体根因及原生隔离机制未定位，后续 TDD/调试练习停止，等待用户决定。不采用该会话建议的全局版本继续执行，也不通过手工文件引用冒充原生加载通过。
- Claude Code、Cursor、Codex、Copilot 的会话运行条件未在本次环境中找到；仍标注未运行验证。没有额外安装这些运行时或修改用户全局设置。
- Task 4 及 Task 5 的 arc42 行为验证继续暂停。克隆冒烟验证因模板未提交而未执行，不能擅自提交以凑验收。整体运行验收未完成。

## 计划自检与执行停机条件

- 覆盖：正式基座、上游原文与锁、平台映射、arc42 正反例和交互试用、复制验证、授权边界分别对应 Task 1–5；章节交互试用包含第 1、4、9 章以及第 3、5、7 章视图关联，运行验证包含先问后写、TDD 和边界故障诊断。
- Task 0 检查及 Task 1–3 的安装、来源资料和文件映射已完成；Task 5 本地验证通过，但 OpenCode 运行接入因实际来源混用而阻塞，其余工具新会话、合成 TDD/调试和克隆仍未验证。Task 4 及依赖 arc42 的验收继续暂停。不能宣称整体计划或全部工具验收完成，也不能用结构测试覆盖运行来源冲突。
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
