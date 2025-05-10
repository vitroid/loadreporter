#!/usr/local/bin/python3

from setuptools import setup
import os

setup(name='LoadReporter',
      version='0.2',
      description='Generate a long image strip from a train video',
      long_description=open('README.md', encoding='utf-8_sig').read(),
      long_description_content_type="text/markdown",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Environment :: No Input/Output (Daemon)",
        ],
      author='Masakazu Matsumoto',
      author_email='vitroid@gmail.com',
      # url='https://github.com/vitroid/TrainScanner/',
      keywords=['loadreporter',],
      license='MIT',
      packages=[],
      install_requires=["zeroconf",
                        "fastapi",
                        "uvicorn"],
      entry_points = {
              'console_scripts': [
                  'loadreporter        = api:main',
              ]
          },
      data_files=[
          ('/etc/systemd/system', ['systemctl/loadreporter.service']),
          ('/etc/avahi/services', ['avahi/loadreporter.service']),
      ],
      include_package_data=True,
      python_requires='>=3.8',
      )
