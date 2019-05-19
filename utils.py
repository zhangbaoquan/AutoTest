# coding=utf-8
"""
@project : AutoTest
@author  : zhangbaoquan
#@file   : utils.py
#@ide    : PyCharm Community Edition
#@time   : 2019-05-19 15:30:27
@desc    : 工具类

"""

import os

""" 
ADB 工具类
"""


class ADBUtils:
    # packageName : 包名
    # pagePath    : Activity路径
    def __init__(self, packageName, pagePath):
        self.packageName = packageName
        self.pagePath = pagePath

    # 开启应用
    def startApp(self):
        openAppCommand = " adb shell am start " + self.packageName + self.pagePath
        os.system(openAppCommand)

    # 杀死应用
    def killApp(self):
        closeAppCommand = " adb shell am force-stop " + self.packageName
        os.system(closeAppCommand)

    # 计算手机的分辨率
    @staticmethod
    def calculateScreenSize():
        return os.popen("adb shell wm size").read()

    # 点击事件
    # x : 屏幕的横坐标
    # y : 屏幕的纵坐标
    @staticmethod
    def clickApp(x, y):
        clickAppCommand = "adb shell input tap " + x + y
        os.system(clickAppCommand)

    # 按下Back返回
    @staticmethod
    def clickBack():
        backAppCommand = "adb shell input keyevent KEYCODE_BACK "
        os.system(backAppCommand)

    # 开启制定的界面
    def openPage(self, pagePath):
        openAppCommand = " adb shell am start " + self.packageName + pagePath
        os.system(openAppCommand)
