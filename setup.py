#!/usr/bin/env python3

from setuptools import setup

setup(name='LoadReporter',
      version='0.1',
      description='Generate a long image strip from a train video',
      long_description=open('README.md', encoding='utf-8_sig').read(),
      long_description_content_type="text/markdown",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
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
       include_package_data=True,
      )
