# LoadReporter

計算機負荷をzeroconfで提供するデーモン。

## インストール方法

### 最も簡単な方法（推奨）

```shell
sudo pip install loadreporter
```

### 開発版をインストールする場合

```shell
sudo pip install git+https://github.com/vitroid/loadreporter.git
```

### ソースからインストールする場合

```shell
git clone https://github.com/vitroid/loadreporter.git
cd loadreporter
sudo pip install .
```

### CentOS 7の場合

必要なパッケージをインストールします：
```shell
# EPELリポジトリの追加
sudo yum install epel-release

# 必要なパッケージのインストール
sudo yum install python38 python38-pip avahi-daemon

# pipのアップグレード
sudo python3.8 -m pip install --upgrade pip setuptools wheel
```

その後、上記のいずれかの方法でインストールしてください。

### サービスの有効化

インストール後、サービスを有効化して起動します：
```shell
sudo systemctl daemon-reload
sudo systemctl enable loadreporter
sudo systemctl start loadreporter
```

サービスの状態を確認します：
```shell
sudo systemctl status loadreporter
```

### Avahiの設定

インストール時に自動的にAvahiのサービスファイルが`/etc/avahi/services/`にコピーされます。
Avahiが有効になっている場合、他のマシンから自動的にサービスが検出されます。

CentOS 7でAvahiを有効にする場合：
```shell
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
```

## 使用方法

サービスが起動すると、以下のエンドポイントでAPIにアクセスできます：
- `http://localhost:8086/v1/info` - システム情報の取得

## トラブルシューティング

サービスが起動しない場合は、ログを確認してください：
```shell
sudo journalctl -u loadreporter
```
