from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class CassandraHelper(object):
    def __init__(self, database):
        self.contact_points = database["Server"].split(",")
        self.user = database["User"]
        self.password = database["Password"]
        self.key_space = database["KeySpace"]

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
            result_dict_list = self.convert_from_db_format_to_dict(rs.current_rows)
        finally:
            self.cluster.shutdown()
        return result_dict_list

    def convert_from_db_format_to_dict(self, db_format_value_list):
        result_dict_list = []
        for i in range(len(db_format_value_list)):
            result_field_dict = {}
            db_format_field_value = db_format_value_list[i]
            for j in range(len(db_format_field_value._fields)):
                db_column_value = db_format_field_value[j]
                if isinstance(db_column_value, list):
                    db_column_value = self.convert_from_db_format_to_dict(db_column_value)
                result_field_dict[db_format_field_value._fields[j]] = db_column_value
            result_dict_list.append(result_field_dict)
        return result_dict_list
