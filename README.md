# zendesk_to_elastic

# 前提条件
Zendesk APIトークンを取得していること
elasticsearchのDockerが起動していること
pythonがインストールされていること
開発時点では3.9

以降のバージョンでは動作未確認

# 環仮想環境境立ち上げ
プロジェクトがあるディレクトリでターミナルを開き、以下のコマンド
python -m venv venv
venv\Scripts\activate

ターミナル表示が　(venv) C:\Users\xxx　となればOK

# ライブラリインストール(初回のみ)
仮想環境内に以下のコマンドでインストール
pip install -r requirements.txt

# 環境変数設定
env_sample.pyをコピーし、env.pyにrenameしたファイルに環境変数を設定する

# 使用方法
venv環境でapp.pyを起動させる</br>