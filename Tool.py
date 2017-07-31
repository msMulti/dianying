#coding=utf-8

import mysql
from mysql import connector
import re
from selenium import webdriver

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

class DBMysql:
    def __init__(self,user,passwd,host,db):
        self._user = user
        self._passwd = passwd
        self._host = host
        self._db = db
        self._conn = mysql.connector.connect(user=self._user,passwd=self._passwd,host=self._host,db=self._db)

    def store(self,data):
        cursor = self._conn.cursor()
        cursor.execute(data)
        ret = cursor.fetchall()
        cursor.close()
        return ret

    def execute(self,data):
        cursor = self._conn.cursor()
        cursor.execute(data)
        cursor.close()

    def close(self):
        self._conn.close()


class MysqlList:
    def __init__(self):
        self.dbMysql = DBMysql('root','gsmrlab','123.57.28.46','Movie')

    def initMovieAddress(self):
        global movieAddressDict
        rows = self.dbMysql.store("select MovieName,MovieAddress,MovieAssistAddress from MovieAddress;")
        for row in rows:
            dict = {"MovieName":row[0], "NuomiAddress":row[1], "MovieAssistAddress":row[2]}
            movieAddressDict[row[0]] = dict

        for key,vlaue in movieAddressDict.items():
            strPrint = "key:" + key + ", 电影名称:" + vlaue["MovieName"] + ", " + "糯米地址:" + vlaue["NuomiAddress"]
            print(strPrint)

    #更新总电影列表
    def updateMovieAddress(self, data):
        if data["MovieName"] in movieAddressDict:
            movieDict = movieAddressDict[data["MovieName"]]

            if movieDict["NuomiAddress"] != data["NuomiAddress"]:
                strPrint = "---更新地址----\n更新的电影名称:" + data["MovieName"] + "旧地址:" + movieDict["NuomiAddress"] + "; 新地址:" + data["NuomiAddress"]
                print(strPrint)

                updateData = "update MovieAddress SET MovieAddress='" + data["NuomiAddress"] + "',MovieAssistAddress='" + data["MovieAssistAddress"] + "' WHERE MovieName='" + data["MovieName"] + "';"
                print(updateData)
                self.dbMysql.execute(updateData)

        else:
            dict = {"MovieName":data["MovieName"], "NuomiAddress":data["NuomiAddress"]}
            strPrint = "---更新电影----\n新加入的电影名称:" + data["MovieName"] + "," + "糯米地址:" + data["NuomiAddress"]
            print(strPrint)
            movieAddressDict[data["MovieName"]] = dict
            insertData = "insert INTO MovieAddress SET MovieName='" + data["MovieName"] + "',MovieAddress='" + data["NuomiAddress"] + "',MovieAssistAddress='" + data["MovieAssistAddress"] + "',MovieScore='" + data["MovieScore"] + "';"
            print(insertData)
            self.dbMysql.execute(insertData)

    #添加电影院信息
    def AddCinema(self, data):
        insertData = "insert INTO Cinema SET CinemaName='" + data["CinemaName"] + "',MovieName=' " + data["MovieName"] + "',CinemaMap='" + data["CinemaMap"] + "',CinemaScore='" + data["CinemaScore"] +"',NuomiGroupPrice='" + data["CinemaGroupPrice"]+ "',NuomiBookPrice='" + data["CinemaBookPrice"]+ "',Time=FROM_UNIXTIME('" + data["updateTime"]+ "');"
        print(insertData)
        self.dbMysql.execute(insertData)





