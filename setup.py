#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from shutil import make_archive
import os
import sys

# 阻止安装时为.ycm_extra_conf.py生成pyc文件
sys.dont_write_bytecode = True

setup(
    name='cppiniter',
    version="1.0.0",
    description="C++项目脚手架",
    long_description="""用于提供C++项目开发环境的初始化""",
    keywords='c++ scaffolding',
    author='xyz1001',
    author_email='zgzf1001@gmail.com',
    url='https://github.com/xyz1001/cppiniter',
    license='MIT',
    packages=find_packages(exclude=['.ycm_extra_conf.py']),
    include_package_data=True,
    zip_safe=False,
    package_data={'cppiniter': ["files/*",
                                "files/.*", "files/**/*", "files/**/.*"]},
    install_requires=['pystache', 'docopt', 'inquirer'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={'console_scripts': [
        'cppiniter = cppiniter.cppiniter:main',
    ]},
)
