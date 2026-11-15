# kondate-market

「パーソナル献立＆コンディショニング・コックピット」が読み込む、**週2回更新の食品物価レポート**です。

- `market.json` … 最新の物価レポート（Claudeが毎週水曜・土曜の朝にニュースを調べて更新）
- `validate.py` … `market.json` がアプリで読める形か確認するスクリプト
- `CLAUDE.md` … 更新作業の手順（Claude用）

アプリの「設定」→「Claudeの週次物価レポート」に次のURLを入れると使えます。

```
https://raw.githubusercontent.com/hide100111010-spec/kondate-market/main/market.json
```

ここには物価のまとめ（どの食材が高い・安いか、価格に影響するニュース、出典）だけを置きます。家族の情報やAPIキーは含みません。
