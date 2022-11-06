from windows import Menu
from db import HW, Group, HWGroup, Lang
import os


class HWListWindow(Menu):
    def __init__(self):
        super().__init__('ui/hw1.ui')
        self.update_table()
        self.btn1.clicked.connect(self.click1)
        self.btn3.clicked.connect(self.click3)

    def update_table(self):
        hws = HW.select_all()
        head = ['ID', 'Название', 'Языки', 'Задачи']
        self.load_table(head, hws)
        self.update_menu()

    def click1(self):
        try:
            name = self.line11.text()
            langs = self.line12.text()
            tasks = self.line13.text()
            HW.insert(name, langs, tasks)
            self.line11.setText('')
            self.line12.setText('')
            self.line13.setText('')
            self.update_table()
        except Exception:
            pass

    def click3(self):
        try:
            id_ = int(self.line3.text())
            HW.delete(id_)
            self.line3.setText('')
            self.update_table()
        except Exception:
            pass


class HWGroupWindow(Menu):
    def __init__(self):
        super().__init__('ui/hw2.ui')
        hws = HW.select_all()
        groups = Group.select_all()
        self.hw01 = {_[0]: _[1] for _ in hws}
        self.hw10 = {_[1]: _[0] for _ in hws}
        self.hw = {_[0]: _ for _ in hws}
        self.group01 = {_[0]: _[1] for _ in groups}
        self.group10 = {_[1]: _[0] for _ in groups}
        self.update_table()
        self.combo11.addItems([''] + list(self.group01.values()))
        self.combo31.addItems([''] + list(self.group01.values()))
        self.combo12.addItems([''] + list(self.hw01.values()))
        self.combo32.addItems([''] + list(self.hw01.values()))
        self.btn1.clicked.connect(self.click1)
        self.btn3.clicked.connect(self.click3)

    def update_table(self):
        hwg = [[self.group01[_[1]], self.hw01[_[0]]] for _ in HWGroup.select_all()]
        head = ['Группа', 'ДЗ']
        self.load_table(head, hwg)
        self.update_menu()

    def click1(self):
        try:
            group_name, hw_name = self.combo11.currentText(), self.combo12.currentText()
            group_id = self.group10[group_name]
            hw_id = self.hw10[hw_name]
            hw = self.hw[hw_id]
            HWGroup.insert(hw_id, group_id)
            self.combo11.setCurrentText('')
            self.combo12.setCurrentText('')
            self.update_table()
            with open('groups/{}/tasks/{}.txt'.format(group_name, hw_name), 'w', encoding='UTF-8') as f:
                langs = {_[0]: _[1] for _ in Lang.select_all()}
                s = '|'.join(langs[int(_)] for _ in hw[2].split('|')) + '\n'
                f.write(s)
                f.write(hw[3].replace('|', '\n'))
        except Exception:
            pass

    def click3(self):
        try:
            group_name, hw_name = self.combo31.currentText(), self.combo32.currentText()
            group_id = self.group10[group_name]
            hw_id = self.hw10[hw_name]
            HWGroup.delete(hw_id, group_id)
            self.combo31.setCurrentText('')
            self.combo32.setCurrentText('')
            self.update_table()
            os.remove('groups/{}/tasks/{}.txt'.format(group_name, hw_name))
            file = 'groups/{}/tasks_results/{}.'.format(group_name, hw_name)
            if os.path.exists(file + 'md'):
                os.remove(file + 'md')
            if os.path.exists(file + 'xlsx'):
                os.remove(file + 'xlsx')
        except Exception:
            pass
