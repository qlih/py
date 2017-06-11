#!/usr/bin/env python3
#Encoding:UTF-8
# hnbtl.py
# hnb.*.txt 笔记的标题、标签加工。hnb = liH NoteBook。tl = title & labels
# hnb的格式：UTF-8编码，第一个不是#开头的行是标题，以后每一个 # 开头的行都是一个子标题。

# todo:
#   命令行匹配
#   * 匹配
#   行排序，没用！(用参数解决）因为不方便查找，只有在编辑笔记，合并、分解标题时有用。
#   预设多个默认的工作目录，可以放在hnbtl.cfg里面
#   挂载到 hnb.*.txt 的菜单中。似乎是 菜单 的 Services

import re
import time
import glob
import os

def hnb_tl(hnb="hnb.*.txt"):
    for fr in glob.glob(hnb):
        if re.search('.tl.txt', fr):
            continue

        (filepath,tempfilename) = os.path.split(fr);
        (shotname,extension) = os.path.splitext(tempfilename);
        fw=shotname+'.tl'+extension
        #try
        fls=[]
        f=open(fr,"r")
        fls = f.readlines()
        f.close()

        f=open(fw,"w")

        i = 0
        cn = ""

        # hf head-flag
        hf = 0

        number = 0
        while i<len(fls):
            ltmp = fls[i].strip()
            if hf==0 and re.search('^[^#]',ltmp) != None: # find Title,第一个不是#开头的行
                hf=1
                f.write(ltmp)
                f.write("\n版本: "+time.strftime('%Y-%m-%d',time.localtime(time.time()))+"\n\n")
                continue
            cn, number = re.subn('^#[ \t]*(.*)', '# \g<1>', ltmp, 0)
            if number>0:
                f.write(cn+"\n")
            i = i+1


        f.close()

if __name__ == '__main__':
    hnb_tl()
