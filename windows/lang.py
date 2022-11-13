from windows import Menu
from PyQt5.QtWidgets import QFileDialog, QLabel
from PyQt5.QtGui import QPixmap
from db import Lang, LangName
import shutil
from glob import glob


class LangMainWindow(Menu):
    def __init__(self):
        super().__init__('ui/lang1.ui')
        self.update_table()
        self.btn1.clicked.connect(self.click1)
        self.btn2.clicked.connect(self.click2)
        self.btn3.clicked.connect(self.click3)

    def update_table(self):
        langs = Lang.select_all()
        head = ['ID', 'Название', 'Картинка']
        self.load_table(head, langs)
        for i, lang in enumerate(langs):
            file = glob('lang/{}.*'.format(lang[0]))[0]
            pic = QPixmap(file)
            pic = pic.scaledToWidth(30)
            pic = pic.scaledToHeight(30)
            label = QLabel(self)
            label.setPixmap(pic)
            self.table.setCellWidget(i, 2, label)
        self.table.resizeColumnsToContents()
        self.update_menu()

    def click1(self):
        try:
            name = self.line1.text()
            file = QFileDialog.getOpenFileName(self, 'Картинка языка ' + name, '')[0]
            Lang.insert(name)
            self.line1.setText('')
            lang_id = Lang.select_name(name)[0][0]
            shutil.copyfile(file, 'lang/{}.{}'.format(lang_id, file.split('.')[-1]))
            self.update_table()
        except Exception:
            pass

    def click2(self):
        try:
            id_ = int(self.line21.text())
            name = int(self.line22.text())
            Lang.update(id_, name)
            self.line21.setText('')
            self.line22.setText('')
            self.update_table()
        except Exception:
            pass

    def click3(self):
        try:
            id_ = int(self.line3.text())
            Lang.delete(id_)
            self.line3.setText('')
            self.update_table()
        except Exception:
            pass


class LangNamesWindow(Menu):
    def __init__(self):
        super().__init__('ui/lang2.ui')
        langs = Lang.select_all()
        self.langs = {_[0]: _[1] for _ in langs}
        self.langs_ = {_[1]: _[0] for _ in langs}
        self.update_table()
        self.combo11.addItems([''] + list(self.langs.values()))
        self.combo31.addItems([''] + list(self.langs.values()))
        self.btn1.clicked.connect(self.click1)
        self.btn3.clicked.connect(self.click3)

    def update_table(self):
        names = [[self.langs[_[1]], _[0]] for _ in LangName.select_all()]
        head = ['Язык', 'Название']
        self.load_table(head, names)
        self.update_menu()

    def click1(self):
        try:
            lang_id = self.langs_[self.combo11.currentText()]
            name = self.line12.text()
            LangName.insert(lang_id, name)
            self.combo11.setCurrentText('')
            self.line12.setText('')
            self.update_table()
        except Exception:
            pass

    def click3(self):
        try:
            lang_id = self.langs_[self.combo31.currentText()]
            name = self.line32.text()
            LangName.delete(lang_id, name)
            self.combo31.setCurrentText('')
            self.line32.setText('')
            self.update_table()
        except Exception:
            pass
