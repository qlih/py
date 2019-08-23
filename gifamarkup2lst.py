#!/usr/bin/env python3

# 从 c3lbl2gifa.txt 标注库 中 取出所有 gifa 文件，标准输出。

__ver = 1 # 20190822

def hashfn(fn):
	return fn[:2]+'/'+fn+'.gif'

def printfs(fs):
	for it in fs:
		print(hashfn(it))
	pass

fs=set() # files set
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

#print(fs)
print(len(fs))
# printfs(fs)
