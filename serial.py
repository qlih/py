#!/usr/bin/env python3
"""
把当前目录下的 gifa 建立成一个系列。交互输入标签，逗号风格。
不查重复（其他程序负责）。
"""
# usage:  $ python3 ../serial.py
# vi ../c3lbl2gifa.txt

import glob

__ver=1 # 20190823

serial=""
for fs in glob.glob('*.gif'):
	fs=fs.split('.')[0]
	if serial=="":
		serial=fs
	else:
		serial=serial+','+fs
serial=serial+":"
print(serial)
with open('../c3lbl2gifa.txt', 'a', encoding='utf-8') as f:
	f.write("\n")	# 新纪录
	f.write(serial)
f.close()
