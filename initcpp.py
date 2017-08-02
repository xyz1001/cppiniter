#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import argparse

project_path = ""
name = ""
project_type = ""
src_dir = "/usr/local/share/initcpp"

def checkEnv():
    if os.path.split(os.path.realpath(__file__))[0] != "/usr/local/bin":
        print("[Error]: 请先运行install.py安装后再执行本程序")
        exit(1)
    if not os.path.exists(src_dir):
        print("[Error]: 程序运行所需文件丢失，请尝试重新安装")
        exit(1)

def parseParameter():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="项目所在目录路径，未指定则默认为当前目录")
    parser.add_argument("-n", "--name", help="项目名，若指定，则以该参数创建项目根目录，否则以项目所在目录名为项目名，以项目路径为项目根目录")
    parser.add_argument("-t", "--type", choices=["cmake", "Qt"], help="项目类型，包括cmake，Qt，默认为cmake类型")
    args = parser.parse_args();
    global project_path
    global name
    global project_type
    project_path = args.path
    if not os.path.isabs(project_path):
        project_path = os.path.abspath(project_path)
    if not os.path.isdir(project_path):
        print("[Error]: %s 不是一个合法的目录!" % project_path)
        exit(1)
    if args.name == None:
        name = os.path.basename(project_path)
    else:
        name = args.name
        project_path = os.path.join(project_path, name)
    if args.type == None:
        project_type = "cmake"
    else:
        project_type = args.type
    print("[Info]: Project path: %s, name: %s, type: %s" % (project_path, name, project_type))

def createDirs():
    def makeDir(dirPath):
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

    try:
        makeDir(os.path.join(project_path, "build"))
        makeDir(os.path.join(project_path, "doc", "example"))
        makeDir(os.path.join(project_path, "include"))
        makeDir(os.path.join(project_path, "lib"))
        makeDir(os.path.join(project_path, "src"))
        makeDir(os.path.join(project_path, "res"))
        makeDir(os.path.join(project_path, "tests"))
    except PermissionError:
        print("[Error]: 创建目录失败，请检查权限")



def createCMakeLists():
    def createTopCMakeLists():
        with open("CMakeLists.txt", 'w') as cmakelists:
            cmakelists.write("project (%s)\n\n" % name)
            cmakelists.write("cmake_minimum_required (VERSION 2.8)\n\n")
            cmakelists.write("add_subdirectory (src)\n")
            cmakelists.write("add_subdirectory (tests)\n")

    def createSrcCMakeLists():
        with open(os.path.join("src","CMakeLists.txt"), 'w') as cmakelists:
            cmakelists.write("add_executable (main main.cpp)\n\n")
            cmakelists.write("# add_library (helloworld helloworld.cpp)\n\n")
            cmakelists.write("# target_link_libraries (main helloworld)\n")

    def createTestsCMakeLists():
        with open(os.path.join("tests","CMakeLists.txt"), 'w') as cmakelists:
            cmakelists.write("include_directories (${PROJECT_SOURCE_DIR}/src)\n")
            cmakelists.write("link_directories (${PROJECT_SOURCE_DIR}/src)\n\n")
            cmakelists.write("add_executable (catch main.cpp test.cpp)\n\n")
            cmakelists.write("# target_link_libraries (catch helloworld)\n")

    try:
        pass
    except Exception:
        print("[Error]: 创建CMakeLists.txt文件失败")
    createTopCMakeLists()
    createSrcCMakeLists()
    createTestsCMakeLists();


def createBaseFiles():
    try:
        shutil.copy(os.path.join(src_dir, "main.cpp"),
                os.path.join(project_path, "src", "main.cpp"));
    except Exception:
        print("[Warning]: 复制main.cpp文件失败，可能是文件缺失或权限不足")

    try:
       shutil.copytree(os.path.join(src_dir, "catch"), os.path.join(project_path, "tests", "catch"))
    except Exception:
        print("[Warning]: 复制catch.hpp出错，可能是文件缺失或权限不足")
        raise
    try:
        with open(os.path.join(project_path, "tests", "main.cpp"), 'w') as test_main:
                test_main.write("#define CATCH_CONFIG_MAIN\n")
                test_main.write("#include \"catch/catch.hpp\"\n")
                test_main.close()
        with open(os.path.join(project_path, "tests", "test.cpp"), 'w') as test_main:
                test_main.write("#include \"catch/catch.hpp\"\n")
                test_main.close()
    except Exception:
        print("[Waring]: 测试文件main.cpp创建失败")
        raise

def createReadme():
    try:
        with open("README.md", 'w') as readme:
            readme.write("# %s" % name)
    except Exception:
        print("[Warning]: 创建README.md失败,请检查权限")

def createGitignore():
    try:
        shutil.copy(os.path.join(src_dir, "gitignore", "%s.gitignore" % project_type.lower()), 
                os.path.join(project_path, ".gitignore"));
    except Exception:
        print("[Warning]: 生成.gitignore文件失败，可能是文件缺失或权限不足")


if __name__ == "__main__":
    checkEnv()
    parseParameter()
    createDirs()
    createBaseFiles()
    createCMakeLists()
    createReadme()
    createGitignore()
    
