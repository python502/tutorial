#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/27 10:23
# @Author  : long.zhang
# @Contact : long.zhang@opg.global
# @Site    : 
# @File    : start.py
# @Software: PyCharm
# @Desc    :

from scrapy import cmdline
cmdline.execute("scrapy crawl etherscan -a id_name=0x2f70fab04c0b4aa88af11304ea1ebfcc851c75d1".split())