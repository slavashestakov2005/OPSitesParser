from windows import Menu
from db import Group, User, UserGroup, Lang, LangName
from PyQt5.QtWidgets import QMessageBox
import os
import shutil
from acmp.parser import parse_group as parse
import threading


def start_parsing(group_name):
    cache_folder, group_folder = 'groups/_cache/', 'groups/' + group_name + '/'
    with open(group_folder + 'users.txt', 'r') as f:
        data = f.read().strip()
    langs = {_[0]: _[1] for _ in Lang.select_all()}
    lang_translate = {_[0]: langs[_[1]] for _ in LangName.select_all()}
    args = cache_folder, group_folder, [int(_) for _ in data.split('\n')], lang_translate
    threading.Thread(target=parse, args=args).start()


class GroupSettingsWindow(Menu):
    def __init__(self):
        super().__init__('ui/group_settings.ui')
        self.update_table()
        self.btn1.clicked.connect(self.click1)
        self.btn2.clicked.connect(self.click2)
        self.btn3.clicked.connect(self.click3)

    def update_table(self):
        groups = Group.select_all()
        head = ['ID', 'Название']
        self.load_table(head, groups)
        self.update_menu()

    def click1(self):
        try:
            name = self.line1.text()
            if name == '_cache':
                raise ValueError('')
            Group.insert(name)
            self.line1.setText('')
            self.update_table()
            folder = 'groups/' + name
            if not os.path.exists(folder):
                os.makedirs(folder)
                os.makedirs(folder + '/tasks')
                os.makedirs(folder + '/tasks_results')
                os.makedirs(folder + '/users_results')
                with open(folder + '/users.txt', 'w'):
                    pass
        except Exception:
            pass

    def click2(self):
        try:
            id_ = int(self.line21.text())
            name_ = Group.select_id(id_)[0][1]
            name = self.line22.text()
            Group.update(id_, name)
            os.rename('groups/' + name_, 'groups/' + name)
            self.line21.setText('')
            self.line22.setText('')
            self.update_table()
        except Exception:
            pass

    def click3(self):
        try:
            id_ = int(self.line3.text())
            name_ = Group.select_id(id_)[0][1]
            Group.delete(id_)
            shutil.rmtree('groups/' + name_)
            self.line3.setText('')
            self.update_table()
        except Exception:
            pass


class GroupWindow(Menu):
    def __init__(self, group_id, group_name):
        super().__init__('ui/group.ui')
        self.group = group_id
        self.name = group_name
        all_users = User.select_all()
        self.users = {_[0]: _[2] + ' (' + str(_[1]) + ')' for _ in all_users}
        self.acmp2user = {_[1]: _[0] for _ in all_users}
        self.user2acmp = {_[0]: _[1] for _ in all_users}
        self.btn1.clicked.connect(self.click1)
        self.btn2.clicked.connect(self.click2)
        self.btn3.clicked.connect(self.click3)
        self.combo1.addItems([''] + list(self.users.values()))
        self.title.setText(group_name)
        self.update_table()

    def update_table(self):
        self.ug = UserGroup.select_group(self.group)
        groups = [[_[0], self.users[_[0]]] for _ in self.ug]
        with open('groups/' + self.name + '/users.txt', 'w') as f:
            for _ in self.ug:
                f.write(str(self.user2acmp[_[0]]))
                f.write('\n')
        head = ['ID', 'Имя']
        self.load_table(head, groups)
        self.update_menu()

    def click1(self):
        try:
            acmp_id = int(self.combo1.currentText().split('(')[-1][:-1])
            user_id = self.acmp2user[acmp_id]
            UserGroup.insert(user_id, self.group)
            self.combo1.setCurrentText('')
            self.update_table()
        except Exception:
            pass

    def click2(self):
        try:
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Вы уверены?")
            dialog.setText("Обновление может быть долгим...\nОно будет выполнено асинхронно, результаты будут сохранены в папке группы.")
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dialog.setIcon(QMessageBox.Question)
            result = dialog.exec()
            if result == QMessageBox.Yes:
                start_parsing(self.name)
        except Exception:
            pass

    def click3(self):
        try:
            user_id = int(self.line3.text())
            UserGroup.delete(user_id, self.group)
            self.line3.setText('')
            self.update_table()
        except Exception:
            pass
