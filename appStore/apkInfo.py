# -*- coding: utf-8 -*-

from systemUtils.util import *

class ApkInfo:
    aapt_content_map = {}
    def __init__(self):
        pass

    @retry(3)
    @timeout(120)
    def sent_aapt(self, apk):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：2015年5月12日
        # 函数参数：传入apk文件
        # 函数方法：发送aapt dump命令
        # 函数返回值：返回aapt反馈信息
        if os.path.isfile(apk):
            command = "%s dump badging \"%s\" " % (Config.default_aapt_save_path, apk)
            aapt_result = os.popen(command)
            self.aapt_content_map[os.path.basename(apk)] = aapt_result.readlines()
        else:
            logger.error("Can't get_aapt_content, Lost Apk file %s" % apk, "on")
            Store.apk_debug_dict[os.path.basename(apk)] = Store.apk_debug_dict[os.path.basename(apk)] + ["Can't get_aapt_content, Lost Apk file %s" % apk]

    @timeout(3600)
    def get_aapt_content(self, remote_apk_info):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：2015年5月12日
        # 函数参数：1.文件名，2.apk目录
        # 函数方法：发送aapt dump命令,获取返回的命令
        # 函数返回值：返回aapt反馈信息的数组
        remote_apk_info_list = remote_apk_info + []
        while remote_apk_info_list:
            if threading.activeCount() <= int(Store.default_max_thread_number) + 1:
                file_name = remote_apk_info_list[0][0] + '_' + remote_apk_info_list[0][1] + remote_apk_info_list[0][3]
                logger.debug("%s aapt dump badging %s" % (len(remote_apk_info_list), file_name), "on")
                t = threading.Thread(target=self.sent_aapt, args=(Store.default_apk_save_path + os.path.sep + file_name,))
                t.start()
                remote_apk_info_list.remove(remote_apk_info_list[0])
            else:
                time.sleep(3)
        while threading.activeCount() > 2 :
            time.sleep(8)
            logger.info("Please wait, the get_aapt_content is still underway...threading.activeCount() is %s" % threading.activeCount(), "on")
        logger.info("aapt_content_map = %s" % self.aapt_content_map, "on")
        return self.aapt_content_map
