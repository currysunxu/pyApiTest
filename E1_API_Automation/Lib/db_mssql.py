#import pymssql


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

    # return the list of column field and value dictionary
    def exec_query_return_dict_list(self, sql):
        cur = self.__get_connect()
        cur.execute(sql)
        result_list = cur.fetchall()
        cols = cur.description

        result_dict_list = []
        for i in range(len(result_list)):
            col_value_dict = {}
            for j in range(len(cols)):
                col_value_dict[cols[j][0]] = result_list[i][j]
            result_dict_list.append(col_value_dict)

        self.conn.close()
        return result_dict_list
