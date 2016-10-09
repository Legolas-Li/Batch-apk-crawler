# -*- coding: utf-8 -*-
from systemUtils.util import *

# AppCrawler starts
if __name__ == "__main__":

    STORE = {
        "baidu": Baidu(),
        "xiaomi": Xiaomi(),
        "wandoujia": Wandoujia(),
        "googlePlay": GooglePlay(),
        "houdini": Houdini(),
    }

    for store in Config.default_store:
        ApkInfoHandle = ApkInfoHandle()
        ParseConfig().reload(store)
        if store == "googlePlay":
            if Store.default_download_loacal_list == "True":
                remote_apk_info = STORE[store].get_apk_list()
                need_download_apk_dictionary, need_copy_apk_list = ApkInfoHandle.get_local_apk_version(remote_apk_info)
                MultiThreadDownload().downloader_multi_thread(need_download_apk_dictionary)
                sys.exit(0)
            else:
                remote_apk_info = STORE[store].get_apk_list()
        else:
            remote_apk_info = STORE[Store.default_store_store].get_apk_list()
        # print "Store.apk_debug_dict", Store.apk_debug_dict, len(Store.apk_debug_dict)

        need_download_apk_dictionary, need_copy_apk_list = ApkInfoHandle.get_local_apk_version(remote_apk_info)

        #     MultiThreadDownload().offline_download(remote_apk_info, need_copy_apk_list, Store.default_apk_save_path, Store.default_apk_offline_download_path)

        MultiThreadDownload().downloader_multi_thread(need_download_apk_dictionary)

        apk_aapt_content = ApkInfo().get_aapt_content(remote_apk_info)

        apk_info_jason_list = ApkInfoHandle.get_apk_upload_info(remote_apk_info, need_download_apk_dictionary,
                                                                apk_aapt_content)

        rank_info_jason_list = ApkInfoHandle.get_apk_rank_upload_info(remote_apk_info, apk_aapt_content)

        Upload().copy_to_file_server()

        logger.info("apk_info_jason = %s" % apk_info_jason_list, "on")

        logger.info("rank_info_jason = %s" % rank_info_jason_list, "on")

        Upload().send_to_web_server(Config.default_web_apk_api, apk_info_jason_list)

        Upload().send_to_web_server(Config.default_web_rank_api, rank_info_jason_list)
