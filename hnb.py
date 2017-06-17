#!/usr/bin/env python3
#Encoding:UTF-8
# hnbtl.py
# hnb.*.txt 笔记的标题、标签加工。hnb = liH NoteBook。tl = title & labels
# hnb的格式：UTF-8编码，第一个不是#开头的行是标题，以后每一个 # 开头的行都是一个子标题。

# todo:
#   预设多个默认的工作目录，可以放在hnbtl.cfg里面
#   挂载到 hnb.*.txt 的菜单中。似乎是 菜单 的 Services

import glob
import math
import os
import re
import sys
import time

_ver = 'Ver 0.3'

def hnb_tl(hnb="hnb.*.txt"): # 大小写敏感
    for fr in glob.glob(hnb):
        if re.search('\.tl\.txt', fr, re.I): #忽略 *.tl.txt *.TL.TXT
            continue

        (filepath,tempfilename) = os.path.split(fr);
        (shotname,extension) = os.path.splitext(tempfilename);
        fw=os.path.join(filepath, shotname+'.tl'+extension)
        #try
        fls=[]
        f=open(fr,"r")
        fls = f.readlines() # 文件一般都不大，全都读入内存。
        f.close()

        f=open(fw,"w")

        # hf head-flag
        hf = 0
        res={}
        number = 0
        for i in range(len(fls)):
            ltmp = fls[i].strip()
            # 可以用两个for循环，分别处理文件头和文件
            if hf==0 and re.search('^[^#]',ltmp) != None: # find Title,第一个不是#开头的行
                hf=1
                f.write(ltmp) # Big Title
                stinfo = os.stat(fr)
                f.write(os.linesep+time.ctime(stinfo.st_atime))
                continue
            title, number = re.subn('^#[\s]*(.*)', '\g<1>', ltmp, 0)
            if number>0:
                if title in res:
                    res[title] = '{}({})'.format(res[title],i+1)
                else:
                    res[title]=i+1

        # format programming show: 行宽 = 以10为底的对数
        ln_width=round(math.log(i,10))
        ln_cap=('LN# '+'%%0%dd'%(ln_width)+' # Title')%(0)
        ln_tem='{:>%d} # {}'%(ln_width+4)

        f.write(os.linesep+os.linesep+ln_cap+os.linesep+os.linesep)
        for title in sorted(res.keys()): # 输出按照标题排序
            f.write(ln_tem.format(res[title], title) + os.linesep)

        f.close()
        # 加上 readonly

if __name__ == '__main__':
    if len(sys.argv)>1:
        hnb_tl(sys.argv[1])
    else:
        hnb_tl()
