#!/usr/bin/env python3
#Encoding:UTF-8
# lnb_tl.py
# hnb.*.txt 笔记的标题、标签加工。hnb = liH NoteBook。tl = title & labels
# hnb的格式：UTF-8编码，第一个不是#开头的行是标题，以后每一个 # 开头的行都是一个子标题。

# todo:
#   命令行匹配
#   * 匹配
#   行排序，没用！因为不方便查找，只有在编辑笔记，合并、分解标题时有用。
#

import re
import time

# fr = "hnb.*.txt"

#fr = "hnb.D50拍照.txt"
#fw = "hnb.D50拍照.tl.txt"

fr = "hnb.计算机笔记2017.txt"
fw = "hnb.计算机笔记2017.tl.txt"

f=open(fr,"r")
fls = f.readlines()
f.close()

f=open(fw,"w")

i = 0
cn =""
#time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

# hf head-flag
hf =0

number = 0

while i<len(fls):
    ltmp = fls[i].strip()
    if hf==0 and re.search('^[^#]',ltmp) != None: # find Title,第一个不是#开头饿行
        hf=1
        f.write(ltmp)
        f.write("\nVer: "+time.strftime('%Y-%m-%d',time.localtime(time.time()))+"\n\n")
        continue
    else:
        pass
    cn, number = re.subn('^#[ \t]*(.*)', '# \g<1>', ltmp, 0)
    if number>0:
        f.write(cn)
        f.write('\n')
    i = i+1

f.close()
