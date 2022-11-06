from db.db import evaluate, execute
from acmp import parse_user_profile as parse


class User:
    @staticmethod
    def select_all():
        return evaluate("SELECT * FROM uuser")

    @staticmethod
    def select_acmp(acmp_id):
        return evaluate("SELECT * FROM uuser WHERE acmp_id={}".format(acmp_id))

    @staticmethod
    def insert(acmp_id):
        try:
            name = parse(acmp_id).name
            execute("INSERT INTO uuser (acmp_id, name) VALUES ({}, '{}')".format(acmp_id, name))
        except Exception:
            pass

    @staticmethod
    def update(id_):
        try:
            res = evaluate("SELECT * FROM uuser WHERE id = {}".format(id_))
            if not res:
                raise ValueError('')
            name = parse(res[0][1]).name
            execute("UPDATE uuser SET name = '{}' WHERE id = {}".format(name, id_))
        except Exception:
            User.delete(id_)

    @staticmethod
    def delete(id_):
        execute("DELETE FROM uuser WHERE id = {}".format(id_))
