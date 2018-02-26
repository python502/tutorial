#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 13:57
# @Author  : long.zhang
# @Contact : long.zhang@opg.global
# @Site    : 
# @File    : amazon.py
# @Software: PyCharm
# @Desc    :
from tutorial.items import EtherscanProductRaw
import scrapy
import re
import time

from bs4 import BeautifulSoup

def getDict4str(strsource, match=':'):
    outdict = {}
    lists = strsource.split('\n')
    for list in lists:
        list = list.strip()
        if list:
            strbegin = list.find(match)
            outdict[list[:strbegin]] = list[strbegin + 1:] if strbegin != len(list) else ''
    return outdict
HEADER = '''
        accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        accept-encoding:gzip, deflate, br
        accept-language:zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
        cache-control:max-age=0
        upgrade-insecure-requests:1
        User-Agent:{}
        '''
header = getDict4str(HEADER.format(
    r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'))

class Etherscan(scrapy.Spider):
    name = 'etherscan'
    def __init__(self, id_name=None, *args, **kwargs):
        super(Etherscan, self).__init__(*args, **kwargs)
        self.start_urls = ['https://etherscan.io/address/{}'.format(id_name)]
        self.id_name = id_name
    def parse(self, response):
        formatUrl = 'https://etherscan.io/txs?a={}&p={}'
        soup = BeautifulSoup(response.body, 'lxml')
        num = int(soup.find('span', {'title': "Normal Transactions"}).getText().strip('\n').strip()[:-4].strip())
        if num%50 == 0:
            page = num/36
        else:
            page = num / 36+1

        for x in range(page):
            x+=1
            url = formatUrl.format(self.id_name, x)
            print url
            yield scrapy.Request(url=url, meta={"id_name": self.id_name},
                                 callback=self.parse_url)
    def parse_url(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        datas = soup.find('table', {'class': "table table-hover "}).find('tbody').findAll('tr')
        now = time.time()
        for sourceData in datas:
            infos = sourceData.findAll('td')
            if len(infos) != 8:
                break
            resultData = EtherscanProductRaw()
            resultData['name'] = response.meta.get('id_name')
            if infos[0].find('font'):
                continue

            resultData['TxHash'] = infos[0].find('span').getText().strip()
            resultData['Block'] = int(infos[1].getText().strip())
            resultData['From_account'] = infos[3].find('span').getText().strip()
            resultData['To_account'] = infos[5].find('span').getText().strip()
            value = ''.join(infos[6].getText().split(','))
            resultData['Value'] = float(value[:-5].strip() if value.find('Ether') !=-1 else value.strip())
            TxFee = ''.join(infos[7].getText().split(','))
            resultData['TxFee'] = float(TxFee[:-5].strip() if TxFee.find('Ether') !=-1 else TxFee.strip())

            # import pdb
            # pdb.set_trace()
            Age = infos[2].find('span').getText().strip()
            pattern_hr = re.compile('\d+ hr')
            pattern_day = re.compile('\d+ day')
            pattern_min = re.compile('\d+ min')
            pattern_count = re.compile('\d+')

            hours = int(pattern_count.findall(pattern_hr.findall(Age)[0])[0]) if pattern_hr.findall(Age) else 0
            day = int(pattern_count.findall(pattern_day.findall(Age)[0])[0]) if pattern_day.findall(Age) else 0
            min = int(pattern_count.findall(pattern_min.findall(Age)[0])[0]) if pattern_min.findall(Age) else 0
            t = now - hours*3600 - day*86400 - min*60
            resultData['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            resultData['operate_type'] = infos[4].find('span').getText().strip()
            yield resultData








