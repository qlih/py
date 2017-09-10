#!/usr/bin/env python3
   # -*- coding:utf-8 -*-
# HTMLParser处理器 (www.38YeYe.com)
# 文章 从 htm 导出 到 utf-8 unwrap text


__version__ = '0.01'

from html.parser import HTMLParser
import re

class YeYeContentParser(HTMLParser):
	_re=[] #放置结果, 如果不用赋值清除，就会一直积累……
	_flg=False #标志，找到了版本。

	# @处理逻辑：
	#	1. 找到 <title>标签，如果 内容 有 'YeYe' 关键字，则继续处理。 flag = step_1
	filename = ''
	_step_1 = False	# 处理 过程中 = True， 处理完 = False
	#	2. 找到 <div class='title'> 得到 标题，继续处理。
	_step_2 = False
	#	3. 找到 <div class='ui-detail-info'> 得到正文，
	_step_3=False
	#	4. 处理正文：
	_step_4=False
	#	4.1 在正文中，<br/> 标签、<br>标签替换为换行；
	#	4.2 遇到 7个'?'+1个' '，替换为两个全角空格。（这个需要在全文扫描后做，还不会）
	#	4.3 遇到 reg = '＊.*＊', 要换行。但是 行首 没有添加空格。也没有处理半角的'*'。
	# @end

	"""
	@todo
		1. 段内处理
			- 没有处理行首、行尾的空格；
			- 没有调用半角、全角转换；
		2. 段落之间的处理
			- 没有处理重复的标题行；
			- 多余的空行。
	@end
	"""

	def handle_starttag(self, tag, attrs):
		if tag=='title':
			self._step_1 = True
		elif tag=='div' and self._flg == True:	# 如果 版本 正确则继续处理
			for attr in attrs:
				if attr[0]=='class' and attr[1]=='title':
					self._step_2 = True
				elif attr[0]=='class' and attr[1] == 'ui-detail-info':
					self._step_3 = True
		elif tag=='br':	# 处理 <br>，而不是 <br ／>，因为是没有</br>这种写法的。<br>就意味着是老版本的资料。
			# 4.1
			self._step_4 = True
			self._re.append('\n')	# <br> --> '\n'
		else:
			pass

	def handle_data(self, data):

		if self._step_1 == True:
			self._step_1 = False	# 只处理第一个 <title>
			if re.search('YeYe', data, re.I):
				self._flg = True 	# 是要处理的文本。
				# 取 子字符串 的结果集合的第一个元素，即要找的标题。
				t_tmp = re.findall('【(.*?)】', data, re.I)
				if len(t_tmp) == 0:
					t_tmp = re.findall('(.*?) ', data, re.I)
				if len(t_tmp) == 0:
					self.filename = ''
				else:
					self.filename = t_tmp[0]	# 通常会有几个，如 1-4、完 什么的。

		if self._step_2 == True:
			self._re.append(data)
			self._re.append("\n\n")	# 标题后空两行
			self._step_2 = False

		if self._step_3 == True and self._step_4 == False:
			# 在 step3 状态下处理 本 <div> 之后的data，<br/>之前的。
			self._re.append(data)	# 这是 div 的 data

		if self._step_4 == True:
			# 4.2
			t_tmp = re.sub('([\?]+[ ]*)','　　', data, re.I)
			# 4.3
			t_tmp = re.sub('(＊.*＊)', '\g<1>\n', t_tmp)
			self._re.append(t_tmp)
			self._step_4 = False

		else:
			pass

	def handle_endtag(self, tag):
		if self._step_3 == True and tag=='div':  # 处理了<br/>以后，遇到了</div>
			self._step_3 = False
		else:
			pass

	def handle_startendtag(self, tag, attrs):
		if self._step_3 == True and tag=='br':
			self._step_4 = True
			# 4.1
			self._re.append("\n")	# <br/> --> '\n'
		else:
			pass

import sys
import codecs	# 读 gbk 编码的本地文件。自动判断，还不会。

if __name__ == '__main__':
	i =len(sys.argv)
	if i>1:
		my=YeYeContentParser()
		while i>1:
			print('Parse '+sys.argv[i-1])
			my._re=[]
			my.feed(codecs.open(sys.argv[i-1], 'r', 'GB18030').read())
			if(my.filename ==''):
				my.filename = sys.argv[i-1].rstrip('.html')	# 用输入文件名替换没有得到的标题名。
			print('\t'+my.filename)
			f=open('story.x.'+my.filename+'.txt','w')
			f.writelines(my._re)
			f.close()
			i=i-1
	else:
		print('Usage example: python3 '+ sys.argv[0]+ ' *.html')
