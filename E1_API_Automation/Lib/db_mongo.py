from pymongo import MongoClient


class MongoHelper(object):
    def __init__(self, database_setting, db_name):
        self.server = database_setting["Server"]
        self.user = database_setting["User"]
        self.password = database_setting["Password"]
        self.db_name = db_name

    def __get_connect(self):
        self.conn = MongoClient('mongodb://' + self.server + '/')
        self.conn.admin.authenticate(self.user, self.password, mechanism='SCRAM-SHA-1')
        db = self.conn.get_database(self.db_name)
        return db

    # return the list of column field and value dictionary
    def exec_query_return_dict_list(self, table_name, find_condition):
        db = self.__get_connect()
        session = db[table_name]
        result_dict_list = []
        try:
            rs = session.find(find_condition)
            for item in rs:
                result_dict_list.append(item)
        finally:
            self.conn.close()
        return result_dict_list

    # update_values should be something like { "alexa": "12345" }
    def exec_update(self, table_name, find_condition, update_values):
        db = self.__get_connect()
        session = db[table_name]
        try:
            session.update_one(find_condition, {"$set": update_values})
        finally:
            self.conn.close()


