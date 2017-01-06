# -*- coding:utf-8 -*- #
'''
@author: Leo
'''
# 导出错误的log文件
def export_error_log(error_list, file_path):
    # 创建文件流，写入list中的内容
    file = open( file_path + '\\error_list.txt', 'w')
    for data in error_list[:-1]:
        file.write(str(data) + '\n')
    file.close()