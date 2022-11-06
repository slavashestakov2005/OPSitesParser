from windows import Menu
from db import User


class UserSettingsWindow(Menu):
    def __init__(self):
        super().__init__('ui/user_settings.ui')
        self.update_table()
        self.btn1.clicked.connect(self.click1)
        self.btn2.clicked.connect(self.click2)
        self.btn3.clicked.connect(self.click3)

    def update_table(self):
        users = User.select_all()
        head = ['ID', 'Acmp ID', 'Имя']
        self.load_table(head, users)
        self.update_menu()

    def click1(self):
        try:
            acmp_id = int(self.line1.text())
            User.insert(acmp_id)
            self.line1.setText('')
            self.update_table()
        except Exception:
            pass

    def click2(self):
        try:
            id_ = int(self.line2.text())
            User.update(id_)
            self.line2.setText('')
            self.update_table()
        except Exception:
            pass

    def click3(self):
        try:
            id_ = int(self.line3.text())
            User.delete(id_)
            self.line3.setText('')
            self.update_table()
        except Exception:
            pass


class UserWindow(Menu):
    def __init__(self, acmp_id, acmp_name):
        super().__init__('ui/user.ui')
        try:
            with open('groups/_cache/user/{}.txt'.format(acmp_id), 'r', encoding='utf-8') as f:
                data = f.read()
            self.content.setText(data)
        except Exception:
            pass
        self.title.setText(acmp_name)
