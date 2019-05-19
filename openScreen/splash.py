"""
@project : AutoTest
@author  : zhangbaoquan
#@file   : utils.py
#@ide    : PyCharm Community Edition
#@time   : 2019-05-19 15:30:27
@desc    : 需求：开屏的展示、点击


市场版及各厂商的包名
1、iReader： com.chaozh.iReaderFree
2、OPPO：    com.oppo.reader
3、VIVO：    com.chaozh.iReader
4、HUAWEI：  com.huawei.hwirehuawiader
5、Gionee：  com.chaozh.iReaderGionee
6、Aliyun：  com.chaozh.ireader.aliyun
7、sansung:  com.mci.smagazine
8、Nubia:    com.chaozh.iReaderNubia

"""
import time

from AutoTest.utils import ADBUtils

if __name__ == '__main__':

    # 包名，这里以VIVO电子书为列
    packageName = "com.chaozh.iReader"
    # 定向打开的路径,这里以欢迎页为例
    pagePath = "/com.chaozh.iReader.ui.activity.WelcomeActivity"
    # 循环的次数
    loopCount = 10

    # print("device id : "+sys.argv[1])
    adb = ADBUtils(packageName, pagePath)

    for i in range(1, loopCount):
        adb.startApp()
        # 这里设置 3s 延时是考虑等广告展示出来后在点击
        time.sleep(3)
        adb.clickApp(500, 500)
        # 这是设置 3s 延时是考虑等广告落地页展示出来后再按back键返回到书城
        time.sleep(3)
        adb.clickBack()
        # 这里设置 2s 延时是避免按完返回键后直接杀进程造成跳闪现象
        time.sleep(2)
        adb.killApp()
        # 这里设置 2s 延时主要是避免杀完进程后立即开启的跳闪（模拟正常操作）
        time.sleep(2)
