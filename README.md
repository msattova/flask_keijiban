# flask keijiban

flaskで作成したwebアプリケーション（掲示板）です。

## 必要なもの

* python: 開発環境のバージョンは3.10だが3.7などでも問題なく動くはず
* requirements.txt記載のライブラリ（requirements.txtがあるディレクトリで以下のコマンドを実行することで一度に導入可能）

```
pip install -r requirements.txt
```

## 実行の仕方

### 準備

1. .envファイルを用意するなどして環境変数FLASK_APPに'keijiban'を設定。
2. requirements.txt記載の必要なライブラリを導入する

### 実行

1. flask_keijibanディレクトリ下で`flask --app keijiban init-db`を実行。これによってデータベースを初期化する。（データベースはschema.sqlに記載されたコマンドを基に作成される）
2. `flask run`コマンドを実行。これによって開発モードでwebアプリケーションが起動する。実行に成功すれば"Running on http://127.0.0.1:5000 "というようなメッセージが出力されるので、このメッセージで示されるアドレスにwebブラウザでアクセスすると動作確認ができる。

## 仕様

* ユーザ登録、ログイン、投稿の表示、プロフィール設定などの機能を備えた簡易的なSNS風の掲示板webアプリ
* ユーザ登録時、「不適切な言葉を変換して表示する」にチェックをつけることで、放送禁止用語などのいわゆる不適切な表現が言い換えられた状態で表示されるようになる（プロフィール編集画面から設定の変更が可能）
* 投稿、プロフィール文章にはmarkdown記法によるテキストの装飾が可能（ただし、現状では``` *em*, **strong**, `code` ```にのみ対応）
* ユーザ登録時にニックネームの欄を空にするとユーザー名がニックネームとして登録される。
* レイアウトはtailwindcssというcssのフレームワークを利用して作成

## 備考

大部分はFlaskの[チュートリアル](https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/tutorial/index.html)を参考に作成

不適切な言葉とその言い換え語のリストについては http://monoroch.net/kinshi/ で公開されている[放送禁止用語リスト](http://monoroch.net/kinshi/kinshi.csv)を基にしている。
