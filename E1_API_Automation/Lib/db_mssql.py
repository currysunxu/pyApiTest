import pymssql


class MSSQLHelper(object):
    def __init__(self, database, db_engine):
        self.server, self.port = database["Server"].split(',')

        self.user = database["User"]
        self.password = database["Password"]
        self.db_engine = db_engine

    def __get_connect(self):
        self.conn = pymssql.connect(self.server, self.user, self.password, self.db_engine, port=self.port)
        cursor = self.conn.cursor()
        if not cursor:
            raise(NameError, "Failed to connect to DB")
        else:
            return cursor

    def exec_non_query(self, sql_query):
        cur = self.__get_connect()
        cur.execute(sql_query)
        self.conn.commit()
        self.conn.close()

    def exec_query(self, sql):
        cur = self.__get_connect()
        cur.execute(sql)
        result_list = cur.fetchall()
        self.conn.close()
        return result_list

    def execute_proc(self, proc_name, parameters):
        cur = self.__get_connect()
        cur.callproc(proc_name, parameters)
        self.conn.commit()
        self.conn.close()
