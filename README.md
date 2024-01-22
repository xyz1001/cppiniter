# C++项目脚手架

该项目用于提供C++项目开发环境的初始化。特点为：

1. 使用 cmake 构建
2. 使用 conan2 进行包管理
3. 使用 google 编码规范
4. 使用 doctest 作为单元测试
4. 使用 clang-format 作为格式化工具
4. 使用 clang-tidy 作为静态代码检查工具

何为脚手架？见[脚手架是什么？](https://stackoverflow.com/questions/235018/what-is-scaffolding-is-it-a-term-for-a-particular-platform)

## 安装

```
pip3 install cppiniter
```

## 使用

```
Usage:
    cppiniter [<dir>] [--name=<name>] [--lib]

Options:
    <dir>                   项目目录，默认为当前目录
    --name=<name>           项目名，默认为项目目录名
    --lib                   项目目标为C++库
```

## 目录结构

```
project
│
├── .clang-format # clang-format 格式化配置

├── .clang-tidy # clang-tidy 静态代码检查配置
│
├── .gitignore # git 忽略文件
│
├── CMakeLists.txt # 顶层 CMake 构建脚本
│
├── CMakeSettings.json # Visual Studio CMake 配置
│
├── conanfile.py # conan 包依赖配置
│
├── README.md # 用来介绍这个项目
│
├── src # 存放项目的源码，包括 .cpp 文件和 .h 文件
│   │
│   ├── CMakeLists.txt
│   │
│   └── main.cpp
│
├── test # 所有的单元测试文件应该放在这个目录下面
│   │
│   ├── CMakeLists.txt
│   │
│   └── main.cpp # 加快doctest的编译速度
│
├── doc # 文档保存目录
│
└── build # 我们应该保持一棵干净的源码树，所有编译动作应该单独在这个目录进行。这个目录应加入gitignore
    │
    └── install # 在没有指定安装目录时默认安装目录，避免安装到系统目录。
