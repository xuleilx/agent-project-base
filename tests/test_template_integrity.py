import hashlib
import json
import os
import re
import unittest
import zipfile
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
ARC42_TAG = "2026.10.19"
ARC42_COMMIT = "9057fe1f32ce543e546f76971515c537f0dd3f63"
ARC42_ASSET = "arc42-template-ZH-withhelp-markdown.zip"
ARC42_SHA256 = "92f20999625ef0b9ecb5996906c5ba7e37d55ac3f5c849f737e3adbd66b31638"


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

    def test_arc42_official_template(self):
        folder = ROOT / "docs" / "arc42-template"
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["tag"], ARC42_TAG)
        self.assertEqual(manifest["templateCommit"], ARC42_COMMIT)
        entry = next(f for f in manifest["files"] if f["name"] == ARC42_ASSET)
        self.assertEqual(entry["sha256"], ARC42_SHA256)
        archive = folder / ARC42_ASSET
        data = archive.read_bytes()
        self.assertEqual(len(data), entry["size"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), ARC42_SHA256)
        with zipfile.ZipFile(archive) as zf:
            members = [n for n in zf.namelist() if not n.endswith("/")]
            self.assertIn("arc42-template-ZH.md", members)
            for name in members:
                with self.subTest(file=name):
                    self.assertEqual((folder / name).read_bytes(), zf.read(name))
        extracted = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()}
        own = {"README.md", "LICENSE.txt", "manifest.json", ARC42_ASSET}
        self.assertEqual(extracted - own, set(members), "出现未登记的文件")
        license_text = (folder / "LICENSE.txt").read_text(encoding="utf-8")
        self.assertIn("Creative Commons Attribution-ShareAlike 4.0", license_text)
        notice = (folder / "README.md").read_text(encoding="utf-8")
        for needle in ("Gernot Starke", "Peter Hruschka", "CC BY-SA 4.0",
                       "https://creativecommons.org/licenses/by-sa/4.0/",
                       ARC42_TAG, ARC42_COMMIT, ARC42_SHA256, "未作修改"):
            self.assertIn(needle, notice)

    def test_custom_skill_format(self):
        name = "arc42-architecture"
        folder = ROOT / ".agents" / "skills" / name
        self.assertTrue(folder.is_dir(), "缺少项目自定义 arc42 skill")
        self.assertFalse(folder.is_symlink(), "权威来源不能是软链接")
        skill_path = folder / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        text = skill_path.read_text(encoding="utf-8")
        parts = text.split("---\n", 2)
        self.assertEqual(parts[0], "")
        self.assertEqual(len(parts), 3, "缺少完整 frontmatter")
        fields = {}
        for line in parts[1].splitlines():
            key, separator, value = line.partition(":")
            self.assertEqual(separator, ":", "此 skill 使用单行 YAML 标量")
            self.assertNotIn(key, fields, "frontmatter 存在重复字段")
            fields[key] = value.strip()
        self.assertEqual(set(fields), {"name", "description"})
        self.assertEqual(fields["name"], name)
        self.assertRegex(fields["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(fields["name"]), 64)
        self.assertTrue(fields["description"])
        self.assertLessEqual(len(fields["description"]), 1024)
        self.assertTrue(parts[2].strip(), "缺少 skill 正文")
        self.assertLess(len(text.splitlines()), 500)
        lock = json.loads((ROOT / "skills-lock.json").read_text(encoding="utf-8"))
        self.assertNotIn(name, lock["skills"], "自定义 skill 不能伪造第三方锁记录")

    def test_custom_skill_portable_links(self):
        name = "arc42-architecture"
        target = ROOT / ".agents" / "skills" / name
        for agent_dir in (".claude", ".qoder"):
            with self.subTest(agent=agent_dir):
                link = ROOT / agent_dir / "skills" / name
                self.assertTrue(link.is_symlink(), "缺少自定义 skill 平台映射")
                self.assertFalse(os.path.isabs(os.readlink(link)))
                self.assertTrue(link.is_dir(), "自定义 skill 链接断开")
                self.assertEqual(link.resolve(), target.resolve())

    def test_no_custom_workflow(self):
        self.assertFalse((ROOT / ".agents" / "workflows").exists())
        ignores = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("/.validation/", ignores)
        self.assertIn("__pycache__/", ignores)
