#!/usr/bin/env python3
"""
查找标签
"""
# usage:  $ python3 ../search.py [defautl-label[,label]]
# vi ../c3lbl2gifa.txt

import sys
import glob

__ver=1 # 20190823

keys=set()
i =len(sys.argv)
# print(len(sys.argv)) # shell 会把 *.* 里面的文件名都展开。
if i>1: # 如果有参数，要从第一个文件开始计算，或者先装入一个列表。
	while i>1:
		keys.add(sys.argv[i-1]) # 参数要写成 '*.*'，否则shell会自动展开*.*，所以用循环
		i=i-1
#	print(keys)
else:
	print("Usage search key1 [key2]")

fs=set() # serch result files set
with open('c3lbl2gifa.txt', 'r', encoding='utf-8') as f:
	for line in f.readlines():
		line=line.strip()
		# 去掉标签、注释、过滤器
		if line[:1] in ['#','%','$']:
			continue
		# 取文件名
		buf=line.split(':')
		# 如果数据文件没有用":"分割，输出出错的行
		if len(buf) == 1:
			print(line)
			continue
		files= buf[0] # 得到“文件”，或者“系列文件”
		labels= buf[1] # 第0个是文件名，第1个是标签
		if keys<=set(labels.split(',')):	# 集合运算
			fs.add(files)	# 这里有 serial 没有展开
		'''
		这是 OR 关系
		for it in labels.split(','):	# 遍历列表
			if it in keys:
				for itf in files.split(','):	# 遍历列表
					fs.add(itf)
		'''
print(fs)
print(len(fs))
