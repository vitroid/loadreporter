#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# read version from loadreporter/__init__.py
try:
    with open("loadreporter/__init__.py", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                __version__ = line.split("=")[1].strip().replace('"', '').replace("'", "")
                break
        else:
            __version__ = "0.2.1"  # fallback
except Exception as e:
    print(f"Warning: Could not read version from loadreporter/__init__.py: {e}")
    __version__ = "0.2.1"  # fallback

setup(
    name='loadreporter',
    version=__version__,
    description='計算機負荷をzeroconfで提供するデーモン',
    author='Masakazu Matsumoto',
    author_email='vitroid@gmail.com',
    packages=['loadreporter'],
    install_requires=[
        'zeroconf',
        'fastapi',
        'uvicorn',
        'numpy',
        'netifaces',
    ],
    entry_points={
        'console_scripts': [
            'loadreporter=loadreporter.api:main',
        ],
    },
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
) 