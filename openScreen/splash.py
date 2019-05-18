

"""

需求： 应用打开，过5s后关闭，操作10次
市场版及厂商的包名
1、iReader： com.chaozh.iReaderFree
2、OPPO：    com.oppo.reader
3、VIVO：    com.chaozh.iReader
4、HUAWEI：  com.huawei.hwirehuawiader
5、Gionee：  com.chaozh.iReaderGionee
6、Aliyun：  com.chaozh.ireader.aliyun
7、sansung:  com.mci.smagazine
8、Nubia:    com.chaozh.iReaderNubia


"""
if __name__ == '__main__':

    # 包名，这里以VIVO电子书为列
    package = "com.chaozh.iReader"
    # 定向打开的路径,这里以欢迎页为例
    pagePath = "/com.chaozh.iReader.ui.activity.WelcomeActivity"
    # 循环的次数
    loopCount = 10
    # 启动一个Activity的adb shell 语句
    openAppCommand = " adb shell am start -n " + package + pagePath
    # 杀死应用的 adb shell 语句
    closeAppCommand = " adb shell am force-stop " + package
