# Google Search Console セットアップ手順

対象サイト: https://musclelove-777.github.io/female-physique-queens/

> 参考: FANZAアフィリプロジェクトにも設定レポートあり
> `051_FANZAアフィリ/GA4_SearchConsole設定レポート_260331.pptx`

---

## 1. プロパティの追加

1. https://search.google.com/search-console にGoogleアカウントでログイン
2. 左上のプロパティセレクタ → 「プロパティを追加」をクリック
3. **「URLプレフィックス」** を選択（右側）
4. `https://musclelove-777.github.io/female-physique-queens/` を入力
5. 「続行」をクリック

**なぜURLプレフィックス？** GitHub Pagesはサブディレクトリ型URLなので、ドメインプロパティ（左側）は使えない。URLプレフィックスを選ぶ必要がある。

---

## 2. 所有権の確認（HTMLファイル方式）

**なぜHTMLファイル方式？** GitHub Pagesではリポジトリにファイルを置くだけで確認完了できるため、最も簡単。DNS設定やHTMLタグ編集が不要。

1. Search Consoleが表示する確認画面で「HTMLファイル」タブを選択
2. `googleXXXXXXXXXXXX.html` というファイルをダウンロード（XXXXは自分固有のコード）
3. ダウンロードしたファイルをリポジトリのルートに配置:

```
female-physique-queens/
  googleXXXXXXXXXXXX.html   <-- ここに置く
  index.html
  ...
```

4. Git で commit & push:

```bash
cd /path/to/female-physique-queens
git add googleXXXXXXXXXXXX.html
git commit -m "Add Google Search Console verification file"
git push origin main
```

5. GitHub Pagesへのデプロイを待つ（通常1-2分）
6. Search Console画面に戻り「確認」ボタンをクリック
7. 「所有権を確認しました」と表示されれば成功

---

## 3. サイトマップの送信

**なぜサイトマップ？** Googleにサイト内の全ページを効率的に発見・クロールしてもらうために必要。

### 3-1. サイトマップの作成

現在このサイトには `sitemap.xml` が存在しない。以下のようなファイルを作成してリポジトリルートに配置する:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://musclelove-777.github.io/female-physique-queens/</loc>
    <lastmod>2026-04-04</lastmod>
  </url>
  <!-- 記事ページがあれば追加 -->
</urlset>
```

commit & push してデプロイを待つ。

### 3-2. Search Console で送信

1. Search Console左メニュー →「サイトマップ」
2. 「新しいサイトマップの追加」に `sitemap.xml` と入力
3. 「送信」をクリック
4. ステータスが「成功しました」になれば完了

---

## 補足: 確認後にやること

- **インデックス登録のリクエスト**: 左メニュー「URL検査」→ サイトURLを入力 →「インデックス登録をリクエスト」で即時クロールを依頼できる
- **検索パフォーマンスの確認**: データが反映されるまで2-3日かかる。左メニュー「検索パフォーマンス」で確認
