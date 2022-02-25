'''
Author: xzhouinfo
Date: 2022-01-16 16:35:01
LastEditors: Please set LastEditors
LastEditTime: 2022-02-19 09:53:16
Description: 各种demo
'''

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from helium import *
from time import sleep
import json
import random
import pandas as pd
import re
import os
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from configparser import ConfigParser

LIVE_CONFIG = ['5000', ['?5000-1万', '?1万-5万', '?5万-10万', '?10万-50万', '?100万-500万'], '80', '']
config_name = 'doudian_config.ini'


class DouDian:
    def __init__(self):
        self.url = 'https://fxg.jinritemai.com/ffa/mshop/homepage/index'
        self.option = ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.option.add_argument('--start-maximized')
        # self.option.opt_binary_location=r"D:\RunningCheeseChrome_V96.0_XiTongZhiJia\RunningCheeseChrome\App\chrome.exe"
        self.option.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=self.option, executable_path='./chromedriver.exe')
        set_driver(self.driver)

    def close_verify(self):
        while Text('请完成下列验证后继续').exists():  # 判断是否需要滑块验证
            print('请完成验证后继续')
            sleep(2)

    def scan_qr(self):
        is_scr = False
        while Text('扫码登录').exists():
            if is_scr == False:
                qr = self.driver.find_element_by_xpath('//div[@class="account-center-qrcode-container"]')
                qr.screenshot('qr.png')
                print('请扫描二维码登录抖店')
                is_scr = True

            if Button('刷新').exists():
                click(Button('刷新'))
                is_scr = False

    def get_wechatid_phonenum(self):
        """
        达人广场页，达人通过信息的联系方式内容
        返回列表

        """
        msg_data_list = []
        name_wechat_phone_msg = []
        while S('.message-center-popup__content').exists():
            all_msg = self.driver.find_elements_by_class_name('message-center-popup__content')
            all_text = [i.text for i in all_msg if ('微信' or '手机') in i.text]
            if all_text:
                name_wechat_phone_msg.append(all_text[0])
            click(S('.message-center-popup__close-icon'))
        for text in name_wechat_phone_msg:
            all_list = text.split('，')
            name = all_list[0].replace('达人同意合作邀约通知\n', '').replace('同意了你的合作邀约', '')
            wechatid = all_list[1].replace('并与你交换了联系方式。', '').replace('。快去达人主页查看。', '').replace('立即查看', '').replace(
                '微信：', '').replace('\n', '')

            if len(all_list) == 3:
                phonenum = all_list[2].replace('。快去达人主页查看。', '').replace('立即查看', '').replace('手机：', '').replace('\n',
                                                                                                                '')
            else:
                phonenum = 0
            msg_data_dict = {'名字': name, '微信号': wechatid, '手机号': phonenum}
            msg_data_list.append(msg_data_dict)

        return msg_data_list

    def close_ad(self):
        """
        关闭悬浮窗广告
        """
        if S('//span[@aria-label="close-circle"]').exists():
            highlight(S('//span[@aria-label="close-circle"]'))
            click(S('//span[@aria-label="close-circle"]'))

    def close_msg(self):
        while S('.message-center-popup__close-icon').exists():
            highlight(S('.message-center-popup__close-icon'))
            click(S('.message-center-popup__close-icon'))

    def close_guide(self):
        """
        关闭引导提示
        """
        button_list = ['知道了', '下一步', '下一个', '完 成', '完成']
        if any([Button(i).exists() for i in button_list]):
            while sum(map(len, [find_all(Button(i)) for i in button_list])):
                for i in button_list:
                    if Button(i).exists():
                        click(Button(i))
                self.close_verify()  # 查看是否需要滑块验证

    def choose_class(self, big_class, small_class):
        """
        选择类目大 小类目如下

        {'玩具乐器': ['玩具', '乐器', '其他'],
        '服饰内衣': ['配饰', '女装', '男装', '内衣'],
        '个护家清': ['纸巾清洁剂', '个人护理'],
        '智能家居': ['床上用品', '厨房用具', '厨房电器', '五金', '日用品', '布艺', '餐具', '家具', '家居饰品', '清洁用具', '收纳整理', '灯具', '汽车'],
        '生鲜': ['肉类', '水果', '蔬菜', '冷冻食品', '海鲜水产'],
        '美妆': ['护肤品', '化妆品'],
        '母婴宠物': ['童鞋', '奶粉辅食', '孕妇产品', '婴童产品', '童装', '宠物用品', '纸尿裤'],
        '食品饮料': ['米面调味', '零食', '传统滋补', '营养保健', '饮料'],
        '3C数码家电': ['手机', '电脑', '数码配件', '影音电器', '智能设备'],
        '图书音像': ['图书', '学习用品'],
        '鞋靴箱包': ['箱包', '男鞋', '女鞋'],
        '运动户外': ['运动健身', '运动服', '户外登山', '运动包', '运动鞋'],
        '钟表配饰': ['眼镜', '饰品', '钟表'],
        '珠宝文玩': ['古董收藏', '珠宝黄金']}


        """
        all_class = self.driver.find_elements_by_xpath('//*/span[@class="false index__valueItem___xcGQU"]')
        ac = [i.text for i in all_class]
        # print(ac)
        if '珠宝文玩' not in ac:
            while S('.message-center-popup__close-icon').exists() and S(
                    '//*/div[@class="index__foldIcon___2JRwk role-item__btn"]').exists() is False:
                click(S('.message-center-popup__close-icon'))
            click(S('//*/div[@class="index__foldIcon___2JRwk role-item__btn"]'))
            wait_until(Text(big_class).exists)
            all_class = self.driver.find_elements_by_xpath('//*/span[@class="false index__valueItem___xcGQU"]')
            ActionChains(self.driver).move_to_element([i for i in all_class if i.text == big_class][0]).perform()
            sleep(1)
            click(small_class)
        else:
            ActionChains(self.driver).move_to_element([i for i in all_class if i.text == big_class][0]).perform()
            sleep(1)
            click(small_class)

    def open_first_page(self):
        # 首页
        go_to(self.url)
        sleep(3)

        self.scan_qr()  # 等待扫描二维码

        wait_until(Text('电商罗盘').exists)  # 等待加载
        sleep(2)
        self.close_ad()  # 如果有广告则关闭广告
        sleep(1)
        self.close_guide()  # 关闭引导提示
        click('营销中心')  # 点击营销中心

        # 营销中心页面
        wait_until(Text('成交金额').exists)  # 等待加载
        self.close_guide()  # 关闭引导提示
        click('达人广场')  # 点击达人广场

        # 达人广场页面
        wait_until(Text('主推类目').exists)  # 等待加载

        self.close_guide()  # 关闭引导
        # self.close_msg() # 关闭消息
        print(self.get_wechatid_phonenum())
        sleep(2)
        self.choose_class('食品饮料', '零食')  # 选择类目

    def main(self):
        self.open_first_page()

    def get_daren_page_data():
        select_values_class = '.index__RadioMultiDropMenuItem___2NJX5'
        select_values = asd.driver.find_elements_by_css_selector(select_values_class)
        click(select_values[1])
        daren_data_dict = {}
        daren_cards = asd.driver.find_elements_by_xpath('//div[@class="daren-card"]')
        daren_cards = [i for i in daren_cards if i.text.split('\n')[-1] != '拒绝合作']
        for daren in daren_cards:
            daren_name = daren.find_element_by_class_name('list-table-info-right-name__nickname').text
            daren_values = daren.find_elements_by_css_selector('.daren-card-keyword__block-value')
            fans_num = daren_values[0].text.replace('\n', '')  # 粉丝数
            average_sales = daren_values[1].text.replace('\n', '')  # 均场销售额
            live_online_num = daren_values[2].text.replace('\n', '')  # 在线人数
            conversion_value = daren_values[3].text.replace('\n', '')  # 转化值
            commission_rate = daren_values[4].text.replace('\n', '')  # 佣金
            category = daren.find_element_by_css_selector('.list-table-info-right__cate').text
            area = daren.find_element_by_css_selector('.list-table-info-right__city').text
            try:
                has_contact_num = daren.find_element_by_css_selector('.list-table-info-right-name__sex')
                has_contact_num = True
            except:
                has_contact_num = False
            print(daren_name, category, area, has_contact_num)
            # daren_data_dict = {'名字':daren_name, '达人类目':daren_all[1], '达人区域':daren_all[2]}


if __name__ == "__main__":
    asd = DouDian()
    asd.main()