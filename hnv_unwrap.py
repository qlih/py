#!/usr/bin/env python3
# Encoding:UTF-8
"""
    hnv_unwrap.py
    算法描述：
    utf-8格式读入
        测量长度，一般字符算1，CJK算2，各行的长度都统计后，排序。相对多字符（比如多余56个ascii），最长的行，如果不多，则可以忽略，看某一个宽度，如70字宽的行是不是很多。
        如果确定是 wrap 的格式，则
            干掉折行，不论结尾的地方是否有标点；
"""
__author__ = 'qlih@qq.com'
__version__ = '0.07'

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
    classic:
        章节数字标准化，上中下等先放放。

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
        print('('+ codeType +')'+ filename)

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
        fout, found = self.SBC2DBC_AlphaDigital(self.__textFileName)
        # 文件名要转换全角到半角。
        f=open(self.__outDir+fout,'w')  #默认存盘的字符编码是utf8，mac下测试。
        for lc in self.__lines:
            f.write(lc)
        f.close()


    # .basic() 方法需要人工识别。
    def basic(self):
        """
        最简单的情况：“两个全角空格开始”……直到下一个“两个全角空格开始”的行，中间的换行全删掉。
            第一行：Title
            第二行：空行 或者 作者、日期等
            第三行：空行
            第四行：正文，或者“第一个章节”，章节=^第[\\d]章：Text\n
            第五行：如果前文是章节，这里是空行
            第六行：本章节正文结束。此处可以结束文件。
            第七行：重复：第三行，或者 空行
            第八行：如果没有章节，最后一个标志是‘■’
        用换行分割自然段，自然段开头不留空格顶头的，是另一种模式。
        """
        # 这里要设置一个例子，说明到底能处理哪种状况。

        _tmpLine=''     # 自然段，缓存。也叫半行缓存。
        _newLine = False

        last_linetmp ='' # 最后一行，非空，用于判断文件末尾。
        split_str = '　　❉❉　　❉❉　　❉❉'+os.linesep
            #    '　　❉　❉　❉　❉　❉　❉' = '^[　]+(　❉)+'
            #    '　　❉❉　　❉❉　　❉❉' = '^(　　❉❉)+'
            #    '►▬▬◄'

            # '　　***', '　　…………', '　　……' 

        for lc in self.__lines:
            # 每一行的缓存，可以去读区规则区的规则，轮番适配一下。
            if re.search('^＊＊＊＊＊＊＊＊＊[＊]+',lc,re.I):
                self.__txt.append(lc)
            if re.search('^　　[　 ]+[第（0-9]',lc, re.I): # 找引导空格很多的标题行
                self.__txt.append(lc.strip()+os.linesep) # 直接处理成顶头的。
            elif re.search('^　[　 ]+[※❉＊]+.*',lc, re.I): # （独立的）分割行
                # 用‘*’分割的可能是敏感词，需要孤立存在。即“    ****\n”这种。
                self.__txt.append(split_str)    # 直接替换
            elif lc.strip() == '':    # basic版：空行，就是自然段结束。lc==os.linesep or lc.strip() == ''
                # todo: 空行的戏一行可能是顶格的“小标题”，也可能是一个折行的东西
                # 判断标题需要用 ^第[0-9]+章节折，字符串不够长，一般没有结束标点。
                # 或者先用章节目录工具处理一下？
                if _newLine:

                    self.__txt.append(_tmpLine+os.linesep) # 结束一个自然段。当前的换行没处理。
                    # _tmpLine='' # 和下文的重复了，可以删除这行。
                    _newLine=False

                _tmpLine=''
                self.__txt.append(os.linesep)
            elif re.search('^　　[^　 ]+',lc, re.I) or re.search('^    [^　 ]+',lc, re.I):  # \u#3000
                        # 应该 增加一个 四半角空格 的选项。
                if _newLine:    # 两个紧邻的自然段。等于要换行（新段落）了。
                    _tmpLine=_tmpLine+os.linesep

                self.__txt.append(_tmpLine)

                _tmpLine='　　'+lc.strip()    # '\u3000\u3000' 行未没有换行。
                _newLine=True   # 确定发现了新自然段。
                # 补丁：修补单独空格的行。
            else:
                if _newLine:    # 自然段的非首行。
                    _tmpLine=_tmpLine+lc.strip() # lc.rstrip() 删掉了行尾的空白和换行。
                else:   # 不是自然段内的顶头行，不处理。（一般是标题）
                    # _tmpLine=_tmpLine+lc # 保留了换行。
                    self.__txt.append(lc.strip()+os.linesep) # 结束一个自然段。当前的换行没处理。
                    _tmpLine = ''   # 没有记录前后文，不知道需不需要记录。记录的好处是可以再加工如“标题”、”分隔符“等扩展内容。
        # 最后一行。最后一行的末尾可能有连续换行。删掉也没什么。
        self.__txt.append(_tmpLine.rstrip()) # 最后一行没有换行符号

        # -----------------------------------
        # 最后一行的“完”签字，倒数查询。
        found =False # 没找到最后一行。
        for i in range(len(self.__txt)-1, -1, -1):
            if self.__txt[i].strip() == '':
                # print(str(i) + 'deleted!')
                del self.__txt[i]    # 删除文件末尾的空行，遇到‘■’时，删除之前的空行，然后后面再加回来。
            else:
                # print(len(self.__txt[i].strip()))
                if found:   # 已经找到最后一行了。
                #    如果删除多了，比如“正文\n\n\n\nPS：正文（完）“,
                #    就会把中间的换行删掉了。
                    break   # 发现了不是末尾的一行，中止
                else:
                    last_linetmp = self.__txt[i]
                    # print('\t' + str(i) + '\n'+last_linetmp)
                    del self.__txt[i]    # 最后一行待处理，移除。
                    found = True # 找到最后一行后，继续循环，把前面的多余空行删除
        
        '''
        最后一行的规则：
            （完）| 【全书完】【完】（排除 未完待续）
            ‘■’后面没有换行，如果没有“完”，就要给一个换行。
        '''

        # 区分行内（完）还是独立行（完）
        _tmpEnd = '[　 \\t]*[\\w（\\(【^未]+完+[】\\)）]$'    # ■也可能在末尾？
        last_linetmp = last_linetmp.rstrip()
        if last_linetmp == '■':
            self.__txt.append(os.linesep)   # 回填一个空行
        elif re.search('^'+_tmpEnd,last_linetmp, re.I):
            last_linetmp = '\n■'  # 直接替换
            print('\tfound:^【完】')
        elif re.search(_tmpEnd,last_linetmp, re.I):
            # 行尾替换
            print('\tfound:【完】')
            last_linetmp = re.sub(_tmpEnd, '\n\n■', last_linetmp)
        else:
            pass

        self.__txt.append(last_linetmp.rstrip())        # 加回最后一行，删掉多余的换行。

        # 修复缓冲区
        self.__lines = self.__txt
        self.__txt = []

    def reset(self):
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
    Alpha: Ａ, \uFF21 -> \u0041  Z, \uFF3A -> \u005A
    Alpha: a, \uFF41, \u0061 - z, \uFF5A, \u007A
    Digital: 0, \uFF10,\u0030 - 9 , \uFF19, \u0039
    '''
    def SBC2DBC_AlphaDigital(self,uString):
        ret = ""
        found = False
        for uchar in uString:
            uCode=ord(uchar)
            if (uCode>=0xff21 and uCode<=0xff3a) or (uCode>=0xff41 and uCode<=0xff5a) or (uCode>=0xff10 and uCode<=0xff19):
                ret +=chr(uCode-0xfee0)
                found = True
            else:
                ret += uchar

        return (ret, found)


    def AlphaDigital(self):
        printLog = True
        ret = ""

        for lc in self.__lines:
            ret,found = self.SBC2DBC_AlphaDigital(lc)
#            if printLog and found:
#                print (lc+'\n'+ret+'\n')
            self.__txt.append(ret)

        # 修复缓冲区
        self.__lines = self.__txt
        self.__txt = []

        pass


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


import chardet  # pip3 install chardet

if __name__ == '__main__':
    i =len(sys.argv)
    # print(len(sys.argv)) # macOS bash 会把 *.* 里面的文件名都展开。
    if i>1: # 如果有参数，要从第一个文件开始计算，或者先装入一个列表。
        while i>1:  # 参数是'*.*'时，shell会自动展开*.*，所以用循环。
            finput = open(sys.argv[i-1], 'rb')
            codeType = chardet.detect(finput.read(1024))["encoding"]    #检测编码方式，读4K就可以了。也许1024
            # print ('编码是 ', codeType)
            finput.close()

            unwrap = textUnWrap(sys.argv[i-1],codeType)
            unwrap.basic()  # 如何自动识别？
            unwrap.AlphaDigital() # 转换全角数字字母。
            unwrap.close()  # 写盘
            i=i-1
    else:
        print('Usage example: unwrap.py *.txt')

"""
1 ＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊＊
--->不处理
2 标题识别
　　　　　　　　　　　　　　　（一）
　　1、这种不是
    2、章节没有断行！
    loop1
    ^(第[一二三四五六七八九十]+章)(.*) -->$1$2\n，然后另一个文件改章节号？
    loop2，解决没有title的章节问题。
    ^(第[一二三四五六七八九十]+章)([ 　]+)(.*)  -->$1：$3

3 结束
    '  （...完）' 的识别还是问题很多。：'【完】'直接点名更准一些。'　　完。'，‘——结束’
    sublime text 和 python 的正则不一样。需要一个python正则工具
        待测试文本，期待文本，测试后结果，结果对比。
4 长句末尾没有标点，不是分割线的，警告。
5 全角转半角
    － 是不是转 - ？
6 输出目录需要改
7 文件名的标题要修订，带有“完”的需要改标题“-最后一章”，否则……
    没有“完”，而且有“章节”的，就要在文件名上加1-?$，
    有■的，有章节的加章节总数，如ABC-7.txt
8 去垃圾
    ‘[|]*派派.*\n’
9 后记、附件、同人、番外，统统用■再分割。
"""