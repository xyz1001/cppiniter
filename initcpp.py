#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import argparse

project_path = ""
name = ""
project_type = ""

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
    print("[Debug]: Project path: %s, name: %s, type: %s" % (project_path, name, project_type))

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
        makeDir(os.path.join(project_path, "tests", "catch"))
    except PermissionError:
        print("[Error]: 创建目录失败，请检查权限")


def createTestFiles():
    try:
       shutil.copy(os.path.join("/home/zix/Project/init-cpp", "tests", "catch", "catch.hpp"), os.path.join(project_path, "tests", "catch"))
       shutil.copy(os.path.join("/home/zix/Project/init-cpp", "tests", "main.cpp"), os.path.join(project_path, "tests"))
    except Exception:
        print("[Warning]: 复制测试所需文件出错，可能是文件缺失或权限不足")

def createReadme():
    try:
        with open("README.md", 'w') as readme:
            readme.write("# %s" % name)
    except Exception:
        print("[Warning]: 创建README.md失败,请检查权限")

def createGitignore():
    try:
        shutil.copy(os.path.join("/home/zix/Project/init-cpp", "gitignore", "%s.gitignore" % project_type), 
                os.path.join(project_path, ".gitignore"));
    except Exception:
        print("[Warning]: 创建.gitignore文件失败，可能是文件缺失或权限不足")


if __name__ == "__main__":
    parseParameter()
    createDirs()
    createTestFiles()
    createReadme()
    createGitignore()
    
