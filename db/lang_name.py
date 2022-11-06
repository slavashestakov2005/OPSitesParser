from db.db import evaluate, execute


class LangName:
    @staticmethod
    def select_all():
        return evaluate("SELECT * FROM lang_name")

    @staticmethod
    def insert(lang_id, name):
        execute("INSERT INTO lang_name (name, lang_id) VALUES ('{}', {})".format(name, lang_id))

    @staticmethod
    def delete(lang_id, name):
        execute("DELETE FROM lang_name WHERE name = '{}' AND lang_id = {}".format(name, lang_id))
