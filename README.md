# Init CPP
C++项目初始化工具，用于自动创建一个统一的C++软件项目的初始目录和文件,基于[荣飞哥](https://github.com/zhaohuaxishi)的CPDS(CPP Project Directory Structure)项目的启发而开发，详情见[`cpds.md`](./cpds.md)。

# C++项目结构规范

```
projetc/
├── build
├── CMakeLists.txt
├── dev
│   ├── bin
│   ├── include
│   └── lib
├── doc
├── README.md
├── src
│   └──CMakeLists.txt
└── test
    └── CMakeLists.txt
```

> - `project`
> 项目文件夹
>  - `build/`
>  我们应该保持一棵干净的源码树，所有编译应该单独在这个目录进行，产生的object文件也存在在这个目录。这个目录里面的东西，不应该上传到git仓库上。
>  - `CMakeLists.txt`
>  这两个文件用于`cmake`自动构建项目，包含`src`子目录和`tests`子目录。
>  - `doc/`
>  所有的文档应该放在这个目录下。
>    - `examples/`(可选)
>    可以包含一个`examples`目录用于介绍api的接口使用。
>  - `dev/`
>  外部库目录
>    - `lib/`
>    外部库库文件目录
>    - `include/`
>    外部库头文件目录
>    - `bin/`
>    外部库动态链接文件目录
>  - `README.md`
>  项目应该有一个`README.md`用来介绍这个项目。但是项目的编译、使用等文档应该放在`doc`目录下面
>  - `src/`
>  这个目录下面存放项目的源码，包括`.cpp`文件和内部使用的`.h`文件
>    - `CMakeLists.txt`
>   这个文件用于自动构建项目
>  - `test/`
>   所有的测试文件应该放在这个目录下面，本项目默认使用[`Catch`](https://github.com/catchorg/Catch2)进行测试
>    - `CMakeLists.txt`
>   用于测试代码的自动构建
