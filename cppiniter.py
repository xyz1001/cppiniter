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
import time
from docopt import docopt

DATA_INSTALL_DIR = "/usr/local/share/cppiniter/data"
VERSION = "1.0"
TMP_DIR = "/tmp/cppiniter"


class Project(object):
    def __init__(self, project_dir, project_name, build_system, is_lib):
        self.dir = project_dir
        self.name = project_name
        self.build_system = build_system
        self.is_lib = is_lib

    def __str__(self):
        return "name: %s\ndir: %s\nbuild system: %s\nlibrary: %s" % (
            self.dir, self.name, self.build_system, self.is_lib)

    def __repr__(self):
        return self.__str__()


class Generator(object):
    def generate(self, project):
        self.project = project

        self.__check_env()
        self.__copy_files()
        self.__generate_files()
        self.__create_file_tree()
        self.__clean()

    def __file_dir(self):
        return os.path.join(self.data_dir, self.project.build_system)

    def __check_env(self):
        bin_dir = os.path.split(os.path.realpath(__file__))[0]
        self.data_dir = os.path.join(bin_dir, "data")
        if not os.path.isdir(self.data_dir):
            self.data_dir = DATA_INSTALL_DIR
            if not os.path.isdir(self.data_dir):
                print("[Error]: 程序运行所需文件丢失，请尝试重新安装")
                exit(1)
        if not os.path.isdir(TMP_DIR):
            os.mkdir(TMP_DIR)
        if not os.path.isdir(self.project.dir):
            os.mkdir(self.project.dir)
        if os.listdir(self.project.dir):
            ok = input("目标文件夹%s不为空，删除该文件夹下所有内容并继续？（y/N）" % self.project.dir)
            if ok == "y" or ok == "Y":
                shutil.rmtree(self.project.dir)
                os.mkdir(self.project.dir)
            else:
                exit(-1)

    def __generate_files(self):
        sys.path.append(self.__file_dir())
        import template

        info = {
            "project_dir":
            self.project.dir,
            "project_name":
            self.project.name,
            "build_system":
            self.project.build_system,
            "is_lib":
            self.project.is_lib,
            "date_time":
            str(time.strftime("%Y-%m-%d %A %X %Z", time.localtime())),
            "version":
            VERSION
        }
        for (k, v) in template.FILES.items():
            content = pystache.render(v, info)
            with open(os.path.join(TMP_DIR, k), "w") as fout:
                fout.write(content)

    def __copy_files(self):
        files_dir = os.path.join(self.__file_dir(), "files")
        for i in os.listdir(files_dir):
            shutil.copy2(os.path.join(files_dir, i), os.path.join(TMP_DIR, i))

    def __create_file_tree(self):
        file_tree_path = os.path.join(self.__file_dir(), "file_tree.json")
        with open(file_tree_path, "r") as fin:
            file_tree = json.loads(fin.read())
        self.__create_tree(file_tree, self.project.dir)

    def __create_tree(self, file_tree, dest_dir):
        for (k, v) in file_tree.items():
            if k != "file":
                dir_path = os.path.join(dest_dir, k)
                os.mkdir(dir_path)
                self.__create_tree(v, dir_path)
            else:
                for (file_name, file_source) in v.items():
                    shutil.copy2(
                        os.path.join(TMP_DIR, file_source),
                        os.path.join(dest_dir, file_name))

    def __clean(self):
        shutil.rmtree(TMP_DIR)


def parse_args(args):
    project_dir = args["<dir>"]
    project_name = args["--name"]
    if args["--qmake"]:
        build_system = "qmake"
    else:
        build_system = "cmake"
    is_lib = args["--lib"]

    if project_dir is None:
        project_dir = "."
    project_dir = os.path.abspath(project_dir)
    if project_name is None:
        project_name = os.path.split(project_dir)[-1]
    return Project(project_dir, project_name, build_system, is_lib)


def main():
    args = docopt(__doc__, version="1.0")
    project = parse_args(args)
    gen = Generator()
    gen.generate(project)


if __name__ == "__main__":
    main()
