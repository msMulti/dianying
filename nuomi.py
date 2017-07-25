#coding=utf-8

movieAddressList = []
movieAddressDict = {}

import mysql
from mysql import connector
import urllib.request
import re
from bs4 import BeautifulSoup
import time
import http.cookiejar

class Tool:
    removeImg = re.compile('<img.*?>| {7}')
    removeAddr = re.compile('<a.*?>| </a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?')

    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()
    
    
    2222222222
