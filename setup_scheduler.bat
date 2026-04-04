@echo off
REM ============================================
REM タスクスケジューラに毎日AM9:00実行を登録するバッチ
REM 管理者権限で実行してください（右クリック→管理者として実行）
REM ============================================

schtasks /create /tn "FemalePhysiqueQueens_DailyCrawl" /tr "c:\Users\atsus\000_ClaudeCode\004_MuscleLove\female-physique-blog\run_daily.bat" /sc daily /st 09:00 /f

if %errorlevel% equ 0 (
    echo.
    echo ✅ タスクスケジューラに登録完了！
    echo    タスク名: FemalePhysiqueQueens_DailyCrawl
    echo    実行時間: 毎日 AM 9:00
    echo    実行内容: Web巡回 → Claude API で記事生成 → ブログ更新
    echo.
    echo    変更する場合: タスクスケジューラを開いて編集してください。
    echo    削除する場合: schtasks /delete /tn "FemalePhysiqueQueens_DailyCrawl" /f
) else (
    echo.
    echo ❌ 登録に失敗しました。管理者権限で実行してください。
)

pause
