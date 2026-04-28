"""female-physique-blog (female-physique-queens) 自動記事生成エントリ"""
from __future__ import annotations
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, r"C:\Users\atsus\000_ClaudeCode\007_自動投稿ブログ")
import fitness_auto_post_lib as lib  # noqa: E402

CLAUDE_MD = (HERE / "CLAUDE.md").read_text(encoding="utf-8") if (HERE / "CLAUDE.md").exists() else ""

CFG = {
    "site_dir": HERE,
    "blog_name": "FEMALE PHYSIQUE QUEENS",
    "site_url": "https://musclelove-777.github.io/female-physique-queens",
    "twitter_site": "@MuscleGirlLove7",
    "accent_color": "#d4af37",
    "categories": [
        "フィジーク選手紹介", "大会レポート", "ポージング講座", "ボディメイク食事",
        "トレーニング理論", "コラム",
    ],
    "seed_topics": CLAUDE_MD,
    "image_query": "physique women fitness",
}

if __name__ == "__main__":
    res = lib.run(CFG)
    print(res)
