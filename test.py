#!/usr/bin/env python
#coding:utf8
import os
if __name__ == '__main__':
    path = 'C:\\Windows\\'
    list_dirs = os.walk(path)
    for root, dirs, files in list_dirs:
        print(root)