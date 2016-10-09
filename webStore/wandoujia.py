# -*- coding: utf-8 -*-
from systemUtils.util import *

class Wandoujia(Store):
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
        url = {"application":u"app", "game":u"game",
             }
        for category in Store.default_apk_category:
            category_selection.append(url.get(category))
        return category_selection

    @timeout(60)
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
        url_prefix = "http://apps.wandoujia.com/api/v1/apps?type=top"
        apk_number_per_page = 60
        if Store.default_download_loacal_list == "True":
            logger.info("Download from local list %s" % Store.default_apk_local, "on")
            with open (Store.default_apk_local ,"r") as app_list_file:
                for package_name in app_list_file.readlines():
                    remote_apk_info.append([package_name.strip(), time.strftime("%Y-%m-%d", time.localtime()), 'http://apps.wandoujia.com/apps/' + package_name.strip() + '/download', self.GENERAL_FILE_EXTENSION])
                    Store.apk_debug_dict[package_name.strip() + "_" + time.strftime("%Y-%m-%d", time.localtime()) + self.GENERAL_FILE_EXTENSION] = []
        else:
            logger.info("Download from online top list http://apps.wandoujia.com/apps/xxx/download ", "on")
            for cid in category_selection:
                page_number = int(Store.default_download_end) / apk_number_per_page + 1
                if int(Store.default_download_end) % apk_number_per_page != 0:
                    page_number = page_number + 1
                count = 0
                if cid == "app" or cid == "game":
                    for i in xrange(1, page_number):
                        web_url = url_prefix + str(cid) + "&max=60&start=" + str(count) + "&opt_fields=apks.packageName,apks.versionName"
    #                     http://apps.wandoujia.com/api/v1/apps?type=topapp&max=60&start=0&opt_fields=apks.packageName,apks.versionName
                        req = self.get_url_content(web_url)
                        content = req.content.decode("utf-8")
                        all_match = json.loads(content)
                        for i in all_match:
                            if count < int(Store.default_download_begin) - 1:
                                count = count + 1
                                continue
                            count = count + 1
                            if count > int(Store.default_download_end):
                                break
                            remote_apk_info.append([i.values()[0][0].get("packageName"), i.values()[0][0].get("versionName"), 'http://apps.wandoujia.com/apps/' + i.values()[0][0].get("packageName") + '/download', self.GENERAL_FILE_EXTENSION])
                            Store.apk_debug_dict[i.values()[0][0].get("packageName") + "_" + i.values()[0][0].get("versionName") + self.GENERAL_FILE_EXTENSION] = []
                else:
                    pass
        logger.debug("remote_apk_info is %s" % remote_apk_info, "on")
        return remote_apk_info
