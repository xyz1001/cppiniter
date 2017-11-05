#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cppiniter init a cpp project struction

Usage:
    cppiniter [<dir>] [--name=<name>] [--cmake|--qmake] [--lib]

Options:
    <dir>                   项目目录，默认为当前目录
    --name=<name>           项目名，默认为项目目录名
    --qmake                 使用qmake进行构建，默认使用CMake作为构建系统
    --lib                   项目目标为C++库
"""

import os
import shutil
import json
import sys
import pystache
from datetime import datetime
from docopt import docopt

cppiniter_dir = ""
VERSION = "1.0"
TMP_DIR = "/tmp/cppiniter"

class Project(object):
    def __init__(self, project_dir, project_name, build_system, is_lib):
        self.dir = project_dir
        self.name = project_name
        self.build_system = build_system
        self.is_lib = is_lib
        self.data_file_dir = os.path.join(cppiniter_dir, "data", self.build_system)

    def __str__(self):
        return "name: %s\ndir: %s\nbuild system: %s\nlibrary: %s"%(self.dir,self.name, self.build_system, self.is_lib)

    def __repr__(self):
        return self.__str__()

def checkEnv(project_dir):
    cppiniter_dir = os.path.split(os.path.realpath(__file__))[0]
    if not os.path.isdir(os.path.join(cppiniter_dir, "data")):
        cppiniter_dir = "/usr/local/share/cppiniter"
        if not os.path.isdir(os.path.join(cppiniter_dir, "data")):
            print("[Error]: 程序运行所需文件丢失，请尝试重新安装")
            exit(1)
    if not os.path.isdir(TMP_DIR):
        os.mkdir(TMP_DIR)
    if not os.path.isdir(project_dir):
        os.mkdir(project_dir)
    if os.listdir(project_dir):
        ok = input("目标文件夹%s不为空，删除该文件夹下所有内容并继续？（y/N）"%project_dir)
        if ok == "y" or ok == "Y":
            shutil.rmtree(project_dir)
            os.mkdir(project_dir)

def parseArgs(args):
    project_dir = args["<dir>"]
    project_name = args["--name"]
    if args["--qmake"]:
        build_system = "qmake"
    else:
        build_system = "cmake"
    is_lib = args["--lib"]

    if project_dir == None :
        project_dir = "."
    project_dir = os.path.abspath(project_dir)
    if project_name == None:
        project_name = os.path.split(project_dir)[-1]
    return Project(project_dir, project_name, build_system, is_lib)

def generateFiles(project) :
    sys.path.append(project.data_file_dir)
    import template

    info = {"project_dir": project.dir,
            "project_name":project.name,
            "build_system":project.build_system,
            "is_lib":project.is_lib,
            "date_time":str(datetime.now()),
            "version": VERSION};
    for (k,v) in template.FILES.items():
        content = pystache.render(v, info)
        with open(os.path.join(TMP_DIR,k), "w") as fout:
                fout.write(content)

def copyFiles(project) :
    files_dir = os.path.join(project.data_file_dir,"files")
    for i in os.listdir(files_dir):
        shutil.copy2(os.path.join(files_dir, i), os.path.join(TMP_DIR, i))

def ParseFileTree(project):
    file_tree_path = os.path.join(project.data_file_dir,  "file_tree.json")
    with open(file_tree_path, "r") as fin:
        file_tree = json.loads(fin.read())
    return file_tree

def CreateTree(file_tree, dest_dir):
    for (k, v) in file_tree.items():
        if k != "file":
            dir_path = os.path.join(dest_dir, k)
            os.mkdir(dir_path)
            CreateTree(v, dir_path)
        else:
            for (file_name,file_source) in v.items():
                shutil.copy2(os.path.join(TMP_DIR, file_source), os.path.join(dest_dir, file_name))

def Clean():
    shutil.rmtree(TMP_DIR)

if __name__ == "__main__":
    args = docopt(__doc__, version="1.0")
    project = parseArgs(args)
    checkEnv(project.dir)
    copyFiles(project)
    generateFiles(project)
    file_tree = ParseFileTree(project)
    CreateTree(file_tree, project.dir)
    Clean()
