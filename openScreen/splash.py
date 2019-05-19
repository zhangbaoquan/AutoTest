

"""

需求：开屏的展示、点击
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
import os
import time
import sys

if __name__ == '__main__':

    # 包名，这里以VIVO电子书为列
    packageName = "com.chaozh.iReader"
    # 定向打开的路径,这里以欢迎页为例
    pagePath = "/com.chaozh.iReader.ui.activity.WelcomeActivity"
    # 循环的次数
    loopCount = 10
    # 启动一个Activity的adb shell 语句
    openAppCommand = " adb shell am start " + packageName + pagePath
    # 杀死应用的 adb shell 语句
    closeAppCommand = " adb shell am force-stop " + packageName
    # 点击屏幕的坐标点（500，500）
    clickAppCommand = "adb shell input tap 500 500"
    # 按下Back返回
    backAppCommand = "adb shell input keyevent KEYCODE_BACK "

    # os.system(openAppCommand)
    # # 获取手机屏幕的大小
    # size_str = os.popen("adb shell wm size").read()
    # print("大小："+size_str)

    print("device id : "+sys.argv[1])

    for i in range(1,loopCount):
        os.system(openAppCommand)
        # 这里设置 3s 延时是考虑等广告展示出来后在点击
        time.sleep(3)
        os.system(clickAppCommand)
        # 这是设置 3s 延时是考虑等广告落地页展示出来后再按back键返回到书城
        time.sleep(3)
        os.system(backAppCommand)
        # 这里设置 2s 延时是避免按完返回键后直接杀进程造成跳闪现象
        time.sleep(2)
        os.system(closeAppCommand)
        # 这里设置 2s 延时主要是避免杀完进程后立即开启的跳闪（模拟正常操作）
        time.sleep(2)