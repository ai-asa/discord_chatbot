# Discord Chatbot

AIを活用したDiscordチャットボットシステムです。OpenAI GPT、Claude、その他のAIモデルを使用して会話を生成し、Discord上でインタラクティブなコミュニケーションを実現します。

## 機能

- 複数のAIモデル対応（OpenAI GPT、Claude）
- 会話履歴の管理
- メタ認知による応答生成
- 感情表現を含む応答
- マルチプロセスによる並列処理
- 詳細なログ記録

## セットアップ

### 1. 必要なパッケージのインストール

以下のコマンドで必要なパッケージをインストールします：
```
    pip install -r requirements.txt
```
### 2. 環境変数の設定

`.env`を作成し、以下の項目を設定してください：

    OPENAI_API_KEY=your_openai_api_key
    DISCORD_TOKEN=your_discord_token
    TARGET_CHANNEL_ID=your_channel_id
    CLAUDE_API_KEY=your_claude_api_key

### 3. 設定ファイルの準備

`config.ini`に必要な設定を行ってください：

    [CONFIG]
    aituber_name = your_bot_name
    retry_limit = 5
    historys_limit = 4
    openai_model = gpt-3.5-turbo-0125
    claude_model = claude-3-haiku-20240307

    [INDEX]
    theme_q_csv_path = ./data/qtheme.csv
    theme_r_csv_path = ./data/rtheme.csv
    theme_c_csv_path = ./data/ctheme.csv
    theme_o_csv_path = ./data/otheme.csv
    meta_csv_path = ./data/meta.csv
    action_csv_path = ./data/action.csv

### 4. データファイルの準備

`data`ディレクトリに以下のCSVファイルを配置してください：
- qtheme.csv: 質問テーマ
- rtheme.csv: 応答テーマ
- ctheme.csv: 会話テーマ
- otheme.csv: その他テーマ
- meta.csv: メタ認知データ
- action.csv: アクションデータ

## 使用方法

1. ボットの起動:

    python main.py

2. Discordサーバーでボットを招待し、設定したチャンネルで会話を開始します。

## ディレクトリ構造

    .
    ├── src/
    │   ├── chat/          # チャットアダプター
    │   ├── discord/       # Discordボット関連
    │   ├── ltm/           # インデックス管理
    │   ├── prompt/        # プロンプト生成
    │   ├── splitter/      # テキスト分割
    │   └── voice/         # 音声処理
    ├── data/              # データファイル
    ├── log/               # ログファイル
    ├── main.py           # メインスクリプト
    ├── run_system.py     # システム実行
    ├── config.ini        # 設定ファイル
    └── .env              # 環境変数

## ログ

ログは`log`ディレクトリ内の以下のファイルに記録されます：
- processlog.log: メインプロセスのログ
- subprocces1.log: サブプロセス1のログ
- subprocces2.log: サブプロセス2のログ
- subprocces3.log: サブプロセス3のログ
- subprocces_discord.log: Discordボットのログ

## 注意事項

- APIキーは必ず`.env`ファイルで管理し、公開リポジトリにアップロードしないでください
- 大量のリクエストを送信する場合は、各APIの利用制限に注意してください
- ボットの応答内容は、設定したプロンプトやAIモデルの特性に依存します
