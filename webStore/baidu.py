# -*- coding: utf-8 -*-
from systemUtils.util import *

class Baidu(Store):
    GENERAL_FILE_EXTENSION = ".apk"

    def __init__(self):
        pass

    @timeout(30)
    def get_url_content(self, web_url):
        # Owner：11602272
        # CreateTime：2015年5月15日
        # ModifyTime：
        # 函数参数： 请求地址，Proxy
        # 函数方法：访问被请求的web_url返回响应结果
        # 函数返回值：req
        return Store.get_url_content(self, web_url)

    def get_category_info(self):
        # Owner：11602272
        # CreateTime：2015年6月1日
        # ModifyTime：
        # 函数参数： 用户配置的下载标签
        # 函数方法：匹配web标签的web_uil信息
        # 函数返回值：category_selection
        category_selection = []
        url = {"application":"101", "game":"102",
                u"系统工具":["software", "501"], u"主题壁纸":["software", "502"],
                u"社交通讯":["software", "503"], u"生活实用":["software", "504"],
                u"资讯阅读":["software", "505"], u"影音播放":["software", "506"],
                u"办公学习":["software", "507"], u"拍摄美化":["software", "508"],
                u"旅游出行":["software", "509"], u"理财购物":["software", "510"],
                u"休闲益智":["game", "401"], u"角色扮演":["game", "402"],
                u"动作射击":["game", "403"], u"模拟辅助":["game", "404"],
                u"体育竞技":["game", "405"], u"赛车竞速":["game", "406"],
                u"棋牌桌游":["game", "407"], u"经营养成":["game", "408"],
                u"网络游戏":["game", ""],
             }
        for category in Store.default_apk_category:
            category_selection.append(url.get(category))
        return category_selection

    @timeout(300)
    def get_apk_list(self):
        # Owner：11602272
        # CreateTime：2015年5月8日
        # ModifyTime：2015年6月2日
        # 函数参数：1.Proxy,2.排名开始，3.排名结束，4.APP分类类型
        # 函数方法：返回指定排名的app列表，列表包括APP名字，版本号，下载链接
        # 函数返回值：all_download_info,['com.tianmashikong.qmqj.bd', '1.4.1', 'http://gdown.baidu.com/data/wisegame/cce33f84449b99f2/quanminqiji_141.apk', '.apk']
#         ("",1,600,2,r"C:\Users\yangli4x\Downloads\Baidu",r"C:\Users\yangli4x\Downloads\Baidu600")
        remote_apk_info = []
        category_selection = self.get_category_info()
#         logger.debug("category_selection is %s" % category_selection, "on")
        apk_number_per_page = 40
        for cid in category_selection:
            page_number = int(Store.default_download_end) / apk_number_per_page + 1
            if int(Store.default_download_end) % apk_number_per_page != 0:
                page_number = page_number + 1
            count = 0
            if cid == "101" or cid == "102":
                for i in xrange(1, page_number):
                    web_url = "http://as.baidu.com/a/rank?cid=" + cid + "&s=1&pn=" + str(i)
                    logger.debug("web_url is %s" % web_url, "on")
    #                 http://as.baidu.com/a/rank?cid=0&s=101&pn=1
                    req = self.get_url_content(web_url)
                    content = req.content.decode("utf-8")
                    tree = lxml.html.fromstring(content)
                    all_match = tree.xpath("//a[@data-download_url]")
                    for i in range(0, len(all_match)):
                        if count < int(Store.default_download_begin) - 1:
                            count = count + 1
                            continue
                        count = count + 1
                        if count > int(Store.default_download_end):
                            break
                        remote_apk_info.append([all_match[i].values()[7], all_match[i].values()[5], all_match[i].values()[8], self.GENERAL_FILE_EXTENSION])
                        Store.apk_debug_dict[all_match[i].values()[7] + "_" + all_match[i].values()[5] + self.GENERAL_FILE_EXTENSION] = []
#                        logger.debug("cid is:%s len(remote_apk_info) is:%s" % (cid, len(remote_apk_info)), "on")
            else:
                for i in xrange(1, page_number):
                    web_url = "http://shouji.baidu.com/" + cid[0] + "/list?cid=" + str(cid[1]) + "&page_num=" + str(i)
                    logger.debug("web_url is %s" % web_url, "on")
    #                     http://shouji.baidu.com/software/list?cid=501
                    req = self.get_url_content(web_url)
                    content = req.content.decode("utf-8")
                    tree = lxml.html.fromstring(content)
                    all_match = tree.xpath("//span[@data_url]")
                    for i in range(0, len(all_match)):
                        if count < int(Store.default_download_begin) - 1:
                            count = count + 1
                            continue
                        count = count + 1
                        if count > int(Store.default_download_end):
                            break
                        remote_apk_info.append([all_match[i].values()[10], all_match[i].values()[11], all_match[i].values()[7], self.GENERAL_FILE_EXTENSION])
                        Store.apk_debug_dict[all_match[i].values()[10]+"_"+all_match[i].values()[11]+self.GENERAL_FILE_EXTENSION] = []
#                        logger.debug("cid is:%s len(remote_apk_info) is:%s" % (cid[0], len(remote_apk_info)), "on")
        logger.debug("remote_apk_info is %s len %s" % (remote_apk_info, len(remote_apk_info)), "on")
        return remote_apk_info
