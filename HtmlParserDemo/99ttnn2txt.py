#!/usr/bin/env python3
   # -*- coding:utf-8 -*-
# HTMLParser处理器 (99ttnn)
   # 比 38YeYe 进化了一点。
# 文章 从 htm 导出 到 utf-8 unwrap text


__version__ = '0.02'

from html.parser import HTMLParser
import re

class TtnnContentParser(HTMLParser):
	_identify='99ttnn'
	_re=[] #放置结果, 如果不用赋值清除，就会一直积累……
	_flg=False #标志，找到了版本。

	# @处理逻辑：
	#	1. 找到 <title>标签，如果 内容 有 self._identify 关键字，则继续处理。 flag = step_1
	filename = ''
	_step_1 = False	# 处理 过程中 = True， 处理完 = False
	#	2.
	#_step_2 = False
	#	3. 找到 <div class='picContent'> 得到正文，
	_step_3=False
	#	4. 处理正文：
	_step_4=False
	#	4.1 在正文中，<br/> 标签、<br>标签替换为换行；
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
				if attr[0]=='class' and attr[1] == 'picContent':
					self._step_3 = True
		elif self._step_3 == True and tag=='br':	# 处理 <br>，而不是 <br ／>，因为是没有</br>这种写法的。<br>就意味着是老版本的资料。
			# 4.1
			self._step_4 = True
			self._re.append('\n')	# <br> --> '\n'
		else:
			pass

	def handle_data(self, data):

		if self._step_1 == True:
			self._step_1 = False	# 只处理第一个 <title>
			if re.search(self._identify, data, re.I):
				self._flg = True 	# 是要处理的文本。
				# 取 子字符串 的结果集合的第一个元素，即要找的标题。
				t_tmp = re.findall('【(.*?)】', data, re.I)
				if len(t_tmp) == 0:
					t_tmp = re.findall('(.*?)[ _]', data, re.I)
				elif len(t_tmp) == 0:
					self.filename = ''
				else:
					self.filename = t_tmp[0].strip()	# 通常会有几个，如 1-4、完 什么的。

		if self._step_3 == True:
			# 99ttnn 都是在 <br />之后开始正文的。
			pass

		if self._step_4 == True:
			self._re.append(data)
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
			self._re.append('\n')	# <br/> --> '\n'
		else:
			pass

import sys
import os

if __name__ == '__main__':
	i =len(sys.argv)
	if i>1:
		my=TtnnContentParser()
		while i>1:
			print('Parse '+sys.argv[i-1])
			my._re=[]
			my.feed(open(sys.argv[i-1]).read())
			if(my.filename ==''):
				my.filename = sys.argv[i-1].rstrip('.html')	# 用输入文件名替换没有得到的标题名。
			print('\t'+my.filename)

			# 判断 写盘文件 是否存在，防止标题名一样的系列文章互相覆盖。
			outfile='story.x.'+my.filename+'.txt'
			j=0
			while True:
				if os.path.exists(outfile):
					outfile = 'story.x.'+my.filename+'.'+str(j)+'.txt'
					j = j+1
				else:
					break;
			# with ... as f
			f=open(outfile,'w')
			f.writelines(my._re)
			f.close()
			i=i-1
	else:
		print('Usage example: python3 '+ sys.argv[0]+ ' *.html')
