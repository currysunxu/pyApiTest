from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class CassandraHelper(object):
    def __init__(self, database, key_space):
        self.contact_points = database["Server"].split(",")
        self.user = database["User"]
        self.password = database["Password"]
        self.key_space = key_space

    def __get_connect(self):
        auth_provider = PlainTextAuthProvider(username=self.user, password=self.password)
        self.cluster = Cluster(contact_points=self.contact_points, auth_provider=auth_provider)
        session = self.cluster.connect(keyspace=self.key_space)

        if not session:
            raise(NameError, "Failed to connect to DB")
        else:
            return session

    # return the list of column field and value dictionary
    def exec_query_return_dict_list(self, sql):
        session = self.__get_connect()
        try:
            rs = session.execute(sql)

            result_dict_list = []
            for result_row in rs.current_rows:
                col_value_dict = {}
                for j in range(len(result_row._fields)):
                    col_value_dict[result_row._fields[j]] = result_row[j]
                result_dict_list.append(col_value_dict)
        finally:
            self.cluster.shutdown()
        return result_dict_list
