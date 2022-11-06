from db.db import evaluate, execute


class Group:
    @staticmethod
    def select_all():
        return evaluate("SELECT * FROM ugroup")

    @staticmethod
    def select_id(id_):
        return evaluate("SELECT * FROM ugroup WHERE id={}".format(id_))

    @staticmethod
    def select_name(name):
        return evaluate("SELECT * FROM ugroup WHERE name='{}'".format(name))

    @staticmethod
    def insert(name):
        execute("INSERT INTO ugroup (name) VALUES ('{}')".format(name))

    @staticmethod
    def update(id_, name):
        execute("UPDATE ugroup SET name = '{}' WHERE id = {}".format(name, id_))

    @staticmethod
    def delete(id_):
        execute("DELETE FROM ugroup WHERE id = {}".format(id_))
