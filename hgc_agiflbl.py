#!/usr/bin/env python3
# coding=utf-8
#   Encoding:UTF-8
#   hbc_agiflbl.py : blue clections, a-gif label for types.
# 统计 标签 个数，排序，并输出每个标签的实例数。
#   filename format: label_##-#|desc.gif

import glob
import re
import os
import sys

def count_lbl(filename="*.*"):
    agts={} # 用于保存标签的dict
    for index,fr in enumerate(glob.glob(filename)):
        (filepath,tempfilename) = os.path.split(fr);
        (shotname,extension) = os.path.splitext(tempfilename);

        if re.search('-\d+',shotname):#去掉带数字序号的文件 *-1*.gif
            continue
        lbl = re.sub('^([_a-zA-Z]+)(\d+).*','\g<1>', shotname) #得到标签
        if lbl in agts:
            agts[lbl]+=1
        else:
            agts[lbl]=1

    for lbl in sorted(agts.keys()): #排序输出
        print ('{0:>16}{1:>3}'.format(lbl,agts[lbl]))#{}{}是字段排列，可以不写字段序号，<^>是左中右对齐
    print('Labels: {} in {}'.format(len(agts),index))


if __name__ == '__main__':  # usage: hgc_agiflbl.py \*.*
    if len(sys.argv)>1:
        count_lbl(sys.argv[1])
    else:
        count_lbl()

