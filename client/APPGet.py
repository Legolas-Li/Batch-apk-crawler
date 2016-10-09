# -*- coding: utf-8 -*-
import os
import shutil
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json
import subprocess
import thread
import platform

class Config:
    default_apk_local_path = r"C:\Users\yangli4x\Downloads\apk-downloader"
    default_server_apk_folder = r"\\ccr\ec\proj\ssg\dpd\BiTS\DaVinci_Customers\AppTestCloudApk\Apk"
    default_rank_min = 1
    default_rank_max = 0
    default_plantform = ["arm", "x86"]
    default_build_time = "2015-8-04_13-24-56"

def retry(attempt):
    # Owner：11602272
    # CreateTime：2015年6月30日
    # ModifyTime：
    # 函数参数： 重试次数
    # 函数方法：如果函数异常失败则会重新尝试attempt次
    # 函数返回值：function
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    att += 1
#                     logger.debug("%s %s, Retry %s times." % (func, e, att), "on")
                print "%s %s, Retry %s times." % (func, e, att)
        return wrapper
    return decorator

class WatchDog:
    # Owner：11602272
    # CreateTime：2015年7月14日
    # ModifyTime：2015年7月14日
    # 类参数： null
    # 函数方法：一旦Python脚本发生改动，自动重新启动被监听的方法
    def iter_module_files(self):
        for module in sys.modules.values():
            file_name = getattr(module, '__file__', None)
            if file_name:
                if file_name[-4:] in ('.pyo', '.pyc'):
                    file_name = file_name[:-1]
                yield file_name

    def is_any_file_changed(self, mtimes):
        for file_name in self.iter_module_files():
            try:
                mtime = os.stat(file_name).st_mtime
                print "mtime", mtime
            except IOError:
                continue
            old_time = mtimes.get(file_name, None)
            if old_time is None:
                mtimes[file_name] = mtime
            elif mtime > old_time:
                return 1
        return 0

    def start_change_detector(self):
        mtimes = {}
        while 1:
            if self.is_any_file_changed(mtimes):
                sys.exit(3)
            time.sleep(1)

    def restart_with_reloader(self):
        while 1:
            args = [sys.executable] + sys.argv
            new_env = os.environ.copy()
            new_env['RUN_FLAG'] = 'true'
            exit_code = subprocess.call(args, env=new_env)
            if exit_code != 3:
                return exit_code

    def run_with_reloader(self, fun):
        if os.environ.get('RUN_FLAG') == 'true':
            thread.start_new_thread(fun, ())
            try:
                self.start_change_detector()
            except KeyboardInterrupt:
                pass
        else:
            try:
                sys.exit(self.restart_with_reloader())
            except KeyboardInterrupt:
                pass

class DownloadByRank:
    store = ""
    category = ""
    category_history = ""
    plantform = ""
    rank_min = ""
    rank_max = ""
    rank_list = []
    def __init__(self):
        pass

    def assert_platform(self):
#        print "platform.system()",platform.system()
        if 'Windows' in platform.system():
            return "Windows"
        elif 'Linux' in platform.system() or "CYGWIN" in platform.system():
            return "Linux"

    def get_user_input(self, caption, default, hidden_flag=False, timeout=10):
        # Owner：11602272
        # CreateTime：2015年7月3日
        # ModifyTime：
        # 函数参数： 说明标题, 默认值
        # 函数方法：获取用户输入的值
        # 函数返回值：user_input
        sys.stdout.write('%s(Default is %s):\n' % (caption, default));
        os_platform = self.assert_platform()
        if os_platform == "Windows":
            import msvcrt
            start_time = time.time()
            user_input = ''
            while True:
                if msvcrt.kbhit():
                    if hidden_flag:
                        user_input_char = msvcrt.getch()
                    else:
                        user_input_char = msvcrt.getche()
                    if ord(user_input_char) == 13:  # enter_key
                        break
                    elif ord(user_input_char) >= 32:  # space_char
                        user_input += user_input_char
                        if hidden_flag:
                            sys.stdout.write('*')
                if len(user_input) == 0 and (time.time() - start_time) > timeout:
                    break
        elif os_platform == "Linux":
            import select
            print "You have ten seconds to answer!"
            i, o, e = select.select([sys.stdin], [], [], timeout)
            if (i):
                user_input = sys.stdin.readline().strip()
            else:
                user_input = ""
        if len(user_input) > 0:
            return user_input
        else:
            return default


    @retry(10)
    def get_store(self):
        # Owner：11602272
        # CreateTime：2015年7月3日
        # ModifyTime：
        # 函数参数：None
        # 函数方法：获取用户选择的store
        # 函数返回值：空
        print '**********Store Menu*************'
        default_store = os.listdir(Config.default_server_apk_folder + os.path.sep + "ranking")
        for i in range(1, len(default_store) + 1):
            print i, ":", default_store[i - 1]
        print '*********************************'
        ret = self.get_user_input("Please input the number of web store from list", 1)
        if int(ret) not in  range(1, len(default_store) + 1, 1):
            raise "error"
        store = default_store[int(ret) - 1]
#         logger.info("Selected store is: %s.%s \n" % (int(ret), store), "on")
        print "Selected store is: %s.%s \n" % (int(ret), store)
        self.store = store

    @retry(10)
    def get_category(self):
        # Owner：11602272
        # CreateTime：2015年7月3日
        # ModifyTime：
        # 函数参数：None
        # 函数方法：获取用户选择的category
        # 函数返回值：空
        print '**********Category Menu**********'
        default_category = os.listdir(Config.default_server_apk_folder + os.path.sep + "ranking" + os.path.sep + self.store)
        for i in range(1, len(default_category) + 1):
            print i, ":", default_category[i - 1]
        print '*********************************'
        ret = self.get_user_input("Please input the number of app category from list", 1)
        if int(ret) not in  range(1, len(default_category) + 1, 1):
            raise "error"
        category = default_category[int(ret) - 1]
#         logger.info("Selected category is: %s.%s \n" % (int(ret), category), "on")
        print "Selected category is: %s.%s \n" % (int(ret), category)
        self.category = category

    @retry(10)
    def get_min(self):
        # Owner：11602272
        # CreateTime：2015年7月3日
        # ModifyTime：
        # 函数参数：None
        # 函数方法：获取用户输入的下载开始值
        # 函数返回值：空
        print '********Default_rank_min*********'
        print "default_rank_min is: %s" % Config.default_rank_min
        print '*********************************'
        rank_min = int(self.get_user_input("Please input the number of app category from list", Config.default_rank_min))
        if int(rank_min) < 1 or int(rank_min) > Config.default_rank_max:
            raise "error"
#         logger.info("Selected rank_min is: %s \n" % int(rank_min), "on")
        print "Selected rank_min is: %s \n" % int(rank_min)
        self.rank_min = int(rank_min)

    @retry(10)
    def get_max(self):
        # Owner：11602272
        # CreateTime：2015年7月3日
        # ModifyTime：
        # 函数参数：None
        # 函数方法：获取用户输入的下载最大数量
        # 函数返回值：空
        print '********Default_rank_max*********'
        print "default_rank_max is: %s" % Config.default_rank_max
        print '*********************************'
        rank_max = int(self.get_user_input("Please input the number of app category from list", Config.default_rank_max))
        if int(rank_max) < 0 or int(rank_max) > Config.default_rank_max or int(rank_max) < self.rank_min:
            raise "error"
#         logger.info("Selected rank_max is: %s \n" % rank_max, "on")
        print "Selected rank_max is: %s \n" % rank_max
        self.rank_max = int(rank_max)

    @retry(10)
    def get_plantfrom(self):
        # Owner：11602272
        # CreateTime：2015年7月8日
        # ModifyTime：
        # 函数参数：None
        # 函数方法：获取用户输入的google下载平台
        # 函数返回值：空
        print '********Default_plantform*********'
        for i in range(1, len(Config.default_plantform) + 1):
            print i, ":", Config.default_plantform[i - 1]
        print '*********************************'
        ret = self.get_user_input("Please input the number of device plantform from list", 1)
        if int(ret) not in  range(1, len(Config.default_plantform) + 1, 1):
            raise "error"
        self.plantform = Config.default_plantform[int(ret) - 1]

    @retry(10)
    def get_category_history(self):
        # Owner：11602272
        # CreateTime：2015年7月8日
        # ModifyTime：
        # 函数参数：None
        # 函数方法：获取用户输入的google下载平台
        # 函数返回值：空
        print '**********Category Menu**********'
        default_category_history = os.listdir(Config.default_server_apk_folder + os.path.sep + "ranking" + os.path.sep + self.store + os.path.sep + self.category)[:-11:-1]
        for i in range(1, len(default_category_history) + 1):
            print i, ":", default_category_history[i - 1]
        print '*********************************'
        ret = self.get_user_input("Please input the number of app category from list", 1)
        if int(ret) not in  range(1, len(default_category_history) + 1, 1):
            raise "error"
        category_history = default_category_history[int(ret) - 1]
#         logger.info("Selected category is: %s.%s \n" % (int(ret), category), "on")
        print "Selected category_history is: %s.%s \n" % (int(ret), category_history)
        self.category_history = category_history

    def get_config(self):
        # Owner：11602272
        # CreateTime：2015年7月3日
        # ModifyTime：
        # 函数参数：None
        # 函数方法：判断全部参数是否全部被定义
        # 函数返回值：空
        self.get_store()
        if self.store:
            pass
        else:
            raise "error"
        self.get_category()
        if self.category:
            pass
        else:
            raise "error"

    def load_json_file(self, json_file):
        # Owner：11602272
        # CreateTime：2015年7月8日
        # ModifyTime：
        # 函数参数：json_file
        # 函数方法：加载json文件
        # 函数返回值：空
        with open (json_file, "r") as f:
            rank_jason = json.load(f)
            try:
                self.rank_list = rank_jason["rank"]
            except Exception as e:
                self.rank_list.append(rank_jason)

    def get_download_rank(self):
        # Owner：11602272
        # CreateTime：2015年7月3日
        # ModifyTime：
        # 函数参数：None
        # 函数方法：获取用户输入的需要的下载开始序号和结束序号
        # 函数返回值：空
        for dict in self.rank_list:
            sum = len(dict["apps"])
            if Config.default_rank_max is 0 :
                Config.default_rank_max = sum
            else:
                if sum < Config.default_rank_max:
                    Config.default_rank_max = sum
                else:
                    pass
        self.get_min()
        if self.rank_min:
            pass
        else:
            raise "error"
        self.get_max()
        if self.rank_max:
            pass
        else:
            raise "error"
        return self.rank_min, self.rank_max

    def get_file(self, json_file=None):
        # Owner：11602272
        # CreateTime：2015年7月3日
        # ModifyTime：
        # 函数参数： json文件
        # 函数方法：判断用户是否传入json文件
        # 函数返回值：json_file
        if json_file is not None:
            return json_file
        else:
            if not self.category.find("json") is -1:
                json_file = Config.default_server_apk_folder + os.path.sep + "ranking" + os.path.sep + self.store + os.path.sep + self.category
            else:
                print "self.store is", self.store
                if self.store == "googlePlay":
                    self.get_plantfrom()
                    self.get_category_history()
                    json_file = Config.default_server_apk_folder + os.path.sep + "ranking" + os.path.sep + self.store + os.path.sep + "All_latest_" + self.plantform + ".json"
                else:
                    self.get_category_history()
                    json_file = Config.default_server_apk_folder + os.path.sep + "ranking" + os.path.sep + self.store + os.path.sep + self.category + os.path.sep + self.category_history
        return json_file

    def get_apk(self, apk_server_path, apk_local_path):
        # Owner：11602272
        # CreateTime：2015年7月5日
        # ModifyTime：
        # 函数参数： 服务器文件目录，本地保存目录，json文件
        # 函数方法：得到apk文件
        # 函数返回值：json_file
        for dict in self.rank_list:
            apk_list = []
            if not self.category.find("json") is -1:
                apk_offline_download_path = apk_local_path + os.path.sep + self.store + os.path.sep + dict["datetime"] + os.path.sep + dict["category"]
                if os.path.exists(apk_offline_download_path) == False:
                    self.create_apk_folder(apk_offline_download_path)
                if os.path.isfile(apk_offline_download_path + os.path.sep + "rank.csv") == True:
                    os.remove(apk_offline_download_path + os.path.sep + "rank.csv")
                with open (apk_offline_download_path + os.path.sep + "rank.csv", "a") as rank:
                    for i in dict["apps"]:
                        rank.write(i["name"] + ", " + i["package"] + ", " + i["version"] + ", " + i["apk_path"] + ", " + str(i["debug_info"]) + "\n")
                for i in dict["apps"][self.rank_min - 1:self.rank_max]:
#                     print "apk_path", i["apk_path"]
                    apk_list.append([i["package"], i["version"], i["apk_path"]])
                self.download_from_server(apk_server_path, apk_offline_download_path, apk_list)
            else:
#                 print "dict[\"category\"] is ", type(dict["category"]), "self.category is", type(self.category.decode('gb2312'))
                if dict["category"] == self.category.decode('gb2312'):
                    apk_offline_download_path = apk_local_path + os.path.sep + self.store + os.path.sep + dict["datetime"] + os.path.sep + dict["category"]
                    if os.path.exists(apk_offline_download_path) == False:
                        self.create_apk_folder(apk_offline_download_path)
                    if os.path.isfile(apk_offline_download_path + os.path.sep + "rank.csv") == True:
                        os.remove(apk_offline_download_path + os.path.sep + "rank.csv")
                    with open (apk_offline_download_path + os.path.sep + "rank.csv", "a") as rank:
                        for i in dict["apps"]:
                            rank.write(i["name"] + ", " + i["package"] + ", " + i["version"] + ", " + i["apk_path"] + ", " + str(i["debug_info"]) + "\n")
                    for i in dict["apps"][self.rank_min - 1:self.rank_max]:
#                         print "apk_path", i["apk_path"]
                        apk_list.append([i["package"], i["version"], i["apk_path"]])
                    self.download_from_server(apk_server_path, apk_offline_download_path, apk_list)

    def create_apk_folder(self, folder_path):
        # Owner：11602272
        # CreateTime：2015年5月8日
        # ModifyTime：
        # 函数参数：文件地址
        # 函数方法：创建文件夹
        # 函数返回值：空
        try:
            if os.path.exists(folder_path) == False:
                os.makedirs(folder_path)
        except WindowsError, e:
#             logger.warn('create %s failed, using %s as save path' % (folder_path, os.getcwd()))
            print 'create %s failed, using %s as save path' % (folder_path, os.getcwd())
        else:
            os.chdir(folder_path)

    def download_from_server(self, apk_save_path, apk_offline_download_path, apk_list):
        # Owner：11602272
        # CreateTime：2015年7月6日
        # ModifyTime：
        # 函数参数：1.本地原先apk保存地址，2.需要复制到的目标地址，3.需要负值的apk列表
        # 函数方法：复制apk
        # 函数返回值：
        for i in apk_list:
            try:
#                 logger.info('Copying %s ...' % i, "on")
                print "Copying %s to %s" % (i[2], apk_offline_download_path)
#                 print "apk_save_path + os.path.sep + i[2]", apk_save_path + os.path.sep + i[2]
                shutil.copyfile(apk_save_path + os.path.sep + i[2], apk_offline_download_path + os.path.sep + i[0] + "_" + i[1] + ".apk")
            except Exception as e:
#                 logger.error("Unexpected copy error: %s" % i, "on")
                print "Unexpected copy error: %s, %s" % (e, i)

    def downloader(self, apk_server_path, apk_local_path, json_file=None):
        # Owner：11602272
        # CreateTime：2015年7月5日
        # ModifyTime：
        # 函数参数：服务器文件目录，本地保存目录，json文件
        # 函数方法：下载入口
        # 函数返回值：空
        self.self_update()
        self.get_config()
        json_file = self.get_file(json_file)
        print "json_file is ", json_file
        self.load_json_file(json_file)
        min, max = self.get_download_rank()
        self.get_apk(apk_server_path, apk_local_path)
#         logger.info("Download over.", "on")
        print "Download over.\n  ~@^_^@~~"
        sys.exit(0)

    def self_update(self):
        # Owner：11602272
        # CreateTime：2015年7月13日
        # ModifyTime：
        # 函数参数：null
        # 函数方法：自动升级APPGet.py文件
        # 函数返回值：空
        version_file = Config.default_server_apk_folder + os.path.sep + "APPGet" + os.path.sep + "Version_Record.txt"
        remote_file = Config.default_server_apk_folder + os.path.sep + "APPGet" + os.path.sep + "APPGet.py"
        print "Checking update..."
        with open (version_file, "r") as file:
            remote_build_time = file.readline()
            print "default_build_time", remote_build_time.strip(), "Config.default_build_time", Config.default_build_time
            if Config.default_build_time == remote_build_time.strip():
                print "APPGet.py is newest!"
                return 1
            else:
                print "Local APPGet.py updating...."
                shutil.copyfile(remote_file, sys.argv[0])
                print "Update finish, Please reload!"
                time.sleep(3)
                sys.exit(1)

if __name__ == "__main__":
    print "Running APPGet.py download by rank."
    def run():
        Downloader = DownloadByRank()
        try:
            res = Downloader.downloader(Config.default_server_apk_folder, Config.default_apk_local_path, sys.argv[1])
        except:
            res = Downloader.downloader(Config.default_server_apk_folder, Config.default_apk_local_path)
    watchDog = WatchDog()
    watchDog.run_with_reloader(run())
