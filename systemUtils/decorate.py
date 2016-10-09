# -*- coding: utf-8 -*-
from systemUtils.util import *

class KThread(threading.Thread):
    # Owner：11602272
    # CreateTime：2015年5月15日
    # ModifyTime：
    # 类方法：继承threading.Thread，并添加了kill方法，让我们能杀掉它
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the
        trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

class Timeout(Exception):
    """Function run timeout"""

def timeout(seconds):
    # Owner：11602272
    # CreateTime：2015年5月15日
    # ModifyTime：
    # 函数参数： 时间
    # 函数方法：若被装饰的方法在指定的时间内未返回，则抛出Timeout异常
    # 函数返回值：function
    def timeout_decorator(func):
        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))
        @functools.wraps(func)
        def _handel_arg(*args, **kwargs):
            result = []
            new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }
            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.isAlive()
            thd.kill()  # kill the child thread
            if alive:
                logger.error(u'%s with args(%s) run too long, timeout %d seconds.' % (func, args, seconds), "on")
                raise Timeout(u'%s with args(%s) run too long, timeout %d seconds.' % (func, args, seconds))
            else:
                return result[0]
        return _handel_arg
    return timeout_decorator

def retry(attempt):
    # Owner：11602272
    # CreateTime：2015年6月30日
    # ModifyTime：
    # 函数参数： 重试次数
    # 函数方法：如果函数异常失败则会重新尝试attempt次
    # 函数返回值：function
    def func_handler(func):
        @functools.wraps(func)
        def args_handler(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    att += 1
                    logger.debug("%s %s, Retry %s times." % (func, e, att), "on")
        return args_handler
    return func_handler


