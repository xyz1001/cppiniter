#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""cppiniter init a cpp project struction

Usage:
    cppiniter [<dir>] [--name=<name>] [--exe]

Options:
    <dir>                   项目目录，默认为当前目录
    --name=<name>           项目名，默认为项目目录名
    --exe                   项目目标为C++应用程序，默认为库
"""

import os
import sys
import shutil
import inquirer
import pystache
import subprocess
import platform
from docopt import docopt
from datetime import datetime

IGNORE_FILES = set([".git", "LICENSE"])
EMPTY_DIR = ("build", "doc")
RENAME_FILES = {"src/project_name/project_name.h": "src/project_name/{{project_name}}.h", "src/project_name/project_name.cpp": "src/project_name/{{project_name}}.cpp", "src/project_name": "src/{{project_name}}"}


def install(args):
    ignores = ["*.pyc", "__pycache__"]

    if args["is_exe"]:
        ignores.append("example")
        ignores.append("test")

    dir = os.path.dirname(os.path.realpath(__file__))
    shutil.copytree(os.path.join(dir, "files"),
                    args["project_dir"],
                    ignore=shutil.ignore_patterns(*ignores),
                    dirs_exist_ok=True)
    for i in EMPTY_DIR:
        os.mkdir(os.path.join(args["project_dir"], i))
    for key, value in RENAME_FILES.items():
        src_path = os.path.join(args["project_dir"], key)
        dst_path = os.path.join(args["project_dir"], pystache.render(value, args))
        os.rename(src_path, dst_path)

    if args["is_exe"]:
        shutil.rmtree(os.path.join(args["project_dir"], "src", args["project_name"]))
    else:
        os.remove(os.path.join(args["project_dir"], "src", "main.cpp"))
        os.remove(os.path.join(args["project_dir"], "src", "version.h.in"))


def render(dir, args):
    for root, dirs, files in os.walk(dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for i in files:
            path = os.path.join(root, i)
            with open(path, "r") as fin:
                content = fin.read()
            content = pystache.render(content, args)
            with open(path, "w") as fout:
                fout.write(content)


def preprocess(args):
    project_dir = args["<dir>"]
    project_name = args["--name"]
    is_exe = args["--exe"]
    author = subprocess.check_output(["git", "config", "--get", "user.name"]
                                     ).decode(sys.stdout.encoding).strip()
    email = subprocess.check_output(["git", "config", "--get", "user.email"]
                                    ).decode(sys.stdout.encoding).strip()
    date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    if author is None:
        author = os.getlogin()

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

    project_name_uppercase = project_name.upper()
    project_name_camelcase = ''.join(project_name.title() for word in project_name.split('_'))
    return {"project_name": project_name, "project_name_uppercase": project_name_uppercase, "project_name_camelcase": project_name_camelcase, "project_dir": project_dir, "is_exe": is_exe, "date_time": date_time, "author": author, "email": email}


def execute(dir):
    subprocess.run(["conan", "install", "..", "-s:h", "build_type=Debug", "--build", "missing"], cwd=os.path.join(dir, "build"))
    subprocess.run(["cmake","--preset=conan-debug"], cwd=dir)


def main():
    args = docopt(__doc__, version="1.0")
    args = preprocess(args)
    install(args)
    render(args["project_dir"], args)
    execute(args["project_dir"])


if __name__ == "__main__":
    main()
