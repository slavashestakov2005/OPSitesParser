from db.db import evaluate, execute


class UserGroup:
    @staticmethod
    def select_all():
        return evaluate("SELECT * FROM user_group")

    @staticmethod
    def select_group(group_id):
        return evaluate("SELECT * FROM user_group WHERE group_id={}".format(group_id))

    @staticmethod
    def insert(user_id, group_id):
        execute("INSERT INTO user_group (user_id, group_id) VALUES ({}, {})".format(user_id, group_id))

    @staticmethod
    def delete(user_id, group_id):
        execute("DELETE FROM user_group WHERE user_id = {} AND group_id = {}".format(user_id, group_id))
