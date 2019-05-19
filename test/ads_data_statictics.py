#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging
import os
import sys
import time
import traceback
import commands
from uiautomator import Device



"""
#需求
统计：签到banner，开屏广告，浮出点击次数；与数据部门数据，秒针数据比对
操作步骤如下：
1）启动程序—点击签到进入福利页面--点击签到banner广告---跳转页面，统计次数
2）启动程序—点击签到进入福利页面—点击浮窗---跳转页面，统计次数
3）启动程序—启动画面—点击：启动画面---跳转页面，统计次数

#执行方式：
cd 到脚本所在目录
python ads_data_statictics.py 设备号
#执行后在当前执行目录下会生成记录文件：设备号_时间戳_log.txt

#测试准备
提前和运营同学沟通，测试期间最好不要配置书城福利页弹框；书城弹框等
程序设置冷启动1S，热启动1S;保证每次全新启动启动画面都能出现
"""

#TODO 根据实际项目修改对应的PACKAGE_NAME
PACKAGE_NAME='com.chaozh.iReader'

class Logger(object):

    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s-%(levelname)-8s: %(message)s', '%Y-%m-%d %H:%M:%S')
        fmt_c = logging.Formatter('%(asctime)s:  %(message)s', '%Y-%m-%d %H:%M:%S')
        # 建立一个streamhandler来把日志打在终端窗口上，级别为error以上
        ch = logging.StreamHandler()
        ch.setFormatter(fmt_c)
        ch.setLevel(clevel)
        # 设置文件日志 建立一个filehandler来把日志记录在文件里，默认级别为debug以上
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        # 将相应的handler添加在logger对象中
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def info(self, message):
        self.logger.info(message)



class Excute(object):
    def __init__(self,device_id):
        self.device_id=device_id
        self.d=Device(self.device_id)
        print(self.d.info)

    def run(self):
        """
        count:控制总的执行次数
        i:控制签到页广告次数
        j:控制开屏广告次数
        k:控制浮窗次数
        """
        time_slapse = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        path=os.path.join(os.getcwd(),device_id + '_' + time_slapse + '_log.txt')
        i = 0
        j = 0
        k = 0
        count = 1
        log = Logger(path)
        while count<=100000:
            # 脚本逻辑
            if (count%3) == 1:
                log.info(50*"#")
                log.info(u"开始:签到页广告页次数测试" )
                try:
                    commands.getoutput(('adb -s %s shell am start '+PACKAGE_NAME)%self.device_id)
                    #启动后等待时间7S，防止启动画面影响不能达到书架界面
                    time.sleep(7)
                    if self.d(description='bookshelf_button').wait.exists(timeout=5000):
                        self.d(description='bookshelf_button').click.wait()
                        time.sleep(1)
                        if self.d(resourceId=PACKAGE_NAME+':id/sign_view').wait.exists(timeout=3000):
                            self.d(resourceId=PACKAGE_NAME+':id/sign_view').click.wait()
                            time.sleep(3)
                            x = self.d.info["displayWidth"]
                            y = self.d.info["displayHeight"]
                            self.d.click(x / 6, y / 6)
                            time.sleep(10)
                            #TODOif d(resourceId='com.android.browser:id/abx').wait.exists(timeout=7000):
                            #TODO 点击广告，跳转后断言浏览器里属性，请根据自己项目实际修改调试
                            if self.d(resourceId='com.android.browser:id/url').wait.exists(timeout=7000):
                                time.sleep(0.5)
                                i += 1
                                log.info(u"签到页广告页次数" + str(i))
                            else:
                                time_slapse = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
                                finename=device_id+'签到页广告页跳转_error'+'_'+str(time_slapse)+'.png'
                                self.screenshot(self.device_id,finename)
                                self.dealTips()
                                commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
                        else:
                            self.dealTips()
                            commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
                    else:
                        self.dealTips()
                        commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
                except:
                    time_slapse = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
                    finename=device_id+'_script_error'+'_'+str(time_slapse)+'.png'
                    self.screenshot(self.device_id,finename)
                    msg = traceback.format_exc()
                    log.info(msg)
            elif (count%3) == 2:
                log.info(u"开始:点击开屏广告次数测试")
                try:
                    commands.getoutput(('adb -s %s shell am start '+PACKAGE_NAME)%self.device_id)
                    #启动后等待时间2S，防止等待时间较长，启动画面消失
                    #等待1s,会出现长时间执行后手机启动变慢，点击时启动画面还没有加载出来
                    #启动画面最好配置5S
                    time.sleep(2)
                    x = self.d.info["displayWidth"]
                    y = self.d.info["displayHeight"]
                    self.d.click(x / 2, y / 2)
                    time.sleep(8)
                    if self.d(description='bookstore_button').exists:
                        commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
                    else:
                        # TODO 点击广告，跳转后断言页面返回按钮属性，请根据自己项目实际修改调试
                        if self.d(className='android.widget.ImageButton')[0].exists:
                            j += 1
                            time.sleep(0.5)
                            log.info(u"点击开屏广告次数" + str(j))
                            self.d(className='android.widget.ImageButton')[0].click.wait() 
                        else:
                            time_slapse = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
                            finename=device_id+'点击开屏广告跳转_error'+'_'+str(time_slapse)+'.png'
                            self.screenshot(self.device_id,finename)
                            self.dealTips()
                            commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
                except:
                    time_slapse = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
                    finename=device_id+'_script_error'+'_'+str(time_slapse)+'.png'
                    self.screenshot(self.device_id,finename)
                    msg = traceback.format_exc()
                    log.info(msg)
                
            else:
                log.info(u"开始:浮窗点击广告次数测试" )
                try:
                    commands.getoutput(('adb -s %s shell am start '+PACKAGE_NAME)%self.device_id)
                    # 启动后等待时间7S，防止启动画面影响不能达到书架界面
                    time.sleep(7)
                    """
                    #书架浮窗--oppo项目没有
                    if self.d(description="bookshelf_button").exists:
                        self.d(description="bookshelf_button").click.wait()
                        time.sleep(1)
                        if self.d(resourceId=PACKAGE_NAME+':id/float_pic').exists:
                            self.d(resourceId=PACKAGE_NAME+':id/float_pic').click.wait()
                            time.sleep(2)
                            #TODO if self.d(resourceId='com.android.browser:id/abx').wait.exists(timeout=7000):
                    """
                    if self.d(description='bookshelf_button').wait.exists(timeout=5000):
                        self.d(description='bookshelf_button').click.wait()
                        time.sleep(1)
                        if self.d(resourceId=PACKAGE_NAME+':id/sign_view').wait.exists(timeout=3000):
                            self.d(resourceId=PACKAGE_NAME+':id/sign_view').click.wait()
                            time.sleep(5)
                            if self.d(resourceId=PACKAGE_NAME+':id/float_pic').wait.exists(timeout=3000):
                                self.d(resourceId=PACKAGE_NAME+':id/float_pic').click.wait()
                                time.sleep(10)
                            # TODO 点击广告，跳转后断言浏览器里属性，请根据自己项目实际修改调试
                            if self.d(resourceId='com.android.browser:id/url').wait.exists(timeout=7000):
                                time.sleep(0.5)
                                k += 1
                                log.info(u"浮窗点击广告次数:" + str(k))
                            else:
                                time_slapse = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
                                finename=device_id+'浮窗点击广告跳转_error'+'_'+str(time_slapse)+'.png'
                                self.screenshot(self.device_id,finename)
                                self.dealTips()
                                commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
                        else:
                            self.dealTips()
                            commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
                    else: 
                        self.dealTips()
                        commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
                except:
                    time_slapse = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
                    finename=device_id+'_script_error'+'_'+str(time_slapse)+'.png'
                    self.screenshot(self.device_id,finename)
                    msg = traceback.format_exc()
                    log.info(msg)       
            #执行一次后，关闭浏览器，关闭测试程序；防止对下次测试有影响
            commands.getoutput(('adb -s %s shell am force-stop com.android.browser')%self.device_id)
            time.sleep(3)
            commands.getoutput(('adb -s %s shell am force-stop '+PACKAGE_NAME)%self.device_id)
            time.sleep(10)
            count += 1


    def screenshot(self,device_id,filename):
        """
        说明：截图（广告点击跳转出错，脚本出错时调用）
        :param device_id: 设备ID
        :param filename: 截图名称
        """
        targetPath=os.getcwd()
        os.system("adb -s %s shell /system/bin/screencap -p /sdcard/%s"%(device_id,filename))
        os.system("adb -s %s pull /sdcard/%s %s"% (device_id,filename,targetPath))
        os.system("adb -s %s shell rm -r /sdcard/%s"%(device_id,filename))
    

    def dealTips(self):
        """
        说明：处理各种弹框；防止对脚本影响
        """
        if self.d(resourceId='com.zhangyue.commonplugin:id/dialog_batch_buy_close').wait.exists(timeout=3000):
            self.d(resourceId='com.zhangyue.commonplugin:id/dialog_batch_buy_close').click.wait()
        if self.d(resourceId=PACKAGE_NAME+':id/cloud_close').wait.exists(timeout=3000):
            self.d(resourceId=PACKAGE_NAME+':id/cloud_close').click.wait()
        if self.d(resourceId=PACKAGE_NAME+':id/close_btn').wait.exists(timeout=3000):
            self.d(resourceId=PACKAGE_NAME+':id/close_btn').click.wait()
        if self.d(resourceId=PACKAGE_NAME+':id/dialog_public_top_bar_title_close').wait.exists():
            self.d(resourceId=PACKAGE_NAME+':id/dialog_public_top_bar_title_close').click.wait()
        if self.d(resourceId=PACKAGE_NAME+':id/iv_close').wait.exists(timeout=3000):
            self.d(resourceId=PACKAGE_NAME+':id/iv_close').click.wait()

if __name__=='__main__':
    device_id = sys.argv[1]
    excute=Excute(device_id)
    excute.run()