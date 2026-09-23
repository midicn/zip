#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""zip 站包索引生成器。

输入：`meta/packs-manifest.json`（由 midicn-lib 仓的 `tools/build_dim_packs.py --verify` 产出，
      经 `midi-lib` 仓 `meta/` 目录单源发布，CI 从 raw.githubusercontent 拉取）
输出：`data/packs.json`（按 8 个维度分组的包清单，供 index.html 渲染）

为什么单独出这个文件：站点要「按维度折叠 + 每包一行」，而 manifest 是平铺数组；
在这里做一次分组，页面就只做渲染，不必内嵌业务逻辑。

用法：python tools/gen_packs_index.py --in meta/packs-manifest.json --out data/packs.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# 维度显示名与排序（顺序即页面折叠区顺序）
DIMS = [
    ("source",   "来源",       "Source"),
    ("genre",    "风格",       "Genre"),
    ("period",   "时期",       "Period"),
    ("instrument", "乐器",     "Instrument"),
    ("zone",     "授权档位",   "Licence tier"),
    ("form",     "曲式",       "Form"),
    ("region",   "地域",       "Region"),
    ("composer", "作曲家",     "Composer"),
]
DIM_NAME = {k: (zh, en) for k, zh, en in DIMS}
DIM_ORDER = {k: i for i, (k, _zh, _en) in enumerate(DIMS)}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", default="meta/packs-manifest.json")
    ap.add_argument("--out", dest="dst", default="data/packs.json")
    args = ap.parse_args(argv[1:])

    src = Path(args.src)
    if not src.exists():
        print(f"[err] 未找到 {src}", file=sys.stderr)
        return 1
    man = json.loads(src.read_text(encoding="utf-8"))

    packs = man.get("packs") or []
    if not packs:
        print("[err] manifest 里没有 packs", file=sys.stderr)
        return 1

    groups: dict[str, list] = {}
    for p in packs:
        groups.setdefault(p["dim"], []).append(p)

    dims = []
    for dim in sorted(groups, key=lambda d: DIM_ORDER.get(d, 99)):
        items = sorted(groups[dim], key=lambda p: -(p.get("count") or 0))
        zh, en = DIM_NAME.get(dim, (dim, dim))
        dims.append({
            "id": dim, "zh": zh, "en": en,
            "packs": len(items),
            "tracks": sum((p.get("count") or 0) for p in items),
            "bytes": sum((p.get("bytes") or 0) for p in items),
            "items": items,
        })

    out = {
        "version": man.get("version"),
        "release_tag": man.get("release_tag"),
        "base_url": man.get("base_url"),
        "total_tracks": man.get("total_tracks"),
        "generated": man.get("generated"),
        "packs": len(packs),
        "bytes": sum((p.get("bytes") or 0) for p in packs),
        "dims": dims,
    }
    dst = Path(args.dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    print(f"[ok] {dst}：{len(packs)} 包 / {len(dims)} 维度 / {out['bytes']/1e9:.2f} GB")
    for d in dims:
        print(f"     {d['zh']:8} {d['packs']:>4} 包 · {d['tracks']:>8,} 首 · {d['bytes']/1e6:>8.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
