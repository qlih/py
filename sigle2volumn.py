#!/usr/bin/env python3
   # -*- coding:utf-8 -*-
"""
package hnv
sigle2volumn.py (反过来的是volumn2single.py）
把每章一个文件的散的小说，合并成一卷。如果是多卷的，用另外的程序。
文件名是章节名，章节名和正文之间是Markdown的2级标题的段落分隔符，20个减号。
目录名就是卷名，卷名后面的分隔符是20个“=”
运行参数就是“卷”目录名。
Version 1.0.0     “烽火逃兵”测试过了。
todo: 
"""
import re
import os
import sys
import glob
class HNVSingle2Volumn():
    """ 
    单个文件合并到一个文件。
    """
    lines=[]
    def save(self):
        f = open(self.outfile, 'w')  #默认存盘的字符编码是utf8，mac下测试。
        for lc in self.lines:
            f.write(lc)
        #f.writelines(self.lines)
        f.close()
    def close(self):
        self.lines = []
    def parse(self):
        pass
    def setOutFile(self, setOutFile):
        self.outfile = setOutFile+'.txt'
        files = glob.glob(setOutFile+'/'+"*.txt")
        print(len(files))
        found = False
        for chn in range(1,10001):
            fre = '第'+str(chn)+'章'
            for i in range(0,len(files)): # if fre in files:
                if re.search(fre, files[i], re.I):
                    print('Found at '+fre)
                    found = True
                    break
            if found:
                break;
        self.lines.append(setOutFile+os.linesep)
        self.lines.append('===================='+os.linesep+os.linesep)
        for i in range(0,len(files)):
            fre = '第'+str(chn+i)+'章'
            chf = glob.glob(setOutFile+'/'+fre+"*.txt")
            if len(chf) >0 :
                filename = chf[0]
                #print(filename)
            else:
                # 遇到断章，退出。
                print('Lose: '+fre)
                return False
            # 取文件名
            (fpath,tempfilename) = os.path.split(filename);
            (shotname,extension) = os.path.splitext(tempfilename);
            #print(shotname)
            self.lines.append(shotname+os.linesep)
            self.lines.append('--------------------'+os.linesep)
            with open(filename,'r') as f:
                self.lines = self.lines + f.readlines()
            self.lines.append(os.linesep+os.linesep)
        print(fre) # 类似日志，打印最后一个文件的章节序号
        return True
# ver 1.0.0
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: sigle2volumn.py dir_name')
        sys.exit(1)
    myv = HNVSingle2Volumn()
    if myv.setOutFile(sys.argv[1]) is True:
        myv.parse()
        myv.save()
        myv.close()
    else:
        print('Read files error.')
        sys.exit(2)
