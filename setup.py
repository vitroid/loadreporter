#!/usr/bin/env python3

from setuptools import setup, find_packages
import os
import subprocess
import sys

# systemdサービスファイルのテンプレート
SYSTEMD_TEMPLATE = """[Unit]
Description=Load Reporter API Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=LOADREPORTER_PATH
Restart=always
RestartSec=10
Environment=PORT=8086

[Install]
WantedBy=multi-user.target
"""

# avahiサービスファイルの内容
AVAHI_SERVICE = """<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">Load Reporter</name>
  <service>
    <type>_http._tcp</type>
    <port>8086</port>
  </service>
</service-group>
"""

def run_command(cmd, error_msg):
    """コマンドを実行し、エラーがあればメッセージを表示"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {error_msg}")
            print(f"Command: {' '.join(cmd)}")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error: {error_msg}")
        print(f"Exception: {str(e)}")
        return False

def post_install():
    """Post-installation script"""
    print("Starting post-installation process...")
    
    # バイナリのパスを取得
    try:
        binary_path = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'loadreporter']).decode()
        for line in binary_path.split('\n'):
            if line.startswith('Location:'):
                location = line.split(':')[1].strip()
                break
        else:
            location = '/usr/local/lib/python3/dist-packages'
        print(f"Package location: {location}")
    except Exception as e:
        print(f"Error getting package location: {str(e)}")
        return
    
    # systemdサービスファイルの作成
    service_content = SYSTEMD_TEMPLATE.replace('LOADREPORTER_PATH', os.path.join(location, 'bin/loadreporter'))
    print(f"Service file content:\n{service_content}")
    
    # サービスファイルのインストール
    try:
        os.makedirs('/etc/systemd/system', exist_ok=True)
        with open('/etc/systemd/system/loadreporter.service', 'w') as f:
            f.write(service_content)
        print("Service file installed successfully")
    except Exception as e:
        print(f"Error installing service file: {str(e)}")
        return
    
    # avahiサービスファイルのインストール
    try:
        os.makedirs('/etc/avahi/services', exist_ok=True)
        with open('/etc/avahi/services/loadreporter.service', 'w') as f:
            f.write(AVAHI_SERVICE)
        print("Avahi service file installed successfully")
    except Exception as e:
        print(f"Error installing avahi service file: {str(e)}")
        return
    
    # サービスの有効化と起動
    if not run_command(['systemctl', 'daemon-reload'], "Failed to reload systemd"):
        return
    print("Systemd daemon reloaded")
    
    if not run_command(['systemctl', 'enable', 'loadreporter'], "Failed to enable service"):
        return
    print("Service enabled")
    
    if not run_command(['systemctl', 'start', 'loadreporter'], "Failed to start service"):
        return
    print("Service started")
    
    # サービスの状態を確認
    if not run_command(['systemctl', 'status', 'loadreporter'], "Failed to get service status"):
        return
    
    print("Post-installation completed successfully!")

# エントリーポイントスクリプトのテンプレート
ENTRY_POINT_TEMPLATE = """#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
from loadreporter.api import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
"""

setup(
    name='loadreporter',
    version='0.1.0',
    description='計算機負荷をzeroconfで提供するデーモン',
    author='Masakazu Matsumoto',
    author_email='vitroid@gmail.com',
    packages=['loadreporter'],
    install_requires=[
        'zeroconf',
        'fastapi',
        'uvicorn',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'loadreporter=loadreporter.api:main',
        ],
    },
    python_requires='>=3.6',
)

# インストール後に実行
if 'install' in sys.argv:
    post_install() 