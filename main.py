from doudian import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QTableWidget, QMainWindow
from qt_material import apply_stylesheet
import sys
import os
import time

CLASS_VALUE = {'玩具乐器': ['玩具', '乐器', '其他'],
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


class Run:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main = QMainWindow()
        self.window = Ui_MainWindow()
        self.window.setupUi(self.main)
        # 类目设置
        self.window.big_class_comboBox.addItems(CLASS_VALUE.keys())  # 设置大类目数据
        self.window.big_class_comboBox.setCurrentIndex(7)  # 设置大类目默认数据
        self.big_class_value = self.window.big_class_comboBox.currentText()  # 获取大类目已选择字符串
        self.window.big_class_comboBox.currentIndexChanged.connect(self.set_small_class_list)  # 当大类目数据改变时更新小类目数据
        self.window.small_class_comboBox.addItems(CLASS_VALUE[self.big_class_value])  # 设置小类目数据
        self.small_value = self.window.small_class_comboBox.currentText()  # 已选择字符串
        self.window.small_class_comboBox.currentIndexChanged.connect(self.get_small_class_value)

        # 设置初始数据
        self.window.save_name_lineEdit.setText('doudian.xlsx')
        self.sales_list = [
            [False, '¥0-100'][self.window.sales_100_500_checkBox.isChecked()],
            [False, '¥500-1000'][self.window.sales_500_1k_checkBox.isChecked()],
            [False, '¥1000-5000'][self.window.sales_1k_5k_checkBox.isChecked()],
            [False, '¥5000-1万'][self.window.sales_5k_1w_checkBox.isChecked()],
            [False, '¥1万-5万'][self.window.sales_1w_5w_checkBox.isChecked()],
            [False, '¥5万-10万'][self.window.sales_5w_10w_checkBox.isChecked()],
            [False, '¥10万-50万'][self.window.sales_10w_50w_checkBox.isChecked()],
            [False, '¥100万-500万'][self.window.sales_100w_500w_checkBox.isChecked()],
            [False, '达人未授权'][self.window.sales_is_none_checkBox.isChecked()]
        ]
        self.sales_list = [i for i in self.sales_list if i is not False]

        self.apply_stylesheet = apply_stylesheet(self.app, theme='dark_teal.xml')
        self.main.show()
        sys.exit(self.app.exec_())

    # 类目设置槽函数
    def set_small_class_list(self):
        """
        当大类目改变时设置小类目列表
        """
        self.big_class_value = self.window.big_class_comboBox.currentText()
        self.window.small_class_comboBox.clear()  # 清除旧数据
        self.window.small_class_comboBox.addItems(CLASS_VALUE[self.big_class_value])  # 设置新数据

    def get_small_class_value(self):
        """
        当小类目改变时，获取小类目选择字符串
        """
        self.small_value = self.window.small_class_comboBox.currentText()


if __name__ == '__main__':
    run = Run()
    run()
