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
***************** 工具方法区 *****************
"""


# 判断当前字符串是否为空
def isEmpty(s):
    if str(s).isspace() or len(str(s)) <= 0:
        return 0
    else:
        return 1


# 计算手机的分辨率，返回一个包含宽度和高度的列表
def calculateScreenSize():
    # 获取设备分辨率的原始数据
    result = os.popen("adb shell wm size").read()
    print("设备分辨率：" + result)
    if isEmpty(result) == 0:
        # 这里设置一个默认值，防止分辨率获取失败
        result = "1080x1920"
    value = result.split("x")
    width = str(value[0])
    high = str(value[1])
    print("high：" + high)
    if width.find(':') != -1:
        # 过滤width值之前的所有冗余数据
        width = str(width.split(':')[1]).lstrip()
        print("width：" + width)
    size = [width, high]
    return size


# 设置x坐标值
# width : 表示屏幕的宽度
# scale : 表示缩放的比例
def positionX(width, scale):
    if width > 0:
        return width / scale
    else:
        return 0


# 设置y坐标值
# high : 表示屏幕的高度
# scale : 表示缩放的比例
def positionY(high, scale):
    if high > 0:
        return high / scale
    else:
        return 0


""" 
********************* ADB 工具类 **************************
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

    # 按下Back返回
    @staticmethod
    def clickBack():
        backAppCommand = "adb shell input keyevent KEYCODE_BACK "
        os.system(backAppCommand)

    # 开启制定的界面
    def openPage(self, pagePath):
        openAppCommand = " adb shell am start " + self.packageName + pagePath
        os.system(openAppCommand)

    # 点击事件
    # x : 屏幕的横坐标
    # y : 屏幕的纵坐标
    def clickApp(self, x, y):
        clickAppCommand = "adb shell input tap " + x + " " + y
        print("点击："+clickAppCommand)
        os.system(clickAppCommand)
