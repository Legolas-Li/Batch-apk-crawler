# -*- coding: utf-8 -*-
from systemUtils.util import *

class MultiThreadDownload:

    WIN_INVALID_CHAR_SET = ['/', '\\', ':', '*', '?', '"', '<', '>', ',']

    def __init__(self):
        pass

    @timeout(7200)
    def downloader_multi_thread(self, need_download_apk_dictionary):
        # Owner：11602272
        # CreateTime：2015年5月9日
        # ModifyTime：
        # 函数参数：1.需要下载的apk，2.proxy
        # 函数方法：多任务同时并发下载
        # 函数返回值：null
        web_url_list = need_download_apk_dictionary.values()
        apk_name_list = need_download_apk_dictionary.keys()
        while web_url_list != [] and apk_name_list != []:
            if threading.activeCount() <= int(Store.default_max_thread_number) + 2:
                t = threading.Thread(target=self.mt_downloader, args=(apk_name_list[0], web_url_list[0], len(apk_name_list)))
                t.start()
                web_url_list.remove(web_url_list[0])
                apk_name_list.remove(apk_name_list[0])
            else:
                time.sleep(3)
        while threading.activeCount() > 2 :
            time.sleep(8)
            logger.info("Please wait, the APP downloading is still underway...threading.activeCount() is %s" % threading.activeCount(), "on")

    @retry(3)
    def mt_downloader(self, apk_name, web_url, length):
        # Owner：11602272
        # CreateTime：2015年5月8日
        # ModifyTime：
        # 函数参数：1.文件名，2.下载地址，3.proxy
        # 函数方法：单个文件下载保存
        # 函数返回值：null
        try:
            logger.info("%s Downloading start %s " % (length, apk_name) , "on")
            if type(web_url) == list:
                url = web_url[0]
                headers = web_url[1]
                cookies = web_url[2]
                if url and cookies:
                    request = requests.get(url, headers=headers, cookies=cookies, proxies=Store.default_proxy)
                else:
                    logger.error("You can't download apps that %s aren't compatible with your device or not available in your country. Try to change your devices in the XML!" % apk_name, "on")
                    Store.apk_debug_dict[apk_name] = Store.apk_debug_dict[apk_name] + ["You can't download apps that %s aren't compatible with your device or not available in your country. Try to change your devices in the XML!" % apk_name]
            else:
                request = requests.get(web_url, proxies=Store.default_proxy)
        except Exception as e:
            logger.error("Failed to requests %s due to %s" % (apk_name, e), "on")
            pass
        else:
            if os.path.exists(Store.default_apk_save_path) == False:
                FloderHandel().create_apk_folder(Store.default_apk_save_path)
            try:
                with open (Store.default_apk_save_path + os.path.sep + apk_name, 'wb') as apk:
                    apk.write(request.content)
            except Exception as e:
                logger.error("Failed to write %s due to %s" % (Store.default_apk_save_path + os.path.sep + apk_name, e), "on")
                Store.apk_debug_dict[apk_name] = Store.apk_debug_dict[apk_name] + ["Failed to write %s due to %s" % (Store.default_apk_save_path + os.path.sep + apk_name, e)]
                raise "Failed to write %s due to %s" % (Store.default_apk_save_path + os.path.sep + apk_name, e)
            except:
                pass
        if os.path.isfile(Store.default_apk_save_path + os.path.sep + apk_name):
            logger.info("%s Downloaded Finish %s" % (length, apk_name) , "on")

    def offline_download(self, need_copy_apk_list, remote_apk_info, apk_save_path, apk_offline_download_path):
        # Owner：11602272
        # CreateTime：2015年5月9日
        # ModifyTime：
        # 函数参数：1.web上apk信息,2.本地apk保存的目录，3.需要复制到的新地址
        # 函数方法：复制该复制的apk
        # 函数返回值：null
        for i in remote_apk_info:
            apk_name = i[0]
            for j in self.WIN_INVALID_CHAR_SET:
                if apk_name.count(j) > 0:
                    apk_name = apk_name.replace(j, ' ')
                else:
                    pass
            if apk_name != i[0]:
                i[0] = apk_name
            else:
                pass
        self.copy_apk(apk_save_path, apk_offline_download_path, need_copy_apk_list)

    def copy_apk(self, apk_save_path, apk_offline_download_path, apk_list, without_version=False):
        # Owner：11602272
        # CreateTime：2015年5月9日
        # ModifyTime：
        # 函数参数：1.本地原先apk保存地址，2.需要复制到的目标地址，3.需要负值的apk列表，4.复制时是否携带版本信息（默认否）
        # 函数方法：复制apk
        # 函数返回值：
        if apk_save_path == apk_offline_download_path:
            return
        else:
            second_copy_list = []
            for i in apk_list:
                try:
                    logger.info('Copying %s ...' % i, "on")
                except Exception, e:
                    pass
                try:
                    if without_version:
                        shutil.copyfile(apk_save_path + os.path.sep + i, apk_offline_download_path + os.path.sep + i.split('_')[0] + i[-4:])
                        os.chdir(os.path.split(sys.argv[0])[0])
                    else:
                        shutil.copyfile(apk_save_path + os.path.sep + i, apk_offline_download_path + os.path.sep + i)
                        os.chdir(os.path.split(sys.argv[0])[0])
                except IOError as e:
                    second_copy_list.append(i)
                except:
                    logger.error("Unexpected error: %s" % sys.exc_info()[0], "on")
                    pass
            if len(second_copy_list) > 0:
                for i in second_copy_list:
                    try:
                        logger.info('Copying %s again...' % i, "on")
                    except Exception, e:
                        pass
                    try:
                        if without_version:
                            shutil.copyfile(apk_save_path + os.path.sep + i, apk_offline_download_path + os.path.sep + i.split('_')[0] + i[-4:])
                            os.chdir(os.path.split(sys.argv[0])[0])
                        else:
                            shutil.copyfile(apk_save_path + os.path.sep + i, apk_offline_download_path + os.path.sep + i)
                            os.chdir(os.path.split(sys.argv[0])[0])
                    except IOError as e:
                        pass
                    except:
                        logger.error("Unexpected error: %s" % sys.exc_info()[0], "on")
                        pass
            else:
                pass
