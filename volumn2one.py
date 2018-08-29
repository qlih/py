#!/usr/bin/env python3
   # -*- coding:utf-8 -*-
"""
volumn2one.py
version: 0.01 用于把卷和题头合并成单一文件。
ver: 0.02 转为GBK/GB18030，体积比UTF8小。但可能会产生乱码。
"""
import re
import os
import sys
# ver 1.0.0
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: sigle2volumn.py dir_name')
        sys.exit(1)
        