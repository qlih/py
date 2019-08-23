#!/usr/bin/env python3

# 把 Test目录： /Users/bxk/bxk.hot/prj.1.programmer/documents/gifa.crc32/0 下的 gif 文件
#	工作目录：/Volumn/bxk456/Class3/..../
#	改名为 crc32签字 的文件名，在 label 手工 标记完 之后，送入hash目录。

# usage:  $ python3 ../crc32marge2lib.py

import shutil
import glob
import shutil

__ver = 1 # 20190823

for fs in glob.glob('*.gif'):	# fs: file from; ft: file target
	# 取前两个字母，做 hash，用作子目录名字。
	# pt 是 path to
	pt = "../"+fs[:2]+"/"+fs
	shutil.move(fs, pt)	# 当前情况下一共240子目录, 已经建好了，不需要再建立了。所以不会出现移动文件异常。
