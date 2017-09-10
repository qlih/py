#!/usr/bin/env python3
# Encoding:UTF-8
# Filename: hnv_regx_filter.py regx_filter.json

__author__ = '+8617087843871'
__ver = '0.1'

import re
import json

import traceback


class hnv_regx():
    #__rules = []
    __log = False   # 输出日志需要找一个方便的方法。

    def load_files(self):   # find in files
        pass

    def parse_in_files(self):
        pass

    def load_regx(self, filters='regx_filter.json'):
        with open(filters,'r') as f:
            self.__rules=json.load(f)

    def add_rule(self):
        # self.__rules.append()
        pass
        # add a rule throw stdin.

    def parse(self):
        cn=''
        cstr=''

        for rule in self.__rules:
            search_regx=rule.get('search')
            if search_regx is None:
                # bug.
                continue
            replace_regx=rule.get('replace','')
            regx_flag=rule.get('flag', 32) # re.U = 32
            try:
                (cn,number)=re.subn(search_regx,replace_regx,cstr,0,regx_flag)
            except Exception as err:
                print(err)
        #self.data=self.cstr.split('\n\n')

    def  __init__ (self):
        self.__rules=[]
        self.load_regx()

if __name__ == '__main__':
    import os
    import sys

    tf = hnv_regx()
    tf.parse()

    # 过滤器的用法：主要包括，初始化，然后设定参数，取得结果。
