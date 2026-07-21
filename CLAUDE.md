# Female Physique Queens - ブログ自動更新ガイド

## プロジェクト概要
「腹筋バキバキの女しか勝たん」をモットーにした女性フィジーカー紹介ブログ。
Instagramで写真を公開しているBikini & Physique部門の選手を紹介する。

## 掲載対象（ロスター）
記事対象の選手リスト（Instagram公開アカウント限定）は必ず `references/roster.md` を読んで参照すること。リストの追加・更新もそのファイルに対して行う。

## 記事生成ルール
- 日本語で書く
- 1記事200〜400文字
- タイトルはキャッチーに（腹筋・バキバキ・筋肉系ワード歓迎）
- 熱量のあるファン目線（「エロい」「たまらん」OK）
- 出典URLを必ず含める
- カテゴリは bikini または physique
- トピック例: 大会結果、選手紹介、トレーニング、比較、ランキング
- 全記事とindex.htmlのフッター直前に MuscleLove広告カード（ML_PROMO_CARDマーカー）を必ず含める。広告カードにはX / Patreon / ゲームポータルの3導線を必ず入れる

## ファイル構成
- `index.html` — メインページ（記事カードは `<div class="blog-grid">` 内）
- `style.css` — スタイル
- `script.js` — フィルター・アニメーション
- `articles/` — 個別記事HTML（YYYYMMDD_NN.html 形式）
- `config.json` — 選手リスト・検索キーワード
- `data/` — クロール履歴・ログ

## 記事HTML テンプレート
個別記事は `articles/YYYYMMDD_NN.html` に保存。
スタイルは `../style.css` を参照。
index.html に戻るリンクを含める。
フッター（`<footer`）直前に以下のMuscleLove広告カードを必ず挿入する（マーカーごとコピー）:
```html
<!-- ML_PROMO_CARD_START -->
<section style="max-width:800px;margin:32px auto;padding:0 20px;">
  <div style="background:#111827;border:1px solid rgba(255,255,255,0.14);border-radius:10px;padding:24px;text-align:center;">
    <p style="margin:0 0 6px;color:#f0f0f5;font-weight:800;">MuscleLove 公式</p>
    <p style="margin:0 0 14px;color:#9ca3af;font-size:0.9rem;">最新情報・限定コンテンツはこちら</p>
    <div style="display:flex;flex-wrap:wrap;gap:10px;justify-content:center;">
      <a href="https://x.com/MuscleGirlLove7" target="_blank" rel="noopener" style="display:inline-block;padding:10px 18px;background:#1d9bf0;color:#fff;border-radius:6px;font-weight:800;text-decoration:none;">X @MuscleGirlLove7</a>
      <a href="https://www.patreon.com/MuscleLove" target="_blank" rel="noopener" style="display:inline-block;padding:10px 18px;background:#ff424d;color:#fff;border-radius:6px;font-weight:800;text-decoration:none;">Patreon 限定コンテンツ</a>
      <a href="https://musclelove-games.vercel.app/?utm_source=blog&amp;utm_medium=promo_card&amp;utm_campaign=female-physique-blog" target="_blank" rel="noopener" style="display:inline-block;padding:10px 18px;background:#22c55e;color:#0b1220;border-radius:6px;font-weight:800;text-decoration:none;">🎮 無料ブラウザゲームで遊ぶ</a>
    </div>
  </div>
</section>
<!-- ML_PROMO_CARD_END -->
```

## index.html 更新方法
`<div class="blog-grid">` 内の `<article class="blog-card">` を最大6件に保つ。
新しい記事を先頭に追加し、古い記事を末尾から削除する。
各カードのフォーマット:
```html
<article class="blog-card" onclick="window.location='articles/YYYYMMDD_NN.html'" style="cursor:pointer;">
    <div class="blog-image" style="background: linear-gradient(135deg, #色1, #色2);"></div>
    <div class="blog-body">
        <span class="blog-date">YYYY.MM.DD</span>
        <h3>記事タイトル</h3>
        <p>記事の要約...</p>
    </div>
</article>
```

## コミットメッセージ
`[auto] Add daily articles YYYY-MM-DD` の形式で。
