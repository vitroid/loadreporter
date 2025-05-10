#!/usr/bin/env python3

from setuptools import setup
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

def post_install():
    """Post-installation script"""
    # バイナリのパスを取得
    binary_path = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'loadreporter']).decode()
    for line in binary_path.split('\n'):
        if line.startswith('Location:'):
            location = line.split(':')[1].strip()
            break
    else:
        location = '/usr/local/lib/python3/dist-packages'
    
    # systemdサービスファイルの作成
    service_content = SYSTEMD_TEMPLATE.replace('LOADREPORTER_PATH', os.path.join(location, 'bin/loadreporter'))
    
    # サービスファイルのインストール
    os.makedirs('/etc/systemd/system', exist_ok=True)
    with open('/etc/systemd/system/loadreporter.service', 'w') as f:
        f.write(service_content)
    
    # avahiサービスファイルのインストール
    os.makedirs('/etc/avahi/services', exist_ok=True)
    with open('/etc/avahi/services/loadreporter.service', 'w') as f:
        f.write(AVAHI_SERVICE)
    
    # サービスの有効化と起動
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'loadreporter'])
    subprocess.run(['systemctl', 'start', 'loadreporter'])

setup(
    name='loadreporter',
    version='0.1.0',
    description='計算機負荷をzeroconfで提供するデーモン',
    author='Masakazu Matsumoto',
    author_email='vitroid@gmail.com',
    packages=[],
    install_requires=[
        'zeroconf',
        'fastapi',
        'uvicorn',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'loadreporter=api:main',
        ],
    },
    package_data={
        '': ['api.py'],
    },
    python_requires='>=3.8',
    include_package_data=True,
)

# インストール後に実行
if 'install' in sys.argv:
    post_install() 