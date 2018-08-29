#!/usr/bin/env python3
   # -*- coding:utf-8 -*-
"""
volumn2single.py(反过来的是 sigle2volumn.py）
version: 0.01 用于把卷拆开
"""
import re
import os
import sys
# ver 1.0.0
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: sigle2volumn.py dir_name')
        sys.exit(1)
