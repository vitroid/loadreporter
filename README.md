# LoadReporter

計算機負荷をzeroconfで提供するデーモン

## クイックインストール

```bash
# PyPIからインストール（推奨）
pip install loadreporter

# ワンライナーでインストール（systemdサービスとして）
curl -sSL https://raw.githubusercontent.com/vitroid/loadreporter/main/install.sh | sudo bash

# より簡単なワンライナー（直接実行）
curl -sSL https://raw.githubusercontent.com/vitroid/loadreporter/main/install.sh | sudo bash -s

# または、手動でインストール
git clone https://github.com/vitroid/loadreporter.git
cd loadreporter
make install
```

## 使用方法

```bash
# 直接実行
python3 -m loadreporter.api

# または
loadreporter

# systemdサービスとして
sudo systemctl start loadreporter
sudo systemctl status loadreporter
```

## API

- `GET /v1/info` - システム情報を取得

## トラブルシューティング

サービスが起動しない場合は、ログを確認してください：
```shell
sudo journalctl -u loadreporter
```
