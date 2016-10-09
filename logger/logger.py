# -*- coding: utf-8 -*-

from systemUtils.util import *

class Logger:
    """defult Logger"""

logger = logging.getLogger("[LOGGER]")
file_handle = logging.FileHandler("apkCrawler_" + time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + ".log")
consol_handle = logging.StreamHandler()
formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s: %(message)s')

def debug(msg, echo="on"):
    logger.setLevel(logging.DEBUG)
    file_handle.setLevel(logging.DEBUG)
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    if echo == "on":
        consol_handle.setFormatter(formatter)
        logger.addHandler(consol_handle)
    else:
        pass
    logger.debug(msg)

def info(msg, echo="on"):
    logger.setLevel(logging.INFO)
    file_handle.setLevel(logging.INFO)
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    if echo == "on":
        consol_handle.setFormatter(formatter)
        logger.addHandler(consol_handle)
    else:
        pass
    logger.info(msg)

def warn(msg, echo="on"):
    logger.setLevel(logging.WARN)
    file_handle.setLevel(logging.WARN)
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    if echo == "on":
        consol_handle.setFormatter(formatter)
        logger.addHandler(consol_handle)
    else:
        pass
    logger.warn(msg)

def error(msg, echo="on"):
    logger.setLevel(logging.ERROR)
    file_handle.setLevel(logging.ERROR)
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    if echo == "on":
        consol_handle.setFormatter(formatter)
        logger.addHandler(consol_handle)
    else:
        pass
    logger.error(msg)

def critical(msg, echo="on"):
    logger.setLevel(logging.CRITICAL)
    file_handle.setLevel(logging.CRITICAL)
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    if echo == "on":
        consol_handle.setFormatter(formatter)
        logger.addHandler(consol_handle)
    else:
        pass
    logger.critical(msg)