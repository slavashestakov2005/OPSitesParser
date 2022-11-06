from db.db import evaluate, execute


class Lang:
    @staticmethod
    def select_all():
        return evaluate("SELECT * FROM lang")

    @staticmethod
    def select_name(name):
        return evaluate("SELECT * FROM lang WHERE name='{}'".format(name))

    @staticmethod
    def insert(name):
        execute("INSERT INTO lang (name) VALUES ('{}')".format(name))

    @staticmethod
    def update(id_, name):
        execute("UPDATE lang SET name = '{}' WHERE id = {}".format(name, id_))

    @staticmethod
    def delete(id_):
        execute("DELETE FROM lang WHERE id = {}".format(id_))
