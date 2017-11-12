#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import shutil


def main():
    try:
        exe = "/usr/local/bin/cppiniter"
        if os.path.exists(exe):
            os.remove(exe)
    except PermissionError:
        print("请以超级用户权限执行该文件")
        exit(1)

    dest = "/usr/local/share/cppiniter"
    if os.path.exists(dest):
        shutil.rmtree(dest)


if __name__ == "__main__":
    main()
