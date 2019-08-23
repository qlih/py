#!/usr/bin/env python3

# 把 Test目录： /Users/bxk/bxk.hot/prj.1.programmer/documents/gifa.crc32/0 下的 gif 文件
#	工作目录：/Volumn/bxk456/Class3/..../
#	改名为 crc32签字 的文件名，并 不 送入hash目录，送入目录用 ../crc32marge2lib.py。

# usage:  $ python3 ../crc32tmpdbcreate.py

import os
import glob
from zlib import crc32

__ver = 2 # 20190822


# 为了查重复, 先读入 list 文件【变成函数】
fd=set() # files set, gifa filename from list file.
with open('../c3lbl2gifa.txt', 'r', encoding='utf-8') as f:
	for line in f.readlines():
		line=line.strip()
		# 去掉标签、注释、过滤器
		if line[:1] in ['#','%','$']:
			continue
		# 取文件名
		files = line.split(':')[0] # 得到“文件”，或者“系列文件”
		# 展开“系列文件”。冒号是系列文件的分隔符，暂时不考虑‘空’文件
		for it in files.split(','):	# 遍历列表
			if it in fd:
				print("Warning, dupfile: " + line) # 重复定义不好，但不算错误。
			fd.add(it)

# print(fd)
print(len(fd))
# printfs(fd)

# 主流程
for fs in glob.glob('*.gif'):	# fs: file from; ft: file target
	with open(fs, 'rb') as f:
		ft = hex(crc32(f.read()))	# 转成 7-8位 16进制整数。
	fl = ft
	ft = ft[2:] + ".gif" # 去掉 “0x”, 然后构成 新的文件名。
	os.rename(fs,ft)

	# 取前两个字母，做 hash，用作子目录名字。
	pt = ft[:2]	# pt 是 path to
	pt = "../"+pt
	# 子目录不存在，就建立子目录，最多建立 15×16=240个子目录，没有0字头。
	if not os.path.exists(pt) :
		 os.makedirs(pt)
	# 去除重复文件
	if os.path.exists(pt+"/"+ft):
		if os.path.getsize(ft) == os.path.getsize(pt+"/"+ft):
			os.remove(ft)	# 文件存在，且文件长度一致，判断是重复文件，删掉。
		else:
			print("Error: "+ft+" exist.")
		continue
	# 在 list 文件中再查找一遍重复
	if fl in fd:
		print("Error: "+fl+" exist.")

