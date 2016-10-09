# -*- coding: utf-8 -*-
from systemUtils.util import *

class Xiaomi(Store):
    GENERAL_FILE_EXTENSION = ".apk"
    xiaomi_store_prefix = "http://app.mi.com/"
    package_cookies = {}
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
        url = {"application":"topList", "game":"gTopList",
                u"实用工具":"5", u"影音视听":"27",
                u"聊天与社交":"2", u"图书与阅读":"7",
                u"学习与教育":"12", u"效率办公":"10",
                u"时尚与购物":"9", u"生活":"4",
                u"旅行与交通":"3", u"摄影摄像":"6",
                u"医疗与健康":"14", u"体育运动":"8",
                u"新闻":"11", u"娱乐消遣":"13",
                u"理财":"1",
                u"战争策略":"16", u"动作枪战":"17",
                u"赛车体育":"18", u"网游RPG":"19",
                u"棋牌桌游":"20", u"格斗快打":"21",
                u"儿童益智":"22", u"休闲创意":"23",
                u"飞行空战":"25", u"跑酷闯关":"26",
                u"塔防迷宫":"28", u"模拟经营":"29",
             }
        for category in Store.default_apk_category:
#             logger.debug("category is %s , value is %s" % (category, url.get(category)), "on")
            category_selection.append(url.get(category))
        return category_selection

    @retry(5)
    def get_apk_content(self, detail_url):
        req = self.get_url_content(detail_url)
        content = req.content.decode("utf-8")
        tree = lxml.html.fromstring(content)
        dl_url_match = tree.xpath("//a[@class='download']")
        detail_info_match = tree.xpath("//ul[@class=' cf']//li")
        apk_name = detail_info_match[7].text
        apk_version = detail_info_match[3].text
        apk_dl_url = self.xiaomi_store_prefix[:-1] + dl_url_match[0].values()[0]
        self.package_cookies[detail_url] = [apk_name, apk_version, apk_dl_url]
        if apk_name and apk_version and apk_dl_url:
            logger.info("Get %s download url, version succees!" % apk_name, "on")
        else:
            logger.error("Get detail_url %s fail." % detail_url, "on")

    @timeout(1500)
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
        logger.debug("category_selection is %s" % category_selection, "on")
        detail_list = []
        for cid in category_selection:
            if cid == "topList" or cid == "gTopList":
                apk_number_per_page = 48
                page_number = int(Store.default_download_end) / apk_number_per_page
                if int(Store.default_download_end) < apk_number_per_page or int(Store.default_download_end) % apk_number_per_page != 0:
                    page_number = page_number + 1
                count = 0
                for i in range(1, page_number + 1):
                    url = self.xiaomi_store_prefix + cid + '?page=' + str(i)
                    logger.debug("Weburl is %s" % url, "on")
                    req = self.get_url_content(url)
                    content = req.content.decode("utf-8")
                    tree = lxml.html.fromstring(content)
                    all_match = tree.xpath("//h5//a[@href]")
                    for e in all_match:
                        if e.values() != '':
                            if count < int(Store.default_download_begin) - 1:
                                count = count + 1
                                continue
                            count = count + 1
                            if count > int(Store.default_download_end):
                                break
                            detail_url = self.xiaomi_store_prefix[:-1] + e.values()[0]
                            detail_list.append(detail_url)
            else:
                apk_number_per_page = 30
                page_number = (int(Store.default_download_end) - 12) / apk_number_per_page
                if (int(Store.default_download_end) - 12) < apk_number_per_page or (int(Store.default_download_end) - 12) % apk_number_per_page != 0:
                    page_number = page_number + 1
                count = 0
#                 logger.debug("cid is %s ,page_number is %s" % (cid, page_number), "on")
                for i in range(0, page_number + 1):
                    url = self.xiaomi_store_prefix + 'category/' + str(cid) + '#page=' + str(i)
                    logger.debug("Weburl is %s" % url, "on")
                    req = self.get_url_content(url)
                    content = req.content.decode("utf-8")
                    tree = lxml.html.fromstring(content)
                    all_match = tree.xpath("//h5//a[@href]")
                    if i > 0:
                        all_match = all_match[12:]
                    for e in all_match:
                        if e.values() != '':
                            if count < int(Store.default_download_begin) - 1:
                                count = count + 1
                                continue
                            count = count + 1
                            if count > int(Store.default_download_end):
                                break
                            detail_url = self.xiaomi_store_prefix[:-1] + e.values()[0]
                            detail_list.append(detail_url)
                        else:
                            pass
            logger.debug("cid is %s len(detail_list) is %s %s" % (cid, len(detail_list), detail_list), "on")
        get_content_by_detail_list = detail_list + []
        while get_content_by_detail_list:
            if threading.activeCount() <= int(Store.default_max_thread_number) + 2:  #    Get download url 30 threading at the same time
                t = threading.Thread(target=self.get_apk_content, args=(get_content_by_detail_list[0],))
                t.start()
                get_content_by_detail_list.remove(get_content_by_detail_list[0])
            else:
                time.sleep(3)
        while threading.activeCount() > 2:
            time.sleep(8)
            logger.info("Please wait, Parseing detail_list web is still underway...threading.activeCount() is %s" % threading.activeCount(), "on")
        logger.debug("self.package_cookies is %s" % self.package_cookies, "on")
        for i in detail_list:
            remote_apk_info.append([self.package_cookies[i][0], self.package_cookies[i][1], self.package_cookies[i][2],self.GENERAL_FILE_EXTENSION])
            Store.apk_debug_dict[self.package_cookies[i][0] + "_" + self.package_cookies[i][1] + self.GENERAL_FILE_EXTENSION] = []
        logger.debug("remote_apk_info is %s" % remote_apk_info, "on")
        return remote_apk_info
