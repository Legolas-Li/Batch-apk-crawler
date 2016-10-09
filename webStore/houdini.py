# -*- coding: utf-8 -*-
from systemUtils.util import *

class Houdini(Store):
    GENERAL_FILE_EXTENSION = ".apk"

    def __init__(self):
        pass

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
        for root, dirs, files in os.walk(Store.default_apk_save_path):
            for filename in files:
                #                 logger.debug("root is %s filename is %s" % (root, fn), "on")
                file_path = os.path.join(root, filename)
                if file_path and (os.path.splitext(file_path)[1] == ".apk"):
                    if len(filename.split("-")) != 1:
                        new_name = filename.split("-")[0] + "_" + filename.split("-")[1][:-4] + self.GENERAL_FILE_EXTENSION
                        os.rename(file_path, os.path.join(root, new_name))
                        file_path = new_name
                    else:
                        pass
                    logger.debug("Filename is %s Version is %s" % (os.path.basename(file_path).split("_")[0], os.path.basename(file_path).split("_")[1][:-4]), "on")
                    remote_apk_info.append([os.path.basename(file_path).split("_1.apk")[0], "1", file_path, self.GENERAL_FILE_EXTENSION])
                    Store.apk_debug_dict[os.path.basename(file_path)] = []
                else:
                    pass
        logger.debug("remote_apk_info is %s" % remote_apk_info, "on")
        return remote_apk_info