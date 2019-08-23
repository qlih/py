#!/usr/bin/env python3
#检查数据文件和库的对应关系： c3lbl2gifa.txt /Volumes/classic3/storage.x.a-gif.crc32lib

# 取 gifa 库里的文件列表，对照 标签“标记”表。
# gifa lst sync lbl

import os
import glob

__ver = 1 # 20190822

fd=set() # gifa filename list from dir
for h in glob.iglob('??',recursive=True): # h hash的字头2字母
	if os.path.isdir(h):
		for it in glob.iglob(h+'/*.gif',recursive=True):
			if it[:2] == it[3:5]:
				it = it[3:]
				if it in fd:
					print("Warning: dupfile: " + it) # 重名, 放错目录时重复了。
				else:
					fd.add(it)	# (暂时)保留 .gif
			else:
				# 一般来说是 copy/move 文件时搞错了
				print("Warning: file stored position error " + it)
		pass

#print(fd)
print(len(fd))

fs=set() # files set, gifa filename from list file.
with open('c3lbl2gifa.txt', 'r', encoding='utf-8') as f:
	for line in f.readlines():
		line=line.strip()
		# 去掉标签、注释、过滤器
		if line[:1] in ['#','%','$']:
			continue
		# 取文件名
		files = line.split(':')[0] # 得到“文件”，或者“系列文件”
		# 展开“系列文件”。冒号是系列文件的分隔符，暂时不考虑‘空’文件
		for it in files.split(','):	# 遍历列表
			if it in fs:
				print("Warning, dupfile: " + line) # 重复定义不好，但不算错误。
			fs.add(it)

# print(fs)
print(len(fs))
# printfs(fs)

# 开始比较，看磁盘中的文件是否都在lbl里了，列出没列入的

for it in fd:
	# 去掉 .gif
	it = it.split('.')[0]
	if it in fs:
		continue
	else:
		print("Error: lst file missing " + it)

# 倒查一遍，列出 磁盘中的文件 比 列表 少了多少。
for it in fs:
	it = it + '.gif'
	if it in fd:
		continue
	else:
		print("Error: disk file missing " + it)
