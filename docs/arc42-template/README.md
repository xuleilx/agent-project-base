# arc42 官方模板（简体中文，带写作说明，Markdown）

本目录原样收录 arc42 官方 Release 发布的模板，作为文档资产使用；它不是 skill，也不定义工作流。arc42 toolkit 仍处于暂停引入状态，与本目录无关。

## 来源与版本

| 项目 | 值 |
| --- | --- |
| 来源仓库 | https://github.com/arc42/arc42-template |
| Release tag | `2026.10.19` |
| 模板源 commit | `9057fe1f32ce543e546f76971515c537f0dd3f63` |
| 模板版本 | 9.1-ZH（10月 2026） |
| 发布包 | `arc42-template-ZH-withhelp-markdown.zip`（536893 字节） |
| 发布包 SHA-256 | `92f20999625ef0b9ecb5996906c5ba7e37d55ac3f5c849f737e3adbd66b31638` |
| manifest.json SHA-256 | `e6f2a71e243bc54d9de21ab3ea4cfa0ce709c3857096167137c3cc40d9c29d7e` |

文件说明：

- `manifest.json`：同一 Release 的官方清单，原样保存，其中记录了发布包的名称、大小和 SHA-256。
- `arc42-template-ZH.md`、`images/`：从官方发布包直接解压，未作修改。
- `LICENSE.txt`：模板源 commit 中的官方许可证声明，原样复制。
- `README.md`：本说明，由本基座添加，不属于 arc42 模板。

官方发布包 `arc42-template-ZH-withhelp-markdown.zip` 不随仓库保存：其解压内容已逐文件收录，再存一份原件属于重复副本。需要核对来源时，按上表的 tag 和 SHA-256 从官方 Release 重新下载该发布包比对。

## 署名与许可证

- 作品：arc42 模板（arc42, the template for software architecture documentation and communication）
- 作者与许可方：Dr. Gernot Starke、Dr. Peter Hruschka 及贡献者，https://arc42.org
- 简体中文译者：Chris (Gentle) Y杨、DannyGe
- 许可证：Creative Commons Attribution-ShareAlike 4.0 International（CC BY-SA 4.0），https://creativecommons.org/licenses/by-sa/4.0/
- 许可说明：https://arc42.org/license，及本目录 `LICENSE.txt`
- 修改情况：模板文件及图片均未作修改，仅新增本 README.md。

本基座与 arc42.org 无隶属关系，上述署名不表示许可方认可本基座或使用本模板的项目。

按官方许可说明：

- 在组织内部复制、修改和使用模板，无需公开。
- 把修改后的模板提供给组织外部（网站、公开仓库、随产品发布）时，修改版须同样采用 CC BY-SA 4.0，并署名、附许可证链接、说明改动。
- 填入模板的架构内容归内容作者所有，按 arc42 结构发布架构文档不会使这些内容适用 CC BY-SA。

## 使用

把 `arc42-template-ZH.md` 和 `images/` 复制到业务项目的文档位置后再填写，不要直接修改本目录中的原件。

带帮助版本中每章的写作说明位于 `:::: sidebar`／`::: note` 块（Pandoc fenced div 语法）中，普通 Markdown 预览会把它们显示为普通文本。官方说明建议：带帮助版本用于熟悉 arc42；编写自己的系统文档时更适合使用纯文本（plain）版本。

## 校验与更新

本目录内容由 `tests/test_template_integrity.py` 中的 `test_arc42_official_template` 校验：

- `manifest.json` 中的 tag、模板 commit 和发布包 SHA-256；
- 收录文件各自的 SHA-256 与测试中的固定值一致，且目录中没有未登记文件，也没有重复的发布包副本；
- 许可证声明和本 README 中的署名信息。

更新属于显式维护操作：先审阅新 Release 的变更，再下载新 Release 的 `manifest.json` 与发布包，核对发布包 SHA-256 和解压内容，替换本目录文件，并同步更新本 README 和测试中的固定值，最后重跑测试。
