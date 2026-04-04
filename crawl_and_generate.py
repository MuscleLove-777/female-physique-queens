"""
FEMALE PHYSIQUE QUEENS - 自動巡回 & 記事生成スクリプト
（Claude Max 版 — APIキー不要、DuckDuckGoで検索 → テンプレ記事生成）

処理の流れ:
1. config.json の選手リスト + 一般キーワードでDuckDuckGo検索
2. 新しいネタ（大会結果、投稿、動画）を収集
3. テンプレートベースで記事HTMLを生成
4. articles/ フォルダにHTMLとして保存
5. index.html の記事セクションを自動更新
6. data/pending_sources.json に「Claude Codeで記事化すべきネタ」を保存

※ Claude Code のスケジュール機能と併用推奨。
  スケジュールエージェントが pending_sources.json を読んで
  リッチな記事を生成 → HTMLに書き込む運用。

使い方:
  python3 crawl_and_generate.py           # 巡回 + 簡易記事生成
  python3 crawl_and_generate.py --collect  # 巡回のみ（ネタ収集だけ）
"""

import json
import os
import sys
import re
import hashlib
from datetime import datetime
from pathlib import Path

import requests

# --- Windows コンソール UTF-8 対応 ---
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# --- 設定読み込み ---
SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_PATH = SCRIPT_DIR / "config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

BLOG_DIR = Path(CONFIG["blog_dir"])
ARTICLES_DIR = BLOG_DIR / CONFIG["articles_dir"]
DATA_DIR = BLOG_DIR / CONFIG["data_dir"]
HISTORY_FILE = DATA_DIR / "crawl_history.json"
PENDING_FILE = DATA_DIR / "pending_sources.json"

ARTICLES_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"generated_hashes": [], "last_run": None}


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def content_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


# ============================================
# Web検索
# ============================================

def search_duckduckgo(query: str, num_results: int = 5) -> list[dict]:
    """DuckDuckGo HTML検索"""
    url = "https://html.duckduckgo.com/html/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FemalePhysiqueQueens/1.0"}
    try:
        resp = requests.post(url, data={"q": query}, headers=headers, timeout=15)
        resp.raise_for_status()
        text = resp.text
        results = []
        # リンクとスニペットを抽出
        pattern = r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>'
        snippet_pattern = r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>'

        links = re.findall(pattern, text, re.DOTALL)
        snippets = re.findall(snippet_pattern, text, re.DOTALL)

        for i, (href, title) in enumerate(links[:num_results]):
            # URLデコード
            if "uddg=" in href:
                m = re.search(r'uddg=([^&]+)', href)
                href = requests.utils.unquote(m.group(1)) if m else href

            title = re.sub(r'<[^>]+>', '', title).strip()
            snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""

            if href and title:
                results.append({"title": title, "snippet": snippet, "url": href})
        return results
    except Exception as e:
        print(f"  [WARN] Search failed for '{query}': {e}")
        return []


def search_web(query: str, num_results: int = 5) -> list[dict]:
    """Google Custom Search（APIキーあれば）→ DuckDuckGo fallback"""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    google_cx = os.environ.get("GOOGLE_CX")

    if google_api_key and google_cx:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {"key": google_api_key, "cx": google_cx, "q": query, "num": min(num_results, 10)}
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return [
                {"title": item.get("title", ""), "snippet": item.get("snippet", ""), "url": item.get("link", "")}
                for item in data.get("items", [])
            ]
        except Exception:
            pass

    return search_duckduckgo(query, num_results)


# ============================================
# コンテンツ収集
# ============================================

def collect_news() -> list[dict]:
    all_results = []
    today = datetime.now().strftime("%Y-%m")

    print("\n=== アスリート別検索 ===")
    for athlete in CONFIG["athletes"]:
        name = athlete["name_ja"] or athlete["name_en"]
        print(f"  🔍 {name}")
        for kw in athlete["search_keywords"][:2]:
            query = f"{kw} {today}"
            results = search_web(query, num_results=3)
            for r in results:
                r["athlete"] = name
                r["category"] = athlete["category"]
                r["instagram"] = athlete["instagram"]
            all_results.extend(results)

    print("\n=== 一般キーワード検索 ===")
    for kw in CONFIG["general_search_keywords"][:3]:
        print(f"  🔍 {kw}")
        results = search_web(kw, num_results=3)
        for r in results:
            r["athlete"] = "general"
            r["category"] = "general"
            r["instagram"] = ""
        all_results.extend(results)

    # 重複URL除去
    seen_urls = set()
    unique = []
    for r in all_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            unique.append(r)

    print(f"\n  📊 {len(unique)} 件の検索結果（重複除去済み）")
    return unique


# ============================================
# テンプレートベース記事生成
# ============================================

GRADIENTS = [
    "linear-gradient(135deg, #ff6b9d, #c44569)",
    "linear-gradient(135deg, #a29bfe, #6c5ce7)",
    "linear-gradient(135deg, #55efc4, #00b894)",
    "linear-gradient(135deg, #fd79a8, #e84393)",
    "linear-gradient(135deg, #ffeaa7, #fdcb6e)",
    "linear-gradient(135deg, #74b9ff, #0984e3)",
    "linear-gradient(135deg, #fab1a0, #e17055)",
    "linear-gradient(135deg, #ff9ff3, #f368e0)",
]


def generate_simple_articles(search_results: list[dict], history: dict) -> list[dict]:
    """
    検索結果からテンプレートベースで記事カードを生成。
    （APIキー不要。Claude Codeスケジュールで後からリッチ化も可能。）
    """
    articles = []
    max_articles = CONFIG.get("max_articles_per_run", 3)

    # スニペットが長い = 情報量が多い順にソート
    sorted_results = sorted(search_results, key=lambda r: len(r.get("snippet", "")), reverse=True)

    for i, r in enumerate(sorted_results):
        if len(articles) >= max_articles:
            break

        title = r["title"]
        h = content_hash(title)
        if h in history["generated_hashes"]:
            continue

        # フィットネス関連か簡易チェック
        fitness_keywords = ["ビキニ", "フィジーク", "bikini", "physique", "IFBB", "FWJ", "Olympia",
                           "筋肉", "腹筋", "fitness", "muscle", "abs", "competition", "大会",
                           "フィットネス", "プロ", "pro", "bodybuilding"]
        text = (title + " " + r.get("snippet", "")).lower()
        if not any(kw.lower() in text for kw in fitness_keywords):
            continue

        snippet = r.get("snippet", "")
        athlete = r.get("athlete", "")
        category = r.get("category", "bikini")
        gradient = GRADIENTS[i % len(GRADIENTS)]

        # 記事本文を組み立て
        body_parts = []
        if snippet:
            body_parts.append(f"<p>{snippet}</p>")
        if athlete and athlete != "general":
            ig = r.get("instagram", "")
            body_parts.append(
                f'<p><strong>{athlete}</strong> に関する最新情報。'
                + (f' Instagram: <a href="https://www.instagram.com/{ig}/" target="_blank">@{ig}</a>' if ig else "")
                + "</p>"
            )
        body_parts.append(f'<p>詳細は<a href="{r["url"]}" target="_blank" rel="noopener">元記事</a>をチェック。</p>')

        article = {
            "title": title[:80],
            "category": category if category != "general" else "bikini",
            "body": "\n".join(body_parts),
            "source_url": r["url"],
            "athletes_mentioned": [athlete] if athlete and athlete != "general" else [],
            "gradient": gradient,
        }

        history["generated_hashes"].append(h)
        articles.append(article)

    print(f"\n  ✅ {len(articles)} 本の記事を生成")
    return articles


# ============================================
# HTML生成 & ブログ更新
# ============================================

def save_article_html(article: dict, index: int) -> str:
    today = datetime.now().strftime("%Y%m%d")
    filename = f"{today}_{index:02d}.html"
    filepath = ARTICLES_DIR / filename

    athletes_tags = "".join(f'<span class="tag">{a}</span>' for a in article.get("athletes_mentioned", []))

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} - FEMALE PHYSIQUE QUEENS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <nav class="filter-nav">
        <div class="container">
            <a href="../index.html" style="color: var(--primary); text-decoration: none; font-family: 'Oswald', sans-serif; font-size: 1.1rem; letter-spacing: 0.1em;">&#8592; FEMALE PHYSIQUE QUEENS</a>
        </div>
    </nav>
    <main class="container">
        <article class="article-detail" style="padding: 60px 0;">
            <div class="blog-image" style="height: 250px; border-radius: 12px; background: {article.get('gradient', GRADIENTS[0])}; margin-bottom: 30px;"></div>
            <span class="blog-date">{datetime.now().strftime('%Y.%m.%d')}</span>
            <h1 style="font-family: 'Oswald', sans-serif; font-size: 2rem; color: #fff; margin: 15px 0; line-height: 1.4;">{article['title']}</h1>
            <div class="card-stats" style="margin-bottom: 20px;">
                <span class="tag">{article['category'].upper()}</span>
                {athletes_tags}
            </div>
            <div style="font-size: 1rem; line-height: 2; color: var(--text-muted);">
                {article['body']}
            </div>
            <p style="margin-top: 30px; font-size: 0.8rem; color: var(--text-muted);">
                出典: <a href="{article.get('source_url', '#')}" target="_blank" rel="noopener" style="color: var(--accent);">{article.get('source_url', '')}</a>
            </p>
        </article>
    </main>
    <footer class="footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Female Physique Queens. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  📝 {filepath.name}")
    return filename


def update_index_html(articles: list[dict]):
    index_path = BLOG_DIR / "index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    today = datetime.now().strftime("%Y%m%d")

    new_cards = ""
    for i, article in enumerate(articles):
        filename = f"{today}_{i:02d}.html"
        gradient = article.get("gradient", GRADIENTS[0])
        body_preview = re.sub(r'<[^>]+>', '', article['body'])[:80]
        new_cards += f"""
            <article class="blog-card" onclick="window.location='articles/{filename}'" style="cursor:pointer;">
                <div class="blog-image" style="background: {gradient};"></div>
                <div class="blog-body">
                    <span class="blog-date">{datetime.now().strftime('%Y.%m.%d')}</span>
                    <h3>{article['title'][:60]}</h3>
                    <p>{body_preview}...</p>
                </div>
            </article>"""

    blog_grid_pattern = r'(<div class="blog-grid">)(.*?)(</div>\s*</section>)'
    match = re.search(blog_grid_pattern, html, re.DOTALL)

    if match:
        existing_cards = match.group(2)
        card_pattern = r'<article class="blog-card".*?</article>'
        existing_list = re.findall(card_pattern, existing_cards, re.DOTALL)
        max_display = 6
        keep_count = max(0, max_display - len(articles))
        kept_cards = "\n            ".join(existing_list[:keep_count])
        updated_cards = new_cards + ("\n            " + kept_cards if kept_cards else "")
        html = html[:match.start(2)] + updated_cards + html[match.end(2):]

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  🔄 index.html 更新完了（{len(articles)}件追加）")


def save_pending_sources(search_results: list[dict]):
    """Claude Code スケジュールエージェント用にネタを保存"""
    pending = {
        "collected_at": datetime.now().isoformat(),
        "sources": search_results[:20],
        "status": "pending",
    }
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)
    print(f"  💾 pending_sources.json に {len(search_results[:20])} 件保存")


# ============================================
# メイン
# ============================================

def main():
    collect_only = "--collect" in sys.argv

    print("=" * 60)
    print(f"  FEMALE PHYSIQUE QUEENS - 自動巡回")
    print(f"  モード: {'ネタ収集のみ' if collect_only else '巡回 + 記事生成'}")
    print(f"  実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    history = load_history()

    # 1. コンテンツ収集
    search_results = collect_news()

    if not search_results:
        print("\n  ⚠️ 検索結果0件。ネットワークを確認してください。")
        return

    # pending_sources に保存（Claude Code用）
    save_pending_sources(search_results)

    if collect_only:
        history["last_run"] = datetime.now().isoformat()
        save_history(history)
        print("\n  ✅ ネタ収集完了。Claude Code スケジュールで記事化してください。")
        return

    # 2. テンプレートベースで記事生成
    articles = generate_simple_articles(search_results, history)

    if not articles:
        print("\n  ⚠️ 新規記事なし（既出ネタのみ）。")
        return

    # 3. HTML保存
    for i, article in enumerate(articles):
        save_article_html(article, i)

    # 4. index.html 更新
    update_index_html(articles)

    # 5. 履歴保存
    history["last_run"] = datetime.now().isoformat()
    save_history(history)

    print("\n" + "=" * 60)
    print(f"  ✅ 完了！{len(articles)}本の記事を追加しました。")
    print("=" * 60)


if __name__ == "__main__":
    main()
