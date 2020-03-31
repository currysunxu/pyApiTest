import pymysql


class MYSQLHelper(object):
    def __init__(self, database):
        self.server, self.port = database["Server"].split(':')
        self.user = database["User"]
        self.password = database["Password"]

    def __get_connect(self):
        self.conn = pymysql.connect(self.server, self.user, self.password, port=int(self.port))
        cursor = self.conn.cursor()
        if not cursor:
            raise(NameError, "Failed to connect to DB")
        else:
            return cursor

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