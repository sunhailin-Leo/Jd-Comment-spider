# Jd-Comment-spider --- v0.1 beta

### 功能详情（Fuction Details）

* csvfile_writer.py
    * 实现csv的写入，以及将json返回的页面数据切片等分。
    * Complete the fuction of csv writing,and spilt the json
* Jd_main.py
    * 主函数，实现爬虫的主要功能（请求页面，解析页面），以及实现了错误的判断。
    * Main fuction.Complete spider`s main function(request,analyse),and judge the error.
* logger_writer.py
    * 实现了由Jd_main传递过来的出错的页面（编码错误，页面存在特殊字符）的记录，并输出成
    一个txt文档，后续版本将更新对于Error_list.txt中出错页面记录的重测。
    * Complete log the error page number,and save in the txt.In the next version,will
    add a function about this txt retest.
* mongodb_writer.py
    * 实现了对于mongodb的存取功能
    * Complete the fuction of MongoDB writing
* user_agent_pool.py
    * 定义了一个user_agent_pool,Jd_main调用其List,利用随机数抽取其中一条user-agent,然后进行请求。
    * Define a list user_agent_pool then Jd_main use it by random number to get it one in list to request the server.