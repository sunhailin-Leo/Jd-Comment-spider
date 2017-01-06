# Jd-Comment-spider --- v0.1 beta

#####Design from :@Leo-Sunhailin(https://github.com/sunhailin-Leo)
#####Contract:
    * Email：379978424@qq.com  / shjkfld379978424@gmail.com
    * Wechat: 379978424
#####Donation:
    * 如果你对我的项目感兴趣的可以进行捐助或留言支持并提供帮，这样我会很乐意的将此项目进行完善下去。
    * If you glad to donate to me or leave a message to help me, i will continue complete this project


### 项目说明（Project explanation）
* Python版本(Python Version)：python 3.4
* 编译环境(Compile Environment)：Eclipse Neon 1.1（pydev插件）--- pydev plugins
* 第三方库的支持(Other Libs)：BeautifulSoup4,pymongo,cookieJar
* 本地库的支持(Local libs support)：
    * 系统库(System libs)：os,shutil,win32api,win32con
    * 本地库(Local libs): re,json,date,random,urllib
* 其他(Other)：
    * 项目暂时没用Scrapy进行编写,考虑到第一版测试以及使用的便捷性上,暂时不使用Scrapy。
      This project not coding by Scrapy,think of the first version and easy using,so I just not coding by Scrapy
    * 后续版本可能推出基于Scrapy + Redis的分布式爬虫。
      After version maybe commit a distributed spider based on Scrapy + redis

### 需求分析(Command analyse) --- Why I code this project
>起初，只是帮助同学完成R语言的数据分析课程设计，后来自己一步一步完善代码，逐步完善代码，变成一个小项目
并上传到github与大家分享。代码目前主要实现的只是简单的评论抓取以及存储，存储方式主要是以csv和mongodb
为主，后续会添加更多的存储方式，以及完善代码的不足的地方。

>At first,this code just only help my friend to finish the R data analyse curriculum design and
i continue to complete the code step by step,to become a small project and upload to Github share
with us.This project just complete the sample comment catch and save right now,the saving mode just
only CSV and MongoDB.I will add more saving mode in after version,and debug.

## 功能（Fuction）
1.抓取京东商品评论，保存到本地。（默认设置了两种存储方式csv和mongoDB）

Get the product comment on JingDong online shop,saved to the local file system.(Default way:CSV and MongoDB)

2.用户使用时需要手动选择存储方式以及填写商品id号
Ps:(https://item.jd.com/10677596338.html) ID号就是后面的数字

User use it need manually choose the saving mode and fill in product ID.
Example:(https://item.jd.com/10677596338.html) ID is number at the last of URL.

## 实现方式（How to Work）
1. 主要利用python urllib库以及json解析库，实现对于评论的json页面的请求。因为减少被京东后台ban掉次数的原因，加入一大堆
  user-agent库,然后设置一个随机数，产生随机时间去后台请求json数据

    * Use python urllib and json,to complete the post to the json page.For reduce ban by JingDong online shop
      server,so I add a user-agent pool to change the user-agent in each post,then i set random number to make
      a random time to send the request.

2. 利用Beautifulsoup中的一个decode方法解决了json中文乱码的编码问题。
    * Use BeautifulSoup`s decode function to solve the encoding error in json with Chinese word.
3. 加入了pymongo和csv库将数据转换成可视化数据，存储到文档数据库和文本表格数据形式。
    * add pymongo and csv lib for tranfer the string or list to visualization data,save in the document database(MongoDB)
      an text table data(CSV)
4. 后续补充...
    * To be Continue...

## 问题（BUG）
1.抓取时间较长(It cost long time to get the data)
* 原因：因为京东后台对于爬虫很敏感，很容易被ban掉，导致程序出错，虽然项目中加入了判断json是否为空，但是
京东后台会对IP的进行长时间的封禁，导致一段时间内无法获取数据，对此进行了粗暴的time.sleep的方法，睡眠爬虫一段时
间后再次进行请求，循环至有返回结果才继续。
* Reason:Because the background server of JingDong is sensetive with Spider,is easy to ban it,caused the
 code raise warning.When judge the json if is not empty,cycle judgement is end.
 But JingDong server is very clever,it will ban my IP for a long time ,let my spider could not get the response
 ,so i add a function by time lib (time.sleep(90),it will stay 90s then countinue request).Also is a cycle juagement
 ,utill the response is not empty.


2.CSV空行问题(csv file with empty row after each data row)
* 原因：暂时不太明白为什么会产生这种问题，后续通过请教大神解决这个问题
* Reason:I don`t still why it cause this problem,then I ask for help later.

## 更新日志（Update Log）
### 第一版本（2017-01-06）
1.实现基本功能，并能完成数据的存取，但是耗时较长。
2.没有MongoDB的用户目前只能选择csv方式，在下个版本中将会对这个问题进行解决。
3.目前还无法对于json中的选项进行选择，在后续版本可能会进行添加。
4.CSV存取后会在每一行数据后面自动空行，这个问题暂时找不到办法解决，在后续版本会进行解决。


