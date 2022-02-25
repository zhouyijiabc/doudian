'''
Author: xzhouinfo
Date: 2022-01-16 16:35:01
LastEditors: Please set LastEditors
LastEditTime: 2022-02-19 09:53:16
Description: ����demo
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

LIVE_CONFIG = ['5000', ['?5000-1��', '?1��-5��', '?5��-10��', '?10��-50��', '?100��-500��'], '80', '']
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
        while Text('�����������֤�����').exists():  # �ж��Ƿ���Ҫ������֤
            print('�������֤�����')
            sleep(2)

    def scan_qr(self):
        is_scr = False
        while Text('ɨ���¼').exists():
            if is_scr == False:
                qr = self.driver.find_element_by_xpath('//div[@class="account-center-qrcode-container"]')
                qr.screenshot('qr.png')
                print('��ɨ���ά���¼����')
                is_scr = True

            if Button('ˢ��').exists():
                click(Button('ˢ��'))
                is_scr = False

    def get_wechatid_phonenum(self):
        """
        ���˹㳡ҳ������ͨ����Ϣ����ϵ��ʽ����
        �����б�

        """
        msg_data_list = []
        name_wechat_phone_msg = []
        while S('.message-center-popup__content').exists():
            all_msg = self.driver.find_elements_by_class_name('message-center-popup__content')
            all_text = [i.text for i in all_msg if ('΢��' or '�ֻ�') in i.text]
            if all_text:
                name_wechat_phone_msg.append(all_text[0])
            click(S('.message-center-popup__close-icon'))
        for text in name_wechat_phone_msg:
            all_list = text.split('��')
            name = all_list[0].replace('����ͬ�������Լ֪ͨ\n', '').replace('ͬ������ĺ�����Լ', '')
            wechatid = all_list[1].replace('�����㽻������ϵ��ʽ��', '').replace('����ȥ������ҳ�鿴��', '').replace('�����鿴', '').replace(
                '΢�ţ�', '').replace('\n', '')

            if len(all_list) == 3:
                phonenum = all_list[2].replace('����ȥ������ҳ�鿴��', '').replace('�����鿴', '').replace('�ֻ���', '').replace('\n',
                                                                                                                '')
            else:
                phonenum = 0
            msg_data_dict = {'����': name, '΢�ź�': wechatid, '�ֻ���': phonenum}
            msg_data_list.append(msg_data_dict)

        return msg_data_list

    def close_ad(self):
        """
        �ر����������
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
        �ر�������ʾ
        """
        button_list = ['֪����', '��һ��', '��һ��', '�� ��', '���']
        if any([Button(i).exists() for i in button_list]):
            while sum(map(len, [find_all(Button(i)) for i in button_list])):
                for i in button_list:
                    if Button(i).exists():
                        click(Button(i))
                self.close_verify()  # �鿴�Ƿ���Ҫ������֤

    def choose_class(self, big_class, small_class):
        """
        ѡ����Ŀ�� С��Ŀ����

        {'�������': ['���', '����', '����'],
        '��������': ['����', 'Ůװ', '��װ', '����'],
        '��������': ['ֽ������', '���˻���'],
        '���ܼҾ�': ['������Ʒ', '�����þ�', '��������', '���', '����Ʒ', '����', '�;�', '�Ҿ�', '�Ҿ���Ʒ', '����þ�', '��������', '�ƾ�', '����'],
        '����': ['����', 'ˮ��', '�߲�', '�䶳ʳƷ', '����ˮ��'],
        '��ױ': ['����Ʒ', '��ױƷ'],
        'ĸӤ����': ['ͯЬ', '�̷۸�ʳ', '�и���Ʒ', 'Ӥͯ��Ʒ', 'ͯװ', '������Ʒ', 'ֽ���'],
        'ʳƷ����': ['�����ζ', '��ʳ', '��ͳ�̲�', 'Ӫ������', '����'],
        '3C����ҵ�': ['�ֻ�', '����', '�������', 'Ӱ������', '�����豸'],
        'ͼ������': ['ͼ��', 'ѧϰ��Ʒ'],
        'Ьѥ���': ['���', '��Ь', 'ŮЬ'],
        '�˶�����': ['�˶�����', '�˶���', '�����ɽ', '�˶���', '�˶�Ь'],
        '�ӱ�����': ['�۾�', '��Ʒ', '�ӱ�'],
        '�鱦����': ['�Ŷ��ղ�', '�鱦�ƽ�']}


        """
        all_class = self.driver.find_elements_by_xpath('//*/span[@class="false index__valueItem___xcGQU"]')
        ac = [i.text for i in all_class]
        # print(ac)
        if '�鱦����' not in ac:
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
        # ��ҳ
        go_to(self.url)
        sleep(3)

        self.scan_qr()  # �ȴ�ɨ���ά��

        wait_until(Text('��������').exists)  # �ȴ�����
        sleep(2)
        self.close_ad()  # ����й����رչ��
        sleep(1)
        self.close_guide()  # �ر�������ʾ
        click('Ӫ������')  # ���Ӫ������

        # Ӫ������ҳ��
        wait_until(Text('�ɽ����').exists)  # �ȴ�����
        self.close_guide()  # �ر�������ʾ
        click('���˹㳡')  # ������˹㳡

        # ���˹㳡ҳ��
        wait_until(Text('������Ŀ').exists)  # �ȴ�����

        self.close_guide()  # �ر�����
        # self.close_msg() # �ر���Ϣ
        print(self.get_wechatid_phonenum())
        sleep(2)
        self.choose_class('ʳƷ����', '��ʳ')  # ѡ����Ŀ

    def main(self):
        self.open_first_page()

    def get_daren_page_data():
        select_values_class = '.index__RadioMultiDropMenuItem___2NJX5'
        select_values = asd.driver.find_elements_by_css_selector(select_values_class)
        click(select_values[1])
        daren_data_dict = {}
        daren_cards = asd.driver.find_elements_by_xpath('//div[@class="daren-card"]')
        daren_cards = [i for i in daren_cards if i.text.split('\n')[-1] != '�ܾ�����']
        for daren in daren_cards:
            daren_name = daren.find_element_by_class_name('list-table-info-right-name__nickname').text
            daren_values = daren.find_elements_by_css_selector('.daren-card-keyword__block-value')
            fans_num = daren_values[0].text.replace('\n', '')  # ��˿��
            average_sales = daren_values[1].text.replace('\n', '')  # �������۶�
            live_online_num = daren_values[2].text.replace('\n', '')  # ��������
            conversion_value = daren_values[3].text.replace('\n', '')  # ת��ֵ
            commission_rate = daren_values[4].text.replace('\n', '')  # Ӷ��
            category = daren.find_element_by_css_selector('.list-table-info-right__cate').text
            area = daren.find_element_by_css_selector('.list-table-info-right__city').text
            try:
                has_contact_num = daren.find_element_by_css_selector('.list-table-info-right-name__sex')
                has_contact_num = True
            except:
                has_contact_num = False
            print(daren_name, category, area, has_contact_num)
            # daren_data_dict = {'����':daren_name, '������Ŀ':daren_all[1], '��������':daren_all[2]}


if __name__ == "__main__":
    asd = DouDian()
    asd.main()