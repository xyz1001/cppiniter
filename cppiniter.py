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



if __name__ == "__main__":
    checkEnv()
    parseParameter()
    createDirs()
    createBaseFiles()
    createCMakeLists()
    createReadme()
    createGitignore()
    
