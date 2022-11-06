from db.db import evaluate, execute


class HWGroup:
    @staticmethod
    def select_all():
        return evaluate("SELECT * FROM hw_group")

    @staticmethod
    def insert(hw_id, group_id):
        execute("INSERT INTO hw_group (hw_id, group_id) VALUES ({}, {})".format(hw_id, group_id))

    @staticmethod
    def delete(hw_id, group_id):
        execute("DELETE FROM hw_group WHERE hw_id = {} AND group_id = {}".format(hw_id, group_id))
