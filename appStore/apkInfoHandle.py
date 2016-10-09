# -*- coding: utf-8 -*-
from systemUtils.util import *

class ApkInfoHandle:
    rank_list = []
    apk_md5_list = []
    apk_name_list = []
    apk_package_list = []
    apk_version_list = []
    apk_file_path_list = []
    apk_icon_path_list = []

    def get_local_apk_version(self, remote_apk_info):
        # Owner：11602272
        # CreateTime：2015年5月9日
        # ModifyTime：
        # 函数参数：1.web上apk信息,2.本地apk保存的目录
        # 函数方法：得到本地文件夹下APP的版本
        # 函数返回值：1.需要下载的apk,2.需要复制的apk
        need_download_apk_dictionary = {}
        need_copy_apk_list = []
        if os.path.exists(Store.default_apk_save_path):
            for i in remote_apk_info:
                expectation_apk_name = i[0] + '_' + i[1] + i[3]
                if os.path.exists(Store.default_apk_save_path + os.path.sep + expectation_apk_name):
                    need_copy_apk_list.append(expectation_apk_name)
                else:
                    try:
                        need_download_apk_dictionary[expectation_apk_name] = [i[2], i[4], i[5]]
                    except:
                        need_download_apk_dictionary[expectation_apk_name] = i[2]
        else:
            FloderHandel().create_apk_folder(Store.default_apk_save_path)
            for i in remote_apk_info:
                try:
                    need_download_apk_dictionary[i[0] + '_' + i[1] + i[3]] = [i[2], i[4], i[5]]
                except:
                    need_download_apk_dictionary[i[0] + '_' + i[1] + i[3]] = i[2]
        logger.debug("need_download_apk_dictionary is %s length is %s" % (need_download_apk_dictionary, len(need_download_apk_dictionary)), "on")
        logger.debug("need_copy_apk_list is %s length is %s" % (need_copy_apk_list, len(need_copy_apk_list)), "on")
        return need_download_apk_dictionary , need_copy_apk_list

    def get_md5(self, file):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：
        # 函数参数：1.文件名，
        # 函数方法：生成文件MD5值
        # 函数返回值：返回传入文件的MD5
        with open (file, 'rb') as f:
            m = md5.new(f.read())
            file_md5 = m.hexdigest()
        return file_md5

    def get_apk_md5(self, remote_apk_info):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：
        # 函数参数：1.文件名，2.apk目录
        # 函数方法：生成文件夹下所有apk文件MD5值
        # 函数返回值：返回传入目录下apk文件的MD5列表
        md5_list = []
        if os.path.exists(Store.default_apk_save_path):
            for i in remote_apk_info:
                apk_name = i[0] + '_' + i[1] + i[3]
                if os.path.isfile(Store.default_apk_save_path + os.path.sep + apk_name):
                    apk_md5 = self.get_md5(Store.default_apk_save_path + os.path.sep + apk_name)
                    md5_list.append(apk_md5)
                else:
                    logger.error("Can't get_apk_md5, Lost Apk file %s" % (Store.default_apk_save_path + os.path.sep + apk_name), "on")
                    md5_list.append("null")
        return md5_list

    def get_apk_name(self, remote_apk_info, apk_aapt_content):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：2015年5月12日
        # 函数参数：1.文件名，2.apk目录
        # 函数方法：生成文件夹下所有apk文件名
        # 函数返回值：返回传入目录下apk文件的文件名
        name_list = []
        if os.path.exists(Store.default_apk_save_path):
            for i in remote_apk_info:
                find_tag = "False"
                apk_name = i[0] + '_' + i[1] + i[3]
                if os.path.isfile(Store.default_apk_save_path + os.path.sep + apk_name):
                    aapt_info = apk_aapt_content.get(apk_name)
                    for line in aapt_info:
                        if line.find("application-label:") != -1:
#                             logger.debug("apk_name line is %s" % line, "on")
                            apk_name = line.split(":")[1].strip()[1:-1].decode("UTF-8", 'ignore').encode("UTF-8")
#                             logger.debug("apk_name = %s" % apk_name, "on")
                            name_list.append(apk_name)
                            find_tag = "True"
                        else:
                            pass
                else:
                    logger.error("Can't get_apk_name, Lost Apk file %s" % (Store.default_apk_save_path + os.path.sep + apk_name), "on")
                if find_tag == "False":
                    logger.warn("Can't find %s name in aapt_info ,use package name" % apk_name, "on")
                    name_list.append(apk_name)
                else:
                    pass
        else:
            logger.error("Def get_apk_name Can't find apk_save_path %s" % (apk_save_path), "on")
        return name_list

    def get_apk_package(self, remote_apk_info, apk_aapt_content):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：2015年5月12日
        # 函数参数：1.文件名，2.apk目录
        # 函数方法：生成文件夹下所有apk文件package
        # 函数返回值：返回传入目录下apk文件的package
        package_list = []
        if os.path.exists(Store.default_apk_save_path):
            for i in remote_apk_info:
                find_tag = "False"
                apk_name = i[0] + '_' + i[1] + i[3]
                if os.path.isfile(Store.default_apk_save_path + os.path.sep + apk_name):
                    aapt_info = apk_aapt_content.get(apk_name)
                    for line in aapt_info:
                        if line.find("package:") == 0:
#                             logger.debug("apk_package line is %s" % line, "on")
                            apk_package = line.split()[1].split("=")[1].strip()[1:-1]
                            package_list.append(i[0])
                            find_tag = "True"
                        else:
                            pass
                else:
                    logger.error("Can't get_apk_package, Lost Apk file %s" % (Store.default_apk_save_path + os.path.sep + apk_name), "on")
                if find_tag == "False":
                    logger.warn("Can't find %s package in aapt_info ,use web package name" % apk_name, "on")
                    package_list.append(i[0])
                else:
                    pass
        else:
            logger.error("Def get_apk_package Can't find Store.default_apk_save_path %s" % (Store.default_apk_save_path), "on")
        return package_list

    def get_apk_version(self, remote_apk_info, apk_aapt_content):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：2015年5月12日
        # 函数参数：1.文件名，2.apk目录
        # 函数方法：生成文件夹下所有apk文件version
        # 函数返回值：返回传入目录下apk文件的version
        version_list = []
        if os.path.exists(Store.default_apk_save_path):
            for i in remote_apk_info:
                find_tag = "False"
                apk_name = i[0] + '_' + i[1] + i[3]
                if os.path.isfile(Store.default_apk_save_path + os.path.sep + apk_name):
                    aapt_info = apk_aapt_content.get(apk_name)
                    for line in aapt_info:
                        if line.find("package:") == 0:
#                             logger.debug("apk_version line is %s" % line, "on")
                            apk_version = line.split()[3].split("=")[1].strip()[1:-1]
                            version_list.append(apk_version)
                            find_tag = "True"
                        else:
                            pass
                else:
                    logger.error("Can't get_apk_package, Lost Apk file %s" % (Store.default_apk_save_path + os.path.sep + apk_name), "on")
                if find_tag == "False":
                    logger.warn("Can't find %s version in aapt_info ,use web version " % apk_name, "on")
                    version_list.append(i[1])
                else:
                    pass
        else:
            logger.error("Def get_apk_version Can't find apk_save_path %s" % (Store.default_apk_save_path), "on")
        return version_list

    def get_apk_file_path(self, remote_apk_info, need_download_apk_dictionary):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：
        # 函数参数：1.文件名，2.apk目录
        # 函数方法：生成文件夹下所有apk文件version
        # 函数返回值：复制apk到上传缓存目录
        apk_file_path_list = []
        upload_apk_name_list = need_download_apk_dictionary.keys()
        if os.path.exists(Store.default_apk_save_path):
            for i in remote_apk_info:
                apk_name = i[0] + '_' + i[1] + i[3]
                if os.path.isfile(Store.default_apk_save_path + os.path.sep + apk_name):
                    apk_md5 = self.get_md5(Store.default_apk_save_path + os.path.sep + apk_name)
                    upload_path = apk_md5[0:2] + os.path.sep + apk_md5[2:4]
                    local_upload_path = "upload" + os.path.sep + "apk" + os.path.sep + apk_md5[0:2] + os.path.sep + apk_md5[2:4]
                    for upload_apk_name in upload_apk_name_list:
                        if apk_name == upload_apk_name:
                            FloderHandel().create_apk_folder(Store.default_apk_save_path + os.path.sep + local_upload_path)
                            shutil.copyfile(Store.default_apk_save_path + os.path.sep + apk_name, Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + apk_md5 + ".apk")
                            os.chdir(os.path.split(sys.argv[0])[0])
                        else:
                            pass
                    if Store.default_copy_file_method != "different":
                        logger.debug("Copy %s to %s" % ((Store.default_apk_save_path + os.path.sep + apk_name), (Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + apk_md5 + ".apk")), "on")
                        FloderHandel().create_apk_folder(Store.default_apk_save_path + os.path.sep + local_upload_path)
                        shutil.copyfile(Store.default_apk_save_path + os.path.sep + apk_name, Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + apk_md5 + ".apk")
                        if os.path.isfile(Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + apk_md5 + ".apk"):
                            pass
                        else:
                            logger.warn("Apk file isn't found %s" % (Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + apk_md5 + ".apk"), "on")
                        os.chdir(os.path.split(sys.argv[0])[0])
                    else:
                        pass
                    apk_file_path_list.append(upload_path + os.path.sep + apk_md5 + ".apk")
                else:
                    logger.warn("apk_file %s is not exist" % (Store.default_apk_save_path + os.path.sep + apk_name), "on")
                    apk_file_path_list.append("null")
        else:
            logger.error("Def get_apk_file_path Can't find Store.default_apk_save_path %s" % (Store.default_apk_save_path), "on")
        return apk_file_path_list

    def get_apk_icon_path(self, remote_apk_info, need_download_apk_dictionary, apk_aapt_content):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：2015年5月13日
        # 函数参数：1.文件名，2.aapt保存路径，3.apk目录
        # 函数方法：生成文件夹下所有apk文件icon
        # 函数返回值：返回传入目录下apk文件的icon
        apk_icon_path_list = []
        upload_apk_name_list = need_download_apk_dictionary.keys()
        if os.path.exists(Store.default_apk_save_path):
            for i in remote_apk_info:
                find_tag = "False"
                apk_name = i[0] + '_' + i[1] + i[3]
                if os.path.isfile(Store.default_apk_save_path + os.path.sep + apk_name):
                    aapt_info = apk_aapt_content.get(apk_name)
#                     logger.debug("apk_name is %s " % apk_name, "on")
                    for line in aapt_info:
                        if line.find("application:") != -1:
                            find_tag = "True"
                            # 获得aapt信息里icon保存的相对路径
#                             logger.debug("line is %s" % line , "on")
                            apk_icon_location = line.split("icon=")[1].strip()[1:-1]
                            # 截取icon文件原始文件名
                            icon_orgin_file = Store.default_apk_save_path + os.path.sep + apk_icon_location.split('/')[len(apk_icon_location.split('/')) - 1]
                            # 解压apk文件拉取icon文件
                            zfile = zipfile.ZipFile(Store.default_apk_save_path + os.path.sep + apk_name, 'r')
                            try:
                                with open (icon_orgin_file , 'wb') as icon:
                                    data = zfile.read(apk_icon_location)
                                    icon.write(data)
                            except:
                                logger.error("Can't read %s apk_icon_location %s" % (apk_name,apk_icon_location), "on")
                            # 获得icon文件的MD5
                            if os.path.isfile(icon_orgin_file):
                                icon_md5 = self.get_md5(icon_orgin_file)
#                                 logger.debug("icon_md5 is: %s" % icon_md5, "on")
                            else:
                                logger.warn("%s icon_orgin_file %s is not exist" % (apk_name,icon_orgin_file), "on")
                            # 拼凑上传缓存区目录结构
                            upload_path = icon_md5[0:2] + os.path.sep + icon_md5[2:4]
                            local_upload_path = "upload" + os.path.sep + "icon" + os.path.sep + icon_md5[0:2] + os.path.sep + icon_md5[2:4]
                            # 判断文件图标是否需要上传更新
                            for upload_apk_name in upload_apk_name_list:
                                if apk_name == upload_apk_name:
                                    FloderHandel().create_apk_folder(Store.default_apk_save_path + os.path.sep + local_upload_path)
                                    # 复制icon文件到上传缓存区，并改名，以MD5值命名
                                    shutil.copyfile(icon_orgin_file, Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + icon_md5 + ".png")
                                    # 由于shutil.copyfile会切换工作目录到destination，再切换回来
                                    os.chdir(os.path.split(sys.argv[0])[0])
                                else:
                                    pass
                            if Store.default_copy_file_method != "different":
                                logger.debug("Copy %s to upload buffer %s" % (icon_orgin_file, Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + icon_md5 + ".png"))
                                FloderHandel().create_apk_folder(Store.default_apk_save_path + os.path.sep + local_upload_path)
                                # 复制icon文件到上传缓存区，并改名，以MD5值命名
                                try:
                                    shutil.copyfile(icon_orgin_file, Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + icon_md5 + ".png")
                                except Exception as e:
                                    logger.warn("Icon_orgin_file %s not correct" % icon_orgin_file, "on")
                                if os.path.isfile(Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + icon_md5 + ".png"):
                                    pass
                                else:
                                    logger.warn("Icon file isn't found %s" % (Store.default_apk_save_path + os.path.sep + local_upload_path + os.path.sep + icon_md5 + ".png"), "on")
                                # 由于shutil.copyfile会切换工作目录到destination，再切换回来
                                os.chdir(os.path.split(sys.argv[0])[0])
                            else:
                                pass
                            # 将缓存区icon的path保存到列表
                            apk_icon_path_list.append(upload_path + os.path.sep + icon_md5 + ".png")
                            # 删除原始icon文件
                            if os.path.isfile(icon_orgin_file):
                                os.remove(icon_orgin_file)
                            else:
                                pass
                        else:
                            pass
                    if find_tag == "False":
                        logger.warn("Can't find %s icon in aapt_info ,use null icon " % apk_name, "on")
                        apk_icon_path_list.append("null")
                    else:
                        pass
                else:
                    logger.warn("apk_file %s is not exist" % (Store.default_apk_save_path + os.path.sep + apk_name), "on")
                    apk_icon_path_list.append("null")
        else:
            logger.error("Def get_apk_icon_path Can't find Store.default_apk_save_path %s" % (Store.default_apk_save_path), "on")
        return apk_icon_path_list


    def get_apk_upload_info(self, remote_apk_info, need_download_apk_dictionary, apk_aapt_content):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：
        # 函数参数：1.文件名，2.下载地址，3.proxy
        # 函数方法：单个文件下载保存
        # 函数返回值：null
        upload_info = {}
        data = []
        upload_info["version"] = "headed-1.0"
        upload_info["heads"] = ["md5", "name", "package", "version", "uri", "icon_uri"]
        self.apk_md5_list = self.get_apk_md5(remote_apk_info)
        logger.debug("apk_md5_list = %s length = %s" % (self.apk_md5_list, len(self.apk_md5_list)), "on")
        self.apk_name_list = self.get_apk_name(remote_apk_info, apk_aapt_content)
        logger.debug("apk_name_list = %s length = %s" % (self.apk_name_list, len(self.apk_name_list)), "on")
        self.apk_package_list = self.get_apk_package(remote_apk_info, apk_aapt_content)
        logger.debug("apk_package_list = %s length = %s" % (self.apk_package_list, len(self.apk_package_list)), "on")
        self.apk_version_list = self.get_apk_version(remote_apk_info, apk_aapt_content)
        logger.debug("apk_version_list = %s length = %s" % (self.apk_version_list, len(self.apk_version_list)), "on")
        self.apk_file_path_list = self.get_apk_file_path(remote_apk_info, need_download_apk_dictionary)
        logger.debug("apk_file_path_list = %s length = %s" % (self.apk_file_path_list, len(self.apk_file_path_list)), "on")
        self.apk_icon_path_list = self.get_apk_icon_path(remote_apk_info, need_download_apk_dictionary, apk_aapt_content)
        logger.debug("apk_icon_path_list = %s length = %s" % (self.apk_icon_path_list, len(self.apk_icon_path_list)), "on")
        apk_info_list = []
        for i in range(len(self.apk_md5_list)):
#             logger.debug("[apk_md5_list[i]=%s, apk_name_list[i]=%s, apk_package_list[i]=%s, apk_version_list[i]=%s, apk_file_path_list[i]=%s, apk_icon_path_list[i]]=%s" % (apk_md5_list[i], apk_name_list[i], apk_package_list[i], apk_version_list[i], apk_file_path_list[i], apk_icon_path_list[i]))
            apk_info_list.append([self.apk_md5_list[i], self.apk_name_list[i], self.apk_package_list[i], self.apk_version_list[i], self.apk_file_path_list[i], self.apk_icon_path_list[i]])
        upload_info["apps"] = apk_info_list
#         data = json.dumps(upload_info, ensure_ascii=False)
        data.append(json.dumps(upload_info))
        return data

    def get_apk_rank_upload_info(self, remote_apk_info, apk_aapt_content):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：
        # 函数参数：1.文件名，2.下载地址，3.proxy
        # 函数方法：单个文件下载保存
        # 函数返回值：null
        upload_info = {}
        data = []
        item = int(Store.default_download_end) - int(Store.default_download_begin) + 1
        seprate = 1
        upload_datetime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        for category in Store.default_apk_category:
            upload_info["version"] = "headed-1.0"
            upload_info["store"] = Store.default_store_store
            upload_info["category"] = category
            upload_info["datetime"] = upload_datetime
            apk_md5_category_list = self.apk_md5_list[(seprate - 1) * item : seprate * item]
            upload_info["apps"] = apk_md5_category_list
            data.append(json.dumps(upload_info))
            self.get_apk_jason_upload_file(remote_apk_info, upload_info, (seprate - 1) * item, seprate * item)
            seprate += 1
        ranking_save_path = Store.default_apk_save_path + os.path.sep + "upload" + os.path.sep + "ranking" + os.path.sep + upload_info["store"]
        with open (ranking_save_path + os.path.sep + "All_latest_" + Store.default_arch + ".json", 'w') as json_file:
            logger.debug("self.rank_list is %s" % self.rank_list, "on")
            json.dump({"rank":self.rank_list}, json_file)
        logger.debug("Store.apk_debug_dict is %s" % Store.apk_debug_dict, "on")
        return data

    def get_apk_jason_upload_file(self, remote_apk_info, upload_info, start , end):
        # Owner：11602272
        # CreateTime：2015年5月11日
        # ModifyTime：
        # 函数参数：1.文件名，2.下载地址，3.proxy
        # 函数方法：单个文件下载保存
        # 函数返回值：null
        apps = []
        detail = {}
        detail["category"] = "%s" % upload_info["category"]
        detail["store"] = "%s" % upload_info["store"]
        detail["datetime"] = "%s" % upload_info["datetime"]
        detail["arch"] = "%s" % Store.default_arch
        for i in range(start, end):
            app = {}
            app["package"] = "%s" % self.apk_package_list[i]
            app["name"] = "%s" % self.apk_name_list[i]
            app["md5"] = "%s" % self.apk_md5_list[i]
            app["version"] = "%s" % self.apk_version_list[i]
            app["apk_path"] = "%s" % self.apk_file_path_list[i]
            app["icon_path"] = "%s" % self.apk_icon_path_list[i]
            if Store.apk_debug_dict[remote_apk_info[i][0] + "_" + remote_apk_info[i][1] + remote_apk_info[i][3]] == []:
                app["debug_info"] = None
            else:
                Store.apk_debug_dict[remote_apk_info[i][0] + "_" + remote_apk_info[i][1] + remote_apk_info[i][3]] = list(set(Store.apk_debug_dict[remote_apk_info[i][0] + "_" + remote_apk_info[i][1] + remote_apk_info[i][3]]))
                print "Store.apk_debug_dict", Store.apk_debug_dict[remote_apk_info[i][0] + "_" + remote_apk_info[i][1] + remote_apk_info[i][3]]
                app["debug_info"] = "%s" % Store.apk_debug_dict[remote_apk_info[i][0] + "_" + remote_apk_info[i][1] + remote_apk_info[i][3]]
            apps.append(app)
        detail["apps"] = apps
        logger.debug("detail is %s" % detail, "on")
        ranking_save_path = Store.default_apk_save_path + os.path.sep + "upload" + os.path.sep + "ranking" + os.path.sep + detail["store"] + os.path.sep + detail["category"]
        if os.path.exists(ranking_save_path) == False:
            FloderHandel().create_apk_folder(ranking_save_path)
        with open (ranking_save_path + os.path.sep + detail["store"] + "_" + detail["category"] + "_" + detail["datetime"] + ".json", 'w') as json_file:
            json.dump(detail, json_file)
        self.rank_list.append(detail)

