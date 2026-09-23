# zip.midicn.com · midicn-lib 维度包下载站

按 **8 个维度**（来源 / 风格 / 时期 / 乐器 / 授权档位 / 曲式 / 地域 / 作曲家）切分的
MIDI 子集包下载站。全部数据来自开放许可来源，逐曲标注许可。

- **本仓**：`midicn/zip-site`（GitHub Pages）
- **数据仓**：`midicn/midi-lib`（Release 分发；`meta/version.json` 与 `meta/packs-manifest.json` 为单源）
- **姊妹站**：`lib.midicn.com`（音乐库 + 4 用途包）· `mid.midicn.com`（维度浏览）

## 目录

| 路径 | 用途 |
| --- | --- |
| `index.html` | 维度包总览与下载（8 维度折叠 + 逐包一行） |
| `404.html` | 404 页 |
| `assets/style.css` | **lib 站的复制件，勿单独修改**（改样式请改 lib 站再复制） |
| `assets/site.css` | 本站专属样式覆盖层 |
| `tools/gen_packs_index.py` | `meta/packs-manifest.json` → `data/packs.json`（按维度分组） |
| `data/packs.json` | 构建产物（CI 生成，不入仓） |

## 版本与清单单源

`deploy.yml` 不硬编码版本号，而是：

1. 从 `raw.githubusercontent.com/midicn/midi-lib/main/meta/version.json` 取 `version`；
2. 从同一目录取 `meta/packs-manifest.json`（由 `midi-lib` 仓 `tools/build_dim_packs.py` 产出）；
3. 生成 `data/packs.json` 后部署。

**因此发版只需在 `midi-lib` 仓更新 `meta/` 两个文件**，本仓无需改动。

## 自定义域（首次配置顺序，务必遵守）

DNS 未生效时**不要**先提交 `CNAME`，否则 `configure-pages` 会失败：

1. 先不带 `CNAME` 部署，确认 Pages 站点可用；
2. 在 DNS 添加 `CNAME zip → midicn.github.io`；
3. DNS 生效后，用 API 把自定义域绑到本仓 Pages。

## 许可

站点代码 MIT；元数据 CC BY 4.0；**MIDI 素材依各来源许可**（C1 可商用 / C2 非商用 / C3 仅研究学习）。
详见 <https://lib.midicn.com/licenses.html>。
