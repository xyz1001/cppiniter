# C++项目脚手架

该项目用于提供C++项目开发环境的初始化。特点为：

1. 使用 cmake 构建
2. 使用 conan 进行包管理
3. 使用 google 编码规范
4. 使用 catch2 作为单元测试
5. 提供了 vim/Youcompleteme 的支持

何为脚手架？见[脚手架是什么？](https://stackoverflow.com/questions/235018/what-is-scaffolding-is-it-a-term-for-a-particular-platform)

# 目录结构

```
/project

    - /build

      我们应该保持一棵干净的源码树，所有编译应该单独在这个目录进行，产生的
      object 文件也存在在这个目录。

      这个目录里面的东西，不应该上传到 gitlab 上。

    - /doc

      所有的文档应该放在这个目录下。

        - /examples 可选

          可以包含一个 examples 目录用于介绍 api 的接口使用。

    - /src

      这个目录下面存放项目的源码，包括 .cpp 文件和内部使用的 .h 文件

        - Makefile.am

          这个文件用于自动构建项目

    - /tests

      所有的测试文件应该放在这个目录下面

        - Makefile.am

          用于测试代码的自动构建

    - Makefile.am
    - configure.ac

      这两个文件用于 GNU 的 autotool 自动构建项目。其中 Makefile.am 中包含 src
      子目录和 tests 子目录。

    - README.md

      项目应该有一个 README.md 用来介绍这个项目。但是项目的编译、使用等文档应该
      放在 doc 目录下面
```

