#!/usr/bin/env python3
# Encoding:UTF-8
#	hnv_unwrap.py
#	算法描述：
#	utf-8格式读入
#		测量长度，一般字符算1，CJK算2，各行的长度都统计后，排序。相对多字符（比如多余56个ascii），最长的行，如果不多，则可以忽略，看某一个宽度，如70字宽的行是不是很多。
#		如果确定是 wrap 的格式，则
#			干掉折行，不论结尾的地方是否有标点；

__author__ = 'qlih@qq.com'
__version__ = '0.04'

import re
import os
import sys
import codecs

'''
检测，检测内码；
'''
class detect():
    def codeType(self):
        pass
    def stage(self):
        return 0
'''
    stage标准：
    stage = 0 # 可读，目前是人工。
    stage = 1 
        utf-8
        第一行是标题，长度有限（16中文字符，或者8个英文单词）
        第一行没有“中文句号”
    stage = 3
        文章结束 = ‘■’  0x25a0
    stage = 4
        确定章节分割和格式
        只有中文双引号
        作者注视符号：ps/㊟
        时间地点分割行，四组：5/3 4/3 4/3 4/3= '　　　　　＊＊＊　　　　＊＊＊　　　　＊＊＊　　　　＊＊＊'
'''
class labelDefine():
    blankLine=False #行与行之间，用空行分割时 = true
    # 全角/半角
    fullSpace=False #出现了全角空格 = true
    fullDigital = False # 出现了全角数字 = true
    fullAlpha = False # 全角“英文”字母
    # 标点符号
    taipei0 = False    # 台北的引号
    taipei0Pire = False # 台北的引号成对出现了 = true
    p0  = False # 冒号和引号匹配问题，半角冒号配全角引号或者相反 = true
    p1 = False # 出现了无法配对的半角双引号

    # 行头部空格
    spaceTotal = 0 # 行头出现的无用空格数量。一般是半角空格。
    # 章节定义
    spaceCharpter = False # 章节前面有空格
    charpterFormat = False # 章节格式符合规定： \n\n第(\d+)章|节 .*\n\n
    # 文章结束符号
    endchar = False   # \u, '■'；在0.03版时，会把这个结束符号前面的换行符号删掉。

    pass

class loadini():
    pass

class textUnWrap():

    __lines=[]  # 原始数据
    __txt=[]    # 保存最终的处理结果

    __textFileName=''
    __outDir='./1/' # 默认的输出目录，这里会有 Bug。

    __writed = False    # 避免重复写盘

    __codeType = 'utf-8'

    def detecCodeType(self):
        finput = open(self.__textFileName,'rb')
        codeType = chardet.detect(finput.read(1024))["encoding"]    #检测编码方式，读1K就可以了。
        # print ('编码是 ', codeType)
        finput.close()
        pass

    def detecLineStruct(self):
        """
        自动判断使用哪种 unwrap 方案。
            basic: 双空格、4+空格开头自然段……
            normal: 顶头，1-2个空格，行尾大量以汉字结束，而不是标点符哈。
            space_break: 行内差不多换行的地方出现一个空格……
            bad: 搞不清楚
        """
        pass

    def __init__ (self, filename='demo_wrap.txt', codeType='utf-8'):
        print(filename)
        print(codeType)

        self.__lines=[] # 读入的原始文件
        self.__textFileName=''
        if codeType=='':
            codeType='utf-8'
        elif codeType=='GB2312' or codeType=='GBK':
            codeType='GB18030'  # 需要逐个检测内码，判断范围是否有超标的。
        with codecs.open(filename,'r', encoding=codeType) as f:
            try:
                self.__lines = f.readlines()
            except Exception as e:
                print(e)    # 一般来说，发生错误后，就不会继续处理了。
                pass
#                raise
            else:
                pass
            finally:
                pass

            self.__textFileName=filename
            self.__txt =[]
        pass

    def close(self):
        # write to file.
        f=open(self.__outDir+self.__textFileName,'w')  #默认存盘的字符编码是utf8，mac下测试。
        for lc in self.__txt:
            f.write(lc)
        f.close()
        #print(self.__txt)
        # 改写 log

    # .basic() 方法需要人工识别。
    def basic(self):
        """
        最简单的情况：“两个全角空格开始”……直到下一个“两个全角空格开始”的行，中间的换行全删掉。
        """
        # 这里要设置一个例子，说明到底能处理哪种状况。

        _tmpLine=''     # 自然段，缓存。
        _newLine = False

        for lc in self.__lines:
            # 每一行的缓存，可以去读区规则区的规则，轮番适配一下。
            if re.search('^　　[^　 ]',lc, re.I):  # \u#3000
                        # 应该 增加一个 四半角空格 的选项。
                if _newLine:    # 两个紧邻的自然段。等于要换行（新段落）了。
                    _tmpLine=_tmpLine+os.linesep

                self.__txt.append(_tmpLine)

                _tmpLine='　　'+lc.strip()    # '\u3000\u3000'
                _newLine=True
            elif lc==os.linesep:    # basic版：空行，就是自然段结束。
                if _newLine:
                    _tmpLine=_tmpLine+os.linesep
                    _newLine=False

                    # 改进：每一行都要单独的append一次。这样的self.__txt是。readlines()的格式。

                _tmpLine=_tmpLine+os.linesep
                self.__txt.append(_tmpLine)
                _tmpLine=''
            else:
                if _newLine:    # 自然段的非首行。
                    _tmpLine=_tmpLine+lc.rstrip()
                else:   # 不是自然段内，不处理。
                    _tmpLine=_tmpLine+lc
        # 最后一行。
        self.__txt.append(_tmpLine)

    def reset(self):
        self.__txt = []

        pass

    '''
    全角字符unicode编码从65281~65374 （0xFF01 ~ 0xFF5E）
    半角字符unicode编码从33~126 （0x21~ 0x7E）
    空格比较特殊，全角为 12288（0x3000），半角为32（0x20）
    而且除空格外，全角/半角按unicode编码排序在顺序上是对应的，
    所以可以直接通过用+-法来处理非空格数据，对空格单独处理。
    '''
    def strQ2B(ustring):
        """把字符串全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code=ord(uchar)
            if inside_code==0x3000:
                inside_code=0x0020
            else:
                inside_code-=0xfee0
            if inside_code<0x0020 or inside_code>0x7e:   #转完之后不是半角字符返回原来的字符
                rstring += uchar
            rstring += unichr(inside_code)
        return rstring

    def strB2Q(ustring):
        """把字符串半角转全角"""
        rstring = ""
        for uchar in ustring:
            inside_code=ord(uchar)
            if inside_code<0x0020 or inside_code>0x7e:   #不是半角字符就返回原来的字符
                rstring += uchar
            if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code=0x3000
            else:
                inside_code+=0xfee0
            rstring += unichr(inside_code)


        return rstring
    '''
    SBC case 全角
    DBC case 半角
    全角-半角 == 0xfee0
    Alpha: A, \uFF21, \u0041 - Z, \uFF3A, \u005A
    Alpha: a, \uFF41, \u0061 - z, \uFF5A, \u007A
    Digital: 0, \uFF10,\u0030 - 9 , \uFF19, \u0039
    '''
    def SBC2DBC_AlphaDigital(self,uString):
        ret = ""
        found = False
        for uchar in uString:
            uCode=ord(uchar)
            if (uCode>0xff21 and uCode<0xff3a) or (uCode>0xff41 and uCode<0xff5a) or (uCode>0xff10 and uCode<0xff19):
                ret +=chr(uCode-0xfee0)
                found = True
            else:
                ret += uchar

            return (ret, found)

    def AlphaDigital(self):
        printLog = True
        for lc in self.__lines:
            ret,found = self.SBC2DBC_AlphaDigital(lc)
            if printLog and found:
                print (lc+'\n'+ret+'\n')

    def advance(self):  # 计算每行的长度。
        # 1 用 muilti_line模式，搜索 标题、独立行……替换成特色【】包含符号。
        # 2 整理 其他剩下的段落，行程新的自然段。
        pass

    def getFilename(self):
        # print(self.__textFileName)
        return self.__textFileName

    def setOutDir(self, outDir='./'):
        self.__outDir = outDir
        pass


import chardet
#import codecs

if __name__ == '__main__':
    i =len(sys.argv)
    # print(len(sys.argv)) # macOS bash 会把 *.* 里面的文件名都展开。
    if i>1: # 如果有参数，要从第一个文件开始计算，或者先装入一个列表。
        while i>1:  # 参数是'*.*'时，shell会自动展开*.*，所以用循环。
            finput = open(sys.argv[i-1], 'rb')
            codeType = chardet.detect(finput.read(1024))["encoding"]    #检测编码方式，读4K就可以了。也许1024
            print ('编码是 ', codeType)
            finput.close()

            unwrap = textUnWrap(sys.argv[i-1],codeType)
            unwrap.basic()  # 如何自动识别？
            unwrap.AlphaDigital() # 转换全角数字字母。
            unwrap.close()  # 写盘
            i=i-1
    else:
        print('Usage example: unwrap.py *.txt')
