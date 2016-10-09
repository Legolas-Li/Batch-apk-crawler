# -*- coding: utf-8 -*-
from systemUtils.util import *

class GooglePlay(Store):
    GENERAL_FILE_EXTENSION = ".apk"
    authSubToken_list = []
    package_name_list = []
    package_cookies = {}
    package_name_map = {}
    package_name_map_retry = {}

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
        url = {"application": "collection/topselling_free?", "game": "category/GAME/collection/topselling_free?",
               }
        for category in Store.default_apk_category:
            category_selection.append(url.get(category))
        return category_selection

    def get_google_token(self):
        # Owner：11602272
        # CreateTime：2015年6月20日
        # ModifyTime：2015年6月25日
        # 函数参数：登陆Google的链接，账户，密码，Proxy
        # 函数方法：登陆Google
        # 函数返回值：auth_token
        account_list = Store.default_account.split(";")
        password_list = Store.default_password.split(";")
        for m in range(0, len(account_list)):
            params = {
              "Email"       : account_list[m],
              "Passwd"      : password_list[m],
              "service"     : "androidsecure",
              "accountType" : "HOSTED_OR_GOOGLE"
              }
            headers = {"Content-type": "application/x-www-form-urlencoded"}
            r = requests.post(Store.default_login_url, data=params, headers=headers, proxies=Store.default_proxy)
            result = r.content.split('\n')
            if result[0] == 'Error=BadAuthentication':
                logger.error("Login failed, please check account or password and restart the script.", "on")
            auth = [i for i in result if i.find('Auth=') != -1]
            if auth:
                account_token = auth[0].split('=')[1]
                if account_token != None:
                    self.authSubToken_list.append(account_token)
                    logger.info("Account %s authSubToken is %s" % (account_list[m], account_token), "on")
                else:
                    logger.error("Get account %s token failed!" % account_list[m], "on")
#                     raise Exception("Get token failed!")
        return self.authSubToken_list

    def google_encode(self, buffer, number):
        while number:
            if number < 128:
                mod = number
                number = 0
            else:
                mod = number % 128
                mod += 128
                number = number / 128
            buffer.append(mod)

    def update_data(self, buffer, data, raw=False):
        if raw is False:
            data_type = type(data).__name__
            if data_type == "bool":
                buffer.append(1 if data is True else 0)
            elif data_type == "int":
                self.google_encode(buffer, data)
            elif data_type == "str":
                self.google_encode(buffer, len(data))
                for c in data:
                    buffer.append(ord(c))
            else:
                raise Exception("Unhandled data type : " + data_type)
        else:
            buffer.append(data)

    def generate_request(self, para):
        tmp = []
        pad = [10]
        result = []
        header_len = 0
        url_config = [[16], [24], [34], [42], [50], [58], [66], [74], [82], [90], [19, 82], [10], [20]]
        for i in range(0, 13):
            if i == 4:
                self.update_data(tmp, '%s:%d' % (para[4], para[2]))
            elif i == 10:
                self.update_data(tmp, para[i])
                header_len = len(tmp) + 1
            elif i == 11:
                self.update_data(tmp, len(para[i]) + 2)
            else:
                self.update_data(tmp, para[i])
            tmp += url_config[i]
        self.update_data(result, header_len)
        result = pad + result + pad + tmp
        stream = ""
        for data in result:
            stream += chr(data)
        return  base64.b64encode(stream, "-_")

    @retry(3)
    def get_update(self, package_name):
        # Owner：11602272
        # CreateTime：2015年7月1日
        # ModifyTime：
        # 函数参数：package_name, apk_save_path, proxy
        # 函数方法：取到apk最近更新时间，用来代替无法从web得到的version信息
        # 函数返回值：update时间信息和是否download的标识
        update = time.strftime("%b-%d-%Y", time.localtime())
        download_flag = True
        req = self.get_url_content("https://play.google.com/store/apps/details?id=%s" % package_name)
        content = req.content.decode("utf-8")
        tree = lxml.html.fromstring(content)
        all_match = tree.xpath("//div[@itemprop=\"datePublished\"]")
        update = str(all_match[0].text_content()).replace(" ", "-").replace(",", "")
        expectation_apk_name = package_name + '_' + update + ".apk"
        if os.path.exists(Store.default_apk_save_path + os.path.sep + expectation_apk_name):
            logger.debug("App %s already exist." % (Store.default_apk_save_path + os.path.sep + expectation_apk_name), "on")
            download_flag = False
        return update, download_flag

    @retry(10)
    def get_apk_url(self, package_name, authSubToken_list):
        # Owner：11602272
        # CreateTime：2015年6月24日
        # ModifyTime：2015年6月25日
        # 函数参数： 需要下载的apk包名,手机的android_id,Proxy
        # 函数方法：null
        # 函数返回值：req
        if authSubToken_list:
            authSubToken = authSubToken_list[0]
            authSubToken_list.remove(authSubToken_list[0])
        else:
            logger.error("authSubToken_list is None %s download fail." % package_name, "on")
            self.package_name_list.remove(package_name)
            self.package_name_map_retry[package_name] = 7
            sys.exit(1)
        if not self.package_cookies.has_key(package_name):
            update, download_flag = self.get_update(package_name)
            url = ""
            cookies = {}
            headers = {}
            if download_flag:
                input_para = [authSubToken, True, int(Store.default_sdk_level) , Store.default_android_id, "", "en", "us", "AT&T", "AT&T", "31038", "31038", package_name, package_name]
                request = self.generate_request(input_para)
                params = {"version" : 2, "request" : request}
                headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept-Language": "en_US",
                    "Authorization": "GoogleLogin auth=%s" % authSubToken,
                    "X-DFE-Enabled-Experiments": "cl:billing.select_add_instrument_by_default",
                    "X-DFE-Unsupported-Experiments": "nocache:billing.use_charging_poller,market_emails,buyer_currency,prod_baseline,checkin.set_asset_paid_app_field,shekel_test,content_ratings    ,buyer_currency_in_app,nocache:encrypted_apk,recent_changes",
                    "X-DFE-Device-Id": Store.default_android_id,
                    "X-DFE-Client-Id": "am-android-google",
                    "User-Agent": "Android-Finsky/3.7.13 (api=3,versionCode=8013013,sdk=16,device=crespo,hardware=herring,product=soju)",
                    "X-DFE-SmallestScreenWidthDp": "320",
                    "X-DFE-Filter-Level": "3",
                    "Accept-Encoding": "",
                    "Host": "android.clients.google.com"}
                r = requests.post('https://android.clients.google.com/market/api/ApiRequest', data=params, headers=headers, verify=False, proxies=Store.default_proxy)
                if r.status_code == 429:
                    logger.error("Get %s Too many request" % package_name, "on")
                elif r.status_code == 403:
                    logger.error("Get %s Forbidden" % package_name, "on")
                elif r.status_code == 401:
                    logger.error("Get %s Unauthorized" % package_name, "on")
                elif r.status_code != 200:
                    logger.error('Unexpected status code %s' % r.status_code, "on")
                gzipped_content = r.content
                response = zlib.decompress(gzipped_content, 16 + zlib.MAX_WBITS)
                match_https = re.search("(https?:\/\/[^:]+)", response)
                if match_https is None:
                    logger.error("Get %s https failed" % package_name, "on")
                else:
                    url = match_https.group(1)
                match_cookie = re.search("MarketDA.*?(\d+)", response)
                if match_cookie is None:
                    logger.error("Get %s cookie failed" % package_name, "on")
                else:
                    cookies = {"MarketDA":match_cookie.group(1)}
                    headers = { "User-Agent" : "AndroidDownloadManager/4.2.1 (Linux; U; Android 4.2.1; Galaxy Nexus Build/JRO03E)", "Accept-Encoding": "" }
            else:
                logger.debug("The apk %s is not update, needn't download." % package_name, "on")
            self.package_cookies[package_name] = [update, url, headers, cookies]
            logger.info("Get %s download url, version, cookes succees!" % package_name, "on")
        else:
            pass

    @timeout(1200)
    def get_apk_list(self):
        # Owner：11602272
        # CreateTime：2015年5月8日
        # ModifyTime：2015年6月2日
        # 函数参数：1.Proxy,2.排名开始，3.排名结束，4.APP分类类型
        # 函数方法：返回指定排名的app列表，列表包括APP名字，版本号，下载链接
        # 函数返回值：all_download_info,['com.tianmashikong.qmqj.bd', '1.4.1', 'http://gdown.baidu.com/data/wisegame/cce33f84449b99f2/quanminqiji_141.apk', '.apk']
#         print proxy, download_begin, download_end, apk_category, account, password, android_id, login_url
        remote_apk_info = []
        logger.debug("Login google play", "on")
        self.account = Store.default_account
        self.password = Store.default_password
        self.get_google_token()
        category_selection = self.get_category_info()
        #         logger.debug("category_selection is %s" % category_selection, "on")
        apk_number_per_page = 100
        if Store.default_download_loacal_list == "True":
            logger.info("Download from local list %s" % Store.default_apk_local, "on")
            with open (Store.default_apk_local ,"r") as app_list_file:
                for package_name in app_list_file.readlines():
                    self.package_name_map [package_name.strip()] = 0
                    self.package_name_list.append(package_name.strip())
        else:
            logger.info("Download from online top list https://play.google.com/store/apps/ ", "on")
            for cid in category_selection:
                page_number = int(Store.default_download_end) / apk_number_per_page + 1
                if int(Store.default_download_end) % apk_number_per_page != 0:
                    page_number = page_number + 1
                count = int(Store.default_download_begin) - 1
                if cid == "collection/topselling_free?" or cid == "category/GAME/collection/topselling_free?":
                    for i in xrange(1, page_number):
                        web_url = "https://play.google.com/store/apps/" + cid + "start=" + str(count) + "&num=100"
    #                 https://play.google.com/store/apps/category/GAME/collection/topselling_free?start=0&num=100
                        req = self.get_url_content(web_url)
                        content = req.content.decode("utf-8")
                        tree = lxml.html.fromstring(content)
                        all_match = tree.xpath("//a[@class=\"title\"]")
                        for i in range(0, len(all_match)):
                            if count < int(Store.default_download_begin) - 1:
                                count = count + 1
                                continue
                            count = count + 1
                            if count > int(Store.default_download_end):
                                break
                            package_name = all_match[i].values()[1].split('=')[1]
                            self.package_name_map [package_name] = 0
                            self.package_name_list.append(package_name)
        logger.debug("self.package_name_list is %s" % self.package_name_list, "on")
        auth_count = 0
        while self.package_name_map:
            if threading.activeCount() <= int(Store.default_max_thread_number) + 2:  #    Get download url 30 threading at the same time
                t = threading.Thread(target=self.get_apk_url, args=(self.package_name_map.items()[0][0], self.authSubToken_list + []))
                t.start()
                del self.package_name_map[self.package_name_map.items()[0][0]]
                auth_count += 1
            else:
                time.sleep(3)
            if auth_count > 400:  #    Remove self.authSubToken_list[0] when over 400 times new threading start.
                self.authSubToken_list.remove(self.authSubToken_list[0])
                auth_count = 0
            else:
                pass
        while threading.activeCount() > 2:
            time.sleep(8)
            logger.info("Please wait, Parseing app is still underway...threading.activeCount() is %s" % threading.activeCount(), "on")
#         logger.debug("package_name_map_retry is : %s" % self.package_name_map_retry, "on")
#         if self.package_name_map_retry:  #    This is backup function use fixed account.
#             self.get_google_token("mys327778674@gmail.com" , "mys1255695864")
#             while self.package_name_map_retry:
#                 if threading.activeCount() <= int(Store.default_max_thread_number) + 2:
#                     t = threading.Thread(target=self.get_apk_url, args=(self.package_name_map_retry.items()[0][0], self.authSubToken_list + []))
#                     t.start()
#                     del self.package_name_map_retry[self.package_name_map_retry.items()[0][0]]
#                 else:
#                     time.sleep(3)
#             while threading.activeCount() > 2 :
#                 time.sleep(8)
#                 logger.info("Please wait, Retry parseing app is still underway...threading.activeCount() is %s" % threading.activeCount(), "on")
#         else:
#             pass
        logger.debug("package_cookies is : %s" % self.package_cookies, "on")
        for i in self.package_name_list:
            remote_apk_info.append([i, self.package_cookies[i][0], self.package_cookies[i][1], self.GENERAL_FILE_EXTENSION, self.package_cookies[i][2], self.package_cookies[i][3]])
            Store.apk_debug_dict[i + "_" + self.package_cookies[i][0] + self.GENERAL_FILE_EXTENSION] = []
        logger.debug("remote_apk_info is %s" % remote_apk_info, "on")
        return remote_apk_info
