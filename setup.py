#!/usr/bin/env python3

from setuptools import setup
import os
import subprocess
import sys

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
    with open('systemctl/loadreporter.tmpl') as f:
        template = f.read()
    service_content = template.replace('LOADREPORTER_PATH', os.path.join(location, 'bin/loadreporter'))
    
    # サービスファイルのインストール
    os.makedirs('/etc/systemd/system', exist_ok=True)
    with open('/etc/systemd/system/loadreporter.service', 'w') as f:
        f.write(service_content)
    
    # avahiサービスファイルのインストール
    os.makedirs('/etc/avahi/services', exist_ok=True)
    with open('avahi/loadreporter.service') as f:
        avahi_content = f.read()
    with open('/etc/avahi/services/loadreporter.service', 'w') as f:
        f.write(avahi_content)
    
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
    data_files=[
        ('/etc/systemd/system', ['systemctl/loadreporter.tmpl']),
        ('/etc/avahi/services', ['avahi/loadreporter.service']),
    ],
    python_requires='>=3.8',
)

# インストール後に実行
if 'install' in sys.argv:
    post_install() 