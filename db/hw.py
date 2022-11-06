from db.db import evaluate, execute


class HW:
    @staticmethod
    def select_all():
        return evaluate("SELECT * FROM hw")

    @staticmethod
    def insert(name, langs, tasks):
        execute("INSERT INTO hw (name, langs, tasks) VALUES ('{}', '{}', '{}')".format(name, langs, tasks))

    @staticmethod
    def delete(id_):
        execute("DELETE FROM hw WHERE id = {}".format(id_))
