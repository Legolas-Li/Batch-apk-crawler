# -*- coding: utf-8 -*-
# import xml.etree.ElementTree as ET
from systemUtils.util import *

class Config:
    """This a class prepare configuration.xml variable"""

class Store:
    """This a class prepare %STORE_NAME%.xml variable"""
    apk_debug_dict = {}

class ParseConfig:

    def __init__(self):
        pass

    def load(self):
        # Owner：11602272
        # CreateTime：2015年5月12日
        # ModifyTime：2015年5月12日
        # 函数参数：null
        # 函数方法：解析config.xml
        # 函数返回值：null
        xml_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir))
        tree = ET.parse(xml_path + os.path.sep + 'configuration.xml')
        root = tree.getroot()
        for child in root:
            setattr(Config, child.tag, child.text)
            logger.debug("%s = %s" % (child.tag, child.text), "on")
        store = []
        for it in root.findall("default_store"):
            store.append(it.text)
        setattr(Config, "default_store", store)
        logger.debug("default_store = %s" % store, "on")

    def reload(self, store):
        # Owner：11602272
        # CreateTime：2015年5月19日
        # ModifyTime：
        # 函数参数：null
        # 函数方法：解析webStore文件夹下的web配置文件
        # 函数返回值：null
        xml_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.pardir)) + os.path.sep + "webStore"
        tree = ET.parse(xml_path + os.path.sep + store + '.xml')
        root = tree.getroot()
        for child in root:
            setattr(Store, child.tag, child.text)
            logger.debug("%s = %s" % (child.tag, child.text), "on")
        apk_category = []
        proxy = None
        for it in root.findall("default_apk_category"):
            apk_category.append(it.text)
        setattr(Store, "default_apk_category", apk_category)
        logger.debug("default_apk_category = %s" % apk_category, "on")
        if Store.default_proxy_type == "http" or Store.default_proxy_type == "socks":
            proxy = {Store.default_proxy_type : Store.default_proxy}
        else:
            pass
        setattr(Store, "default_proxy", proxy)
        logger.debug("default_proxy = %s" % proxy, "on")
