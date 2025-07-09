#!/bin/bash

set -e

echo "LoadReporter インストールスクリプト"
echo "=================================="

# 必要なパッケージの確認
check_dependencies() {
    echo "依存関係を確認中..."
    
    # Python3の確認
    if ! command -v python3 &> /dev/null; then
        echo "エラー: python3 が見つかりません"
        echo "sudo apt-get install python3 python3-pip を実行してください"
        exit 1
    fi
    
    # gitの確認
    if ! command -v git &> /dev/null; then
        echo "エラー: git が見つかりません"
        echo "sudo apt-get install git を実行してください"
        exit 1
    fi
    
    echo "依存関係: OK"
}

# 一時ディレクトリの作成
setup_temp_dir() {
    echo "一時ディレクトリを作成中..."
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT
    cd $TEMP_DIR
}

# リポジトリのクローン
clone_repository() {
    echo "リポジトリをクローン中..."
    git clone https://github.com/vitroid/loadreporter.git
    cd loadreporter
}

# インストール実行
install_package() {
    echo "LoadReporterをインストール中..."
    make install
}

# メイン処理
main() {
    check_dependencies
    setup_temp_dir
    clone_repository
    install_package
    
    echo ""
    echo "インストール完了！"
    echo "サービス状態を確認中..."
    sudo systemctl status loadreporter --no-pager -l
    
    echo ""
    echo "使用方法:"
    echo "  sudo systemctl start loadreporter    # サービス開始"
    echo "  sudo systemctl stop loadreporter     # サービス停止"
    echo "  curl http://localhost:8086/v1/info  # APIテスト"
}

# スクリプト実行
main "$@" 