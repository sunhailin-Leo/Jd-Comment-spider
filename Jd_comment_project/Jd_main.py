# -*- coding:utf-8 -*- #
'''
@author: Leo
'''
import os
import json
import time
import random
import shutil
import win32api
import win32con
import urllib.request as ur
from bs4 import BeautifulSoup
from http import cookiejar
from Jd_comment_project.csvfile_writer import *
from Jd_comment_project.logger_writer import *
from Jd_comment_project.mongodb_writer import *
from Jd_comment_project.user_agent_pool import *

class parse:
    def __init__(self):
        
        # while循环标志标量
        self.Flag = True
        
        # 用list存储评论数据
        self.datalist = []
        
        # 翻页数，初始为0 
        self.turnPage = 0

        # 存取错误页数的List
        self.ErrroPage_list = []
        
        # 设置循环创建文件的编号，初始值为0
        self.Doc_flag = 0
        
        # 初始化错误信息的字符串（测试时不没初始化导致报错）
        self.error_info = ""
        
        # 初始化productId
        self.productId = 0

    def pasrser(self, page, csvfile):
        # 循环置空
        self.datalist = []
        
        # 打开json页面
        # 1、从agent池中随机获取一条agent
        rand = random.randint(0, len(user_agent) - 1)
        headers = {"user-Agent": user_agent[rand]}

        # 拼凑Url地址，并通过opener打开json页面
        url_data = "https://sclub.jd.com/comment/productPageComments.action?productId=" + self.productId + "&score=0&sortType=3&page=" + str(page) + "&pageSize=10&isShadowSku=0"
        cookie = cookiejar.CookieJar()
        opener = ur.build_opener(ur.HTTPCookieProcessor(cookie))
        request = ur.Request(url_data, headers=headers)
        html = opener.open(request).read().decode('gbk')

        # 测试输出到控制台，方便查询问题
        Console_print = "https://sclub.jd.com/comment/productPageComments.action?productId=" + self.productId + "&score=0&sortType=3&page="+ str(page) +"&pageSize=10&isShadowSku=0" + "\n" + "User:Agent:"+ user_agent[rand]
        print(Console_print)

        # 把页面数据转成JSON数组
        try:
            jsonDict = json.loads(html)
        except:
            print('error json loads   ####### 请等待    #######')
            time.sleep(90)
            self.pasrser(page, csvfile)
        
        # 选择json的comments子节点
        json_hotCommentTagStatistics = jsonDict['comments']
        
        # 计算一页json的评论数的长度
        json_len = len(json_hotCommentTagStatistics)
        
        
        # 循环获取一页的评论
        for each_comment in json_hotCommentTagStatistics:
            self.datalist.append(each_comment['nickname'])
            self.datalist.append(each_comment['content'])
            self.datalist.append(each_comment['creationTime'])
            self.datalist.append(each_comment['referenceName'])
            self.datalist.append(each_comment['userProvince'])
            self.datalist.append(each_comment['userLevelName'])
            self.datalist.append(each_comment['userClientShow'])

        # 判断传进函数的csvfile参数是否为None，Controller函数中区分两种状态影响csvfile的参数        
        if csvfile is not None:
            csv_writter(self.datalist, csvfile)
        
        else:
            insert_into_mongodb(self.datalist)    
        # 判断一页json的长度，如果小于10则说明到达尾页，否则继续执行while循环
        if json_len < 10: 
            return False
        return True

    # 核心Controller方法
    def controller(self, path, file_path, save_way):

        if save_way == "csv":
            # 打开并创建csv文件
            with open(path, 'w+') as path:
                # 开始循环（默认为True）
                while self.Flag:
                    try:
                        time.sleep(random.random())
                        self.turnPage += 1
                        print(self.turnPage)
                        self.Flag = self.pasrser(page = self.turnPage, csvfile = path)
                    except Exception as err:
                        self.error_info = str(err)
                        break
    
            # 关闭csv流
            path.close()
    
            # 打印错误页码
            print("Error", self.turnPage)
    
            # 将错误页码保存到list中，当所有正常页码抓取完毕以后输出到log文件中
            self.ErrroPage_list.append(self.turnPage)
    
            # 判断页面报错类型是否为编码转换类型
            if "'gbk' codec can't decode byte" in self.error_info:
                print("Skip Error")
                self.Retry_function(page = self.turnPage + 1, file_path = file_path)
            else:
                time.sleep(90)
                self.Retry_function(page = self.turnPage, file_path = file_path)
                
        elif save_way == "MongoDB":
            while self.Flag:
                    try:
                        time.sleep(random.random())
                        self.turnPage += 1
                        print(self.turnPage)
                        self.Flag = self.pasrser(page = self.turnPage, csvfile = None)
                    except Exception as err:
                        self.error_info = str(err)
                        break
            # 打印错误页码
            print("Error", self.turnPage)
    
            # 将错误页码保存到list中，当所有正常页码抓取完毕以后输出到log文件中
            self.ErrroPage_list.append(self.turnPage)
    
            # 判断页面报错类型是否为编码转换类型
            if "'gbk' codec can't decode byte" in self.error_info:
                print("Skip Error")
                self.Retry_function(page = self.turnPage + 1, file_path = None)
            else:
                time.sleep(90)
                self.Retry_function(page = self.turnPage, file_path = None)
        

    # 重试方法
    def Retry_function(self, page, file_path):
        
        print("#######请等待#######")
        if self.pasrser(page, csvfile = None) is True:
            self.Doc_flag += 1
            if file_path is not None:
                self.controller(file_path + "\\JD_Product_Comment_" + str(self.Doc_flag) + ".csv", file_path = file_path)
            else:
                self.controller(None, None, "MongoDB")
        else:
            print("All data Save")
            if file_path is not None:
                export_error_log(self.ErrroPage_list, file_path = file_path)
            else:
                export_error_log(self.ErrroPage_list, file_path = "D:\\")


# 类的初始化
P = parse()

# 存储方法选择
save_way = input("请选择存储方式:(1.csv、2.MongoDB):")

# 用户输入商品id号
P.productId = input("请输入商品的Id:")

# 判断用户存储 
if save_way == "1": 
    
    # 获取桌面路径并创建文件
    Desktop_Path = win32api.RegQueryValueEx(win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 0, win32con.KEY_READ), 'Desktop')[0].replace("\\","\\\\")
    path = Desktop_Path + '\\' + 'JD_Product_Comment'

    if os.path.exists(path):
        shutil.rmtree(path)
        print("######### Clear Already ######### ")
    
    os.mkdir(path)
    print("######### CreateFile Already ######### ")
    
    # 程序入口为parse类中的Controller方法
    P.controller(path = path + '\\' + "JD_Product_Comment_1.csv", file_path = path, save_way = "csv")
    
    # 当所有评论存入csv中（存在可能生成多个csv文件），合成一份
    Combine_csvfile(path)

elif save_way == "2":
    path = None
    file_path = None
    save_way = "MongoDB"
    P.controller(path, file_path, save_way)

else:
    raise Exception("WrongChoiceException")

    

