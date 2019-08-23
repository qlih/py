#!/usr/bin/env python3

# 从 c3lbl2gifa.txt 标注库 中 取出所有 标签，标准输出。

__ver = 1 # 20190822

lblc={} # lbl 的 counter，用字典。
with open('c3lbl2gifa.txt', 'r', encoding='utf-8') as f:
	for line in f.readlines():
		line=line.strip()
		# 去掉标签、注释、过滤器
		if line[:1] in ['#','%','$']:
			continue
		# 取标签
		labels = line.split(':')[1] # 第一个是文件名，第二个是标签
		# 展开“系列标签”。冒号是系列的分隔符，暂时不考虑‘空’标签。
		for it in labels.split(','):	# 遍历列表
			if lblc.__contains__(it):	# python2 用 .has_key(key)
				# 标签的引用次数+1
				lblc[it]=lblc[it]+1
			else:
				lblc[it]=1
				pass
# print(lblc)
# 删除没有使用过的。或者打印一个文件。
lblo={}
lbl1={}
for it in lblc:
	if lblc[it]>1:
		lblo[it]=lblc[it]
	if lblc[it]==1:
		lbl1[it]=lblc[it]
	pass
#	print(it)
print(lblo) # > 1
print(str(len(lblo)) + '/' + str(len(lblc)) + ", " + str(len(lbl1)) + " has 1 instance.")
print(lbl1) # == 1


# 同义词的一致化