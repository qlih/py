#!/usr/bin/env python3
"""
把当前目录下的 gifa 添加为没标签的记录，然后用 TxT 编辑器 手工添加标签。
可选参数是 default 标签
"""
# usage:  $ python3 ../append.py [defautl-label[,label]]
# vi ../c3lbl2gifa.txt

import sys
import glob

__ver=1 # 20190823

lbl=''
if len(sys.argv)>1:
	lbl=sys.argv[1]

# 取 文件表, 查重复
# lib=getlst('../c3lbl2gifa.txt')

with open('../c3lbl2gifa.txt', 'a', encoding='utf-8') as f:
	files = sorted(glob.glob('*.gif'))
	# import os
	# sorted(glob.glob('*.png'), key=os.path.getmtime)
	# sorted(glob.glob('*.png'), key=os.path.getsize)
	
	for fs in files:
		f.write("\n")	# 新纪录
		f.write(fs.split('.')[0]+":"+lbl)
f.close()
