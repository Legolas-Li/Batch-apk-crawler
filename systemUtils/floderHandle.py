# -*- coding: utf-8 -*-
from systemUtils.util import *

class FloderHandel:
    fail_times = 0
    def __init__(self):
        pass

    def create_apk_folder(self, folder_path):
        # Owner：11602272
        # CreateTime：2015年5月8日
        # ModifyTime：
        # 函数参数：文件地址
        # 函数方法：创建文件夹
        # 函数返回值：空
        try:
            # if os.path.exists(folder_path) == True:
            #     shutil.rmtree(folder_path)
            if os.path.exists(folder_path) == False:
                os.makedirs(folder_path)
        except WindowsError, e:
            logger.warn('create %s failed, using %s as save path' % (folder_path, os.getcwd()))
        else:
            os.chdir(folder_path)

    def copy_apk_file(self, src, dst):
        # Owner：11602272
        # CreateTime：2015年7月8日
        # ModifyTime：
        # 函数参数：源文件，目标文件
        # 函数方法：复制文件
        # 函数返回值：空
        try:
            logger.info("Copying file %s to %s" % (src, dst), "on")
            shutil.copy(src, dst)
        except Exception as e:
            logger.error("Copying file %s fail %s" % (src, e), "on")
            self.fail_times += 1

    def copy_apk_folder(self, root_folder, destination_folder):
        # Owner：11602272
        # CreateTime：2015年7月8日
        # ModifyTime：
        # 函数参数：目录地址,目标目录地址
        # 函数方法：复制文件夹
        # 函数返回值：空
        copy_file_map = {}
        for parent, dirnames, filenames in os.walk(root_folder):
            for filename in filenames:
                if os.path.exists(destination_folder + os.path.sep + parent[-5:]):
                    copy_file_map[os.path.join(parent, filename)] = destination_folder + os.path.sep + parent[-5:]
                else:
                    self.create_apk_folder(destination_folder + os.path.sep + parent[-5:])
                    copy_file_map[os.path.join(parent, filename)] = destination_folder + os.path.sep + parent[-5:]
        logger.info("copy_file_map is %s length is %s" % (copy_file_map,len(copy_file_map)), "on")
        while copy_file_map:
            if threading.activeCount() <= int(Store.default_max_thread_number) + 2:  #    Get download url 30 threading at the same time
                t = threading.Thread(target=self.copy_apk_file, args=(copy_file_map.items()[0][0], copy_file_map.items()[0][1]))
                t.start()
                del copy_file_map[copy_file_map.items()[0][0]]
            else:
                time.sleep(3)
        while threading.activeCount() > 1:
            time.sleep(8)
            logger.info("Please wait, Copying apk file to server is still underway...threading.activeCount() is %s" % threading.activeCount(), "on")
        return self.fail_times
