#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='cppiniter',
    version="1.0.7",
    description="C++项目脚手架",
    long_description="""用于提供C++项目开发环境的初始化""",
    keywords='c++ scaffolding',
    author='xyz1001',
    author_email='zgzf1001@gmail.com',
    url='https://github.com/xyz1001/cppiniter',
    license='MIT',
    include_package_data=True,
    package_dir={
        'cppiniter': 'cppiniter',
    },
    packages=[
        'cppiniter',
    ],
    install_requires=['pystache', 'docopt', 'inquirer'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={'console_scripts': [
        'cppiniter = cppiniter.cppiniter:main',
    ]},
)
