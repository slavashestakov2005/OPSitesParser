from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAction, QTableWidgetItem
from PyQt5.QtCore import Qt
from db import Group, User


class Menu(QMainWindow):
    def add_action(self, menu, func, text, separator=False):
        action = QAction(str(text), self)
        action.triggered.connect(func)
        menu.addAction(action)
        if separator:
            menu.addSeparator()

    def load_table(self, head, data):
        self.table.setColumnCount(len(head))
        self.table.setHorizontalHeaderLabels(head)
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def open_window(self, w, *args):
        self.w = w() if not args else w(*args)
        self.close()
        self.w.show()

    def __init__(self, file):
        super().__init__()
        uic.loadUi(file, self)
        self.update_menu()

    def update_menu(self):
        self.menu_1.clear()
        self.menu_2.clear()
        self.menu_3.clear()
        self.menu_4.clear()
        self.add_action(self.menu_1, self.push1s, 'Настройки', True)
        self.add_action(self.menu_2, self.push2s, 'Настройки', True)
        self.add_action(self.menu_3, self.push31, 'Семейства')
        self.add_action(self.menu_3, self.push32, 'Названия')
        self.add_action(self.menu_4, self.push41, 'Список ДЗ')
        self.add_action(self.menu_4, self.push42, 'Задать ДЗ')
        for group in Group.select_all():
            self.add_action(self.menu_1, self.push1, group[1])
        for user in User.select_all():
            self.add_action(self.menu_2, self.push2, '{} ({})'.format(user[2], user[1]))

    def push1s(self, *args):
        from windows.group import GroupSettingsWindow as w
        self.open_window(w)

    def push2s(self, *args):
        from windows.user import UserSettingsWindow as w
        self.open_window(w)

    def push1(self, *args):
        try:
            from windows.group import GroupWindow as w
            group_name = self.sender().text()
            group_id = Group.select_name(group_name)[0][0]
            self.open_window(w, group_id, group_name)
        except Exception as ex:
            pass

    def push2(self, *args):
        try:
            from windows.user import UserWindow as w
            acmp_id = int(self.sender().text().split('(')[-1][:-1])
            acmp_name = User.select_acmp(acmp_id)[0][2]
            self.open_window(w, acmp_id, acmp_name)
        except Exception as ex:
            pass

    def push31(self, *args):
        from windows.lang import LangMainWindow as w
        self.open_window(w)

    def push32(self, *args):
        from windows.lang import LangNamesWindow as w
        self.open_window(w)

    def push41(self, *args):
        from windows.hw import HWListWindow as w
        self.open_window(w)

    def push42(self, *args):
        from windows.hw import HWGroupWindow as w
        self.open_window(w)
