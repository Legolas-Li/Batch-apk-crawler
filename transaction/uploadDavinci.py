# -*- coding: utf-8 -*-
from systemUtils.util import *

class Upload:

    def __init__(self):
        pass

    @timeout(20)
    def send_to_web_server(self, web_api, data):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：
        # 函数参数：1.服务器接收地址，2.Jason格式的数据
        # 函数方法：上传数据到服务器接口
        # 函数返回值：null
        for upload in data:
            r = requests.post(web_api, upload)
            logger.debug("Web response is %s" % r.content, "on")
        logger.info('Successfully! Please see apkCrawler log.', "on")

    def copy_to_file_server(self):
        # Owner：11602272
        # CreateTime：2015年5月20日
        # ModifyTime：
        # 函数参数：1.本地apk保存跟目录，2服务器保存apk的根目录，3.服务器保存icon的根目录
        # 函数方法：上传apk和icon到文件服务器并清空本地文件夹
        # 函数返回值：null
        local_apk_upload_path = Store.default_apk_save_path + os.path.sep + "upload" + os.path.sep + "apk" + os.path.sep
        local_icon_upload_path = Store.default_apk_save_path + os.path.sep + "upload" + os.path.sep + "icon" + os.path.sep
        local_ranking_upload_path = Store.default_apk_save_path + os.path.sep + "upload" + os.path.sep + "ranking"
        if os.path.isdir(local_apk_upload_path):
            re = FloderHandel().copy_apk_folder(local_apk_upload_path, Config.default_server_apk_folder)
            if re == 0 :
                if os.path.isdir(local_apk_upload_path):
                    try:
                        shutil.rmtree(local_apk_upload_path)
                    except Exception as e:
                        logger.error("shutil.rmtree error %s" % e, "on")
                else:
                    pass
            else:
                logger.error("Return value is %s" % re, "on")
        else:
            logger.warn("Def copy_to_file_server Can't find local_apk_upload_path %s" % (local_apk_upload_path), "on")
        if os.path.isdir(local_icon_upload_path):
            re = FloderHandel().copy_apk_folder(local_icon_upload_path, Config.default_server_icon_folder)
            if re == 0 :
                if os.path.isdir(local_icon_upload_path):
                    try:
                        shutil.rmtree(local_icon_upload_path)
                    except Exception as e:
                        logger.error("shutil.rmtree error %s" % e, "on")
                else:
                    pass
            else:
                logger.error("Return value is %s" % re, "on")
        else:
            logger.warn("Def copy_to_file_server Can't find local_icon_upload_path %s" % (local_icon_upload_path), "on")
        if os.path.isdir(local_ranking_upload_path):
            commend = "xcopy /e /s /y %s\* %s" % (local_ranking_upload_path, Config.default_server_ranking_folder)
            re = os.system(commend)
            logger.debug("Commend is %s return %s " % (commend, re), "on")
            if re == 0 :
                if os.path.isdir(local_ranking_upload_path):
                    try:
                        shutil.rmtree(local_ranking_upload_path, ignore_errors=True)
                    except Exception as e:
                        logger.error("shutil.rmtree error %s" % e, "on")
                else:
                    pass
            else:
                logger.error("Commend is %s Block %s" % (commend, re), "on")
        else:
            logger.warn("Def copy_to_file_server Can't find local_apk_upload_path %s" % (local_ranking_upload_path), "on")