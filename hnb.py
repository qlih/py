#!/usr/bin/env python3
# Encoding:UTF-8
# hnb.py hnbtl.cfg
#
#   hnb.*.txt 笔记的标题、标签加工。hnb = liH NoteBook。tl = title & labels
#   hnb的格式：UTF-8编码，第一个不是#开头的行是标题，以后每一个 # 开头的行都是一个子标题。
#   记录一下log，即到底有多少个 hnb 文件，

import glob
import math
import os
import re
import sys
import time

__author__ = 'qlih@qq.com'
__version__  = '0.31'

def get_paths(lpath="./"):  # ~/etc, /usr/local/etc, /var, ./
    cfgs =[]
    res =[]
    try:    # with
        f = open(os.path.join(lpath,'hnbtl.cfg') ,'r')
        cfgs=f.readlines()
        f.close()
    except Exception as e:
        res.append('./')    # 如果发生问题，就处理当前目录下的文件。这个设置是配置文件仅仅配置在程序目录下的一种逻辑，只有这样才能避免去执行太多的配置命令。
        return res

    # re1=re.compile('^#.*', re.I+re.U) # 都是unicode搜索，这里没有汉字，可以不用。
    # re2=re.compile('[/\\\]+',re.X+re.U) # re.X 为了增加可读性，忽略空格和’ # ’后面的注释
    # re3=re.compile('^~')
    # if result=re1.match(ltmp):

    for ltmp in cfgs:
        ltmp = ltmp.strip() # 处理~
        if re.search('^#.*', ltmp):
            continue
        if re.search('[/\\\]+', ltmp): # 需要有路径字符
                    # re.sub() todo 删除行中的注释
            if re.search('^~',ltmp):
                ltmp = os.path.expanduser(ltmp)
            res.append(ltmp)
        else:
            continue
    return res


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

        hf = 0 # hf head-flag／文件头的大标题标志
        res={}
        number = 0
        lbls={}
        lblcount =0
        for i in range(len(fls)):
            ltmp = fls[i].strip()
            # 可以用两个for循环，分别处理文件头和文件，可读性好些？
            if hf==0 and re.search('^[^#]',ltmp) != None: # find Title,第一个不是#开头的行
                hf=1
                f.write(ltmp) # Big Title
                stinfo = os.stat(fr)
                f.write(os.linesep+time.ctime(stinfo.st_atime))
                continue
            # *?a 匹配第一个出现的a，*后面的？表示非贪婪匹配。
            title, number = re.subn('^#[\s]*(.*)', '\g<1>', ltmp, 0)
            if number>0: # 找到一个标题
                if title in res:
                    res[title] = '{}({})'.format(res[title],i+1)
                else:
                    res[title]=i+1 # 行号
                #lbls = split(title)
                for lbs_idx in title.split():
                    if re.search('^[\d]+',lbs_idx): #刷掉 数字 开头的
                        continue
                    #elif re.search('^\.',lbs_idx): #'.'开头，unicode单字，或者是截取部分……
                    #    continue

                    if lbs_idx in lbls:
                        lbls[lbs_idx]+=1 #老标签，重复出现1次。
                    else:
                        lbls[lbs_idx]=1 #新标签，出现一次
                        lblcount+=1 #标签的总数
        # write labels
        f.write(os.linesep+'Labels: '+str(len(lbls))+os.linesep+os.linesep)
        for lbs_name in sorted(lbls):
        #for lbs_name in [(k, lbls[k]) for k in sorted(lbls.keys())]:
            f.write('{:>4} : {:>}'.format(lbls[lbs_name],lbs_name))
            f.write(os.linesep)
        f.write(os.linesep)

        # format programming show: 行宽 = 以10为底的对数
        ln_width=round(math.log(i,10))
        ln_cap=('LN# '+'%%0%dd'%(ln_width)+' # Titles: %d')%(0, len(res))
        ln_tem='{:>%d} # {}'%(ln_width+4)
        # 标题

        f.write(os.linesep+os.linesep+ln_cap+os.linesep+os.linesep)
        for title in sorted(res.keys()): # 输出按照标题排序
            f.write(ln_tem.format(res[title], title) + os.linesep)

        f.close()


if __name__ == '__main__':
    i =len(sys.argv)
    # print(len(sys.argv)) # shell 会把 *.* 里面的文件名都展开。
    if i>1: # 如果有参数，要从第一个文件开始计算，或者先装入一个列表。
        while i>1:
            hnb_tl(sys.argv[i-1]) # 参数要写成 '*.*'，否则shell会自动展开*.*，所以用循环
            i=i-1
    else:
        (filepath,scriptname) = os.path.split(sys.argv[0]) # 取配置文件路径
        res =get_paths(filepath)
        for ltmp in res:
            hnb_tl(os.path.join(ltmp, 'hnb.*.txt'))
