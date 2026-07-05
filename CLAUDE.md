# Female Physique Queens - ブログ自動更新ガイド

## プロジェクト概要
「腹筋バキバキの女しか勝たん」をモットーにした女性フィジーカー紹介ブログ。
Instagramで写真を公開しているBikini & Physique部門の選手を紹介する。

## 掲載選手（Instagram公開アカウント限定）
### 日本
- 安井友梨 (@yuri.yasui.98) - IFBB Bikini Pro, 191K followers
- ダンシーあずさ (@az.official__) - JBBF Bikini 5連覇, ~100K followers
- 黒川夢 (@yume_ifbbpro) - IFBB Bikini Pro, 66K followers
- 野田ユリカ (@yurika_ifbbpro) - IFBB Bikini Olympian, 3x Olympia
- MISA (@misamisa_ifbb_figure_pro) - IFBB Figure Pro, 72K followers
- 渋谷美穂 (@shibuya_miho) - 腹筋女子日本一

### 韓国
- ソン・アルム (@ahreum_song) - IFBB Bikini Pro, 285K followers
- イ・ユナ (@lynzzzzang) - IFBB Bikini Pro

### 海外
- Maureen Blanquisco (@maureenblanquisco) - 🇵🇭 2x Bikini Olympia Champion
- Lauralie Chapados (@lauraliechap) - 🇨🇦 Bikini Olympia Champion
- Karen Yuen Campion (@karenfit.ifbbpro) - 🇭🇰 First HK Olympian
- Janet Layug (@janetlayug) - 🇺🇸 Bikini Olympia Champion

## 記事生成ルール
- 日本語で書く
- 1記事200〜400文字
- タイトルはキャッチーに（腹筋・バキバキ・筋肉系ワード歓迎）
- 熱量のあるファン目線（「エロい」「たまらん」OK）
- 出典URLを必ず含める
- カテゴリは bikini または physique
- トピック例: 大会結果、選手紹介、トレーニング、比較、ランキング
- 全記事とindex.htmlのフッター直前に MuscleLove広告カード（ML_PROMO_CARDマーカー）を必ず含める

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
