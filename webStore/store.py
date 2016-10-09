# -*- coding: utf-8 -*-
from systemUtils.util import *

class Store(Store):

    def __init__(self):
        pass

    @retry(5)
    @timeout(30)
    def get_url_content(self, web_url):
        # Owner：11602272
        # CreateTime：2015年5月15日
        # ModifyTime：
        # 函数参数： 请求地址，Proxy
        # 函数方法：访问被请求的web_url返回响应结果
        # 函数返回值：req
        try:
            req = requests.get(web_url, proxies=Store.default_proxy)
#             logger.debug("Web request is : %s" % req, "on")
        except requests.exceptions.ConnectionError as e:
            logger.error('Connection %s was lost,please check the network.' % web_url, "on")
            raise "Connection was lost,please check the network."
        except Exception, e:
            logger.error("error is %s" % e, "on")
            raise "error is %s" % e
        else:
            return req

    def get_apk_list(self):
        # Owner：11602272
        # CreateTime：2015年5月15日
        # ModifyTime：
        # 函数参数：
        # 函数方法：返回指定排名的app列表，列表包括APP名字，版本号，下载链接
        # 函数返回值：remote_apk_info,['com.tianmashikong.qmqj.bd', '1.4.1', 'http://gdown.baidu.com/data/wisegame/cce33f84449b99f2/quanminqiji_141.apk', '.apk']
        remote_apk_info = []
        return remote_apk_info
