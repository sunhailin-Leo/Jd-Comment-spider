# -*- coding:utf-8 -*- #
'''
@author: Leo
'''
import datetime
from pymongo import MongoClient

conn = MongoClient('mongodb://localhost:27017')
db = conn.JD

def insert_into_mongodb(comment_list):
    
    comment_list = [comment_list[i:i+7] for i in range(0, len(comment_list), 7)]
    
    # 把拆分后的list循环取出
    for each_comment in comment_list:
        Each_comment_dict = {'nickname':each_comment[0],'content':each_comment[1],'creationTime':each_comment[2],'referenceName':each_comment[3],'userProvince':each_comment[4],'userLevelName':each_comment[5],'userClientShow':each_comment[6]}
        try:
            db.Comment.insert(Each_comment_dict)
        except Exception as err:
            print("[Error]" + datetime.datetime.now() + "mongodb_writer:" + err)