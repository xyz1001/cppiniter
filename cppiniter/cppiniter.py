#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cppiniter init a cpp project struction

Usage:
    cppiniter [<dir>] [--name=<name>] [--lib]

Options:
    <dir>                   项目目录，默认为当前目录
    --name=<name>           项目名，默认为项目目录名
    --lib                   项目目标为C++库
"""

import os
import shutil
import inquirer
import pystache
from docopt import docopt

IGNORE_FILES = set([".git", "LICENSE"])


def install(args):
    ignores = []
    if args["is_lib"]:
        ignores.append("src/main.cpp")

    dir = os.path.dirname(os.path.realpath(__file__))
    shutil.copytree(os.path.join(dir, "files"),
                    args["project_dir"],
                    ignore=shutil.ignore_patterns(*ignores),
                    dirs_exist_ok=True)


def render(dir, args):
    for root, dirs, files in os.walk(dir):
        for i in files:
            path = os.path.join(root, i)
            with open(path, "r") as fin:
                content = fin.read()
            content = pystache.render(content, args)
            with open(path, "w") as fout:
                fout.write(content)
        for i in dirs:
            render(os.path.join(root, i), args)


def preprocess(args):
    project_dir = args["<dir>"]
    project_name = args["--name"]
    is_lib = args["--lib"]

    if project_dir is None:
        project_dir = "."
    project_dir = os.path.abspath(project_dir)
    if project_name is None:
        project_name = os.path.split(project_dir)[-1]
    if not os.path.isdir(project_dir):
        os.mkdir(project_dir)
    elif not set(os.listdir(project_dir)) <= IGNORE_FILES:
        tips = "目标文件夹%s不为空，删除该文件夹下所有内容并继续？" % project_dir
        correct = inquirer.confirm(tips, default=True)
        if correct:
            shutil.rmtree(project_dir)
            os.mkdir(project_dir)
        else:
            exit(-1)
    return {"project_name": project_name, "project_dir": project_dir, "is_lib": is_lib}


def main():
    args = docopt(__doc__, version="1.0")
    args = preprocess(args)
    install(args)
    render(args["project_dir"], args)


if __name__ == "__main__":
    main()
