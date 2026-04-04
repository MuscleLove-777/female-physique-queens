@echo off
REM ============================================
REM FEMALE PHYSIQUE QUEENS - 毎日自動実行バッチ
REM ============================================
REM
REM このバッチはタスクスケジューラから呼ばれる。
REM 手動で実行もOK: ダブルクリックで起動。
REM
REM 事前準備:
REM   環境変数 ANTHROPIC_API_KEY に Claude API キーをセットすること
REM   （システム環境変数 or このファイルに直書き）
REM ============================================

REM --- APIキー（未設定の場合はここに書く） ---
REM set ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx

REM --- Google Custom Search（オプション: あるとより良い検索結果） ---
REM set GOOGLE_API_KEY=your-google-api-key
REM set GOOGLE_CX=your-custom-search-engine-id

cd /d "c:\Users\atsus\000_ClaudeCode\004_MuscleLove\female-physique-blog"

echo [%date% %time%] === FEMALE PHYSIQUE QUEENS 自動巡回開始 === >> data\crawl_log.txt

python crawl_and_generate.py >> data\crawl_log.txt 2>&1

echo [%date% %time%] === 完了 === >> data\crawl_log.txt
echo. >> data\crawl_log.txt
