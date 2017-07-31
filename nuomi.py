#coding=utf-8

movieAddressList = []
movieAddressDict = {}

import Tools
import urllib.request
from bs4 import BeautifulSoup
import time
import http.cookiejar

class NuoMi:
    def __init__(self,url):
        self._url = url
        self._header={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            #'Accept-Encoding': 'gzip, deflate',
            'Host': 'bj.nuomi.com',
        }
        self._tool = Tool()
        self._mysqlList = MysqlList()

    def getOpener(self):
        cj = http.cookiejar.CookieJar()
        pro = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(pro)
        header = []
        for key,value in self._header.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        return opener

    def start(self):
        #self._mysqlList.initMovieAddress()
        self.getSocre()

        #获取跳转的字符
        for key,value in movieAddressDict.items():
            print(value)
            self.getFilmPrice(value["MovieName"],value["NuomiAddress"])
            for number in range(2,30):
                filmUrl = value["MovieAssistAddress"] + str(number)
                time.sleep(3)
                if (self.getFilmPrice(value["MovieName"],filmUrl) == False):
                    break

    def getScoreContent(self):
        try:
            #req = urllib.request.Request(self._url)
            #response = urllib.request.urlopen(req)

            opener = self.getOpener()
            response = opener.open(self._url)
            data = response.read().decode('UTF-8')
            return data
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print("连接糯米电影网页失败,错误原因",e.reason)
                return None

    #获取电影列表的请求
    def get_ajax_Title(self):
        ajaxUrl = 'http://bj.nuomi.com/pcindex/main/filmlist?type=1'
        print('正在访问ajax网页   ' + ajaxUrl)
        #ajaxReq = urllib.request.Request(ajaxUrl, headers=self._header)
        #response = urllib.request.urlopen(ajaxReq)
        opener = self.getOpener()
        response = opener.open(ajaxUrl)
        data = response.read().decode('UTF-8')
        return data

    #通过标签为a找到电影的名称，地址和评分
    def getSocre(self):
        ajaxData = self.get_ajax_Title()
        soup = BeautifulSoup(ajaxData)

        a_soup = soup.find_all('a')
        if (a_soup != None):
            for soupData in a_soup:
                if soupData['href'] != 'javascript:void(0);':#筛选
                    if soupData.span != None:
                        score = soupData.em.string + soupData.span.string
                    else:
                        score = str(0)

                    movieName = soupData['title']
                    movieAddress = self._url + soupData['href']
                    MovieAssistAddress = movieAddress + '/0-0/subd/cb0-d10000-s0-o-b1-f0?pn='
                    dict = {"MovieName":movieName, "NuomiAddress":movieAddress, "MovieAssistAddress":MovieAssistAddress, "MovieScore":score}
                    self._mysqlList.updateMovieAddress(dict)
                    #print(dict)

    #获取电影数据
    def getFilmPriceData(self,filmName,filmUrl):
        print('正在访问电影:'+ filmName+ '的网页,' + filmUrl)
        #filmReq = urllib.request.Request(filmUrl, headers=self._header)
        #response = urllib.request.urlopen(filmReq)
        opener = self.getOpener()
        response = opener.open(filmUrl)
        data = response.read().decode('UTF-8')
        return data


    #获取各个电影的价格，地址和评分
    def getFilmPrice(self,filmName,filmUrl):
        data = self.getFilmPriceData(filmName, filmUrl)
        print(data)
        soup = BeautifulSoup(data)

        class_soup = soup.find_all(attrs={'class':'cinema'})
        if (class_soup != None):
            for classData in class_soup:
                cinemaName = classData.find(attrs={'class':'cib-name'}).a.string
                cinemaMap = classData.find(attrs={'class':'cib-address'}).p.string
                cinemaScore = classData.find(attrs={'class':'cib-rate'}).find(class_ = "rate-int").string + classData.find(attrs={'class':'cib-rate'}).find(class_ = "rate-decimal").string

                if (classData.find(class_ = "ci-groupon clearfix") != None):#有时候不会有团购价格，所以需判断
                    cinemaGroupPrice = classData.find(class_ = "ci-groupon clearfix").find(class_ = "ci-price").string
                else:
                    cinemaGroupPrice = str(0)

                if (classData.find(class_ = "ci-book clearfix") != None):#有时候不会有选座价格，所以需判断
                    cinemaBookPrice = classData.find(class_ = "ci-book clearfix").find(class_ = "ci-price").string
                else:
                    cinemaBookPrice = str(0)

                strPrint = "电影名称:" + cinemaName  + ", \t团购价" + cinemaGroupPrice + ", \t在线选座价:" + cinemaBookPrice + ", 地址:" + cinemaMap
                dict = {'MovieName':filmName,'CinemaName':cinemaName, 'CinemaMap':cinemaMap,'CinemaScore':cinemaScore,'CinemaGroupPrice':cinemaGroupPrice,'CinemaBookPrice':cinemaBookPrice,'updateTime':str(int(time.time()))}
                print(dict)
                self._mysqlList.AddCinema(dict)
        else:
            print('Class soup is None')
            return False

        return True