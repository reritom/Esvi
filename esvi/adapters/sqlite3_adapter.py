from esvi import fields
import sqlite3

class Sqlite3Adapter():
    def __init__(self, cnx):
        self.cnx = cnx
        self.db = sqlite3.connect(cnx.get_path())

    def initialise_model(self, query, cnx):
        field_list = []
        print("Query fields are {}".format(query.get_fields()))
        for key, value in query.get_fields().items():
            field_string = "{} {}".format(key, value.get_type())

            if value.is_primary():
                field_string += " PRIMARY KEY"
            field_list.append(field_string)

        joined_fields = "(" + ','.join(field_list) + ")"


        sql_query = 'CREATE TABLE IF NOT EXISTS {} '.format(query.get_model_name()) + joined_fields + ';'
        print("Query is {}".format(sql_query))

        with sqlite3.connect(cnx.get_path()) as conn:
            conn.cursor().execute(sql_query)
        if conn:
            conn.close


    def create_model(self, query, cnx):
        columns = self.get_model_definition(query, cnx)


        base_query = 'INSERT INTO {} '.format(query.get_model_name())

        key_list = []
        value_list = []

        print("Creating model with:")
        for key in columns:
            value = query.get_content()[key]
            print(key, value)
            key_list.append(key)

            if isinstance(value, str):
                value_list.append("'{}'".format(value))
            else:
                value_list.append(str(value))

        key_string = "(" + ' , '.join(key_list) + ")"
        value_string = "(" + ' , '.join(value_list) + ")"

        sql_query = base_query + key_string + ' VALUES ' + value_string + ';'
        print("Query is {}".format(sql_query))

        connection = sqlite3.connect(cnx.get_path())
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
        print("Model created {}".format(cursor.lastrowid))
        return cursor.lastrowid

    def delete_model(self):
        pass

    def retrieve_by_pk(self, query, cnx):
        print("In retrieve_by_pk")
        for field_name, field_value in query.get_fields().items():
            if field_value.__class__ == fields.PrimaryKey:
                pk_name = field_name
                break

        sql_query = "SELECT * FROM {table} WHERE {pk_name} = '{pk_value}';".format(table=query.get_model_name(),
                                                                                 pk_name=pk_name,
                                                                                 pk_value=query.get_content())

        print("Query is {}".format(sql_query))

        connection = sqlite3.connect(cnx.get_path())
        cursor = connection.cursor()
        cursor.execute(sql_query)
        model = cursor.fetchall()[0]
        print(model)

        columns = self.get_model_definition(query, cnx)
        model_dict = {column: model[index] for index, column in enumerate(columns)}
        return model_dict




    def update_model(self, query, cnx):
        # Retrieve the list of column names in the correct order
        columns = self.get_model_definition(query, cnx)

        for field_name in query.get_fields().keys():
            field_value = query.get_fields()[field_name]
            if field_value.__class__ == fields.PrimaryKey:
                pk_name = field_name
                pk_value = query.get_content()[field_name]
                break

        base_query = 'UPDATE {} SET'.format(query.get_model_name())

        key_value_list = []

        print("Updating model with content {}".format(query.get_content()))

        print("Updating model with:")

        for key in columns:
            print("Key is {}".format(key))
            value = query.get_content()[key]
            print(key, value)

            if isinstance(value, str):
                value = ("'{}'".format(value))
            else:
                value = str(value)

            key_value_list.append('{}={}'.format(key, value))

        key_value_string = ' , '.join(key_value_list)


        if isinstance(pk_value, str):
            pk_value = ("'{}'".format(pk_value))
        else:
            pk_value = str(pk_value)

        sql_query = '{base_query} {key_value_string} WHERE {pk_name} = {pk_value};'.format(base_query=base_query,
                                                                                           key_value_string=key_value_string,
                                                                                           pk_name=pk_name,
                                                                                           pk_value=pk_value)

        print("Query is {}".format(sql_query))

        connection = sqlite3.connect(cnx.get_path())
        cursor = connection.cursor()
        cursor.execute(sql_query)
        models = cursor.fetchall()
        connection.commit()
        print(models)

        return models


    def filter_models(self, query, cnx):
        pass

    def get_model_definition(self, query, cnx):
        print("In get_model_definition for {}".format(query.get_model_name()))
        sql_query = 'PRAGMA TABLE_INFO({})'.format(query.get_model_name())

        connection = sqlite3.connect(cnx.get_path())
        cursor = connection.cursor()
        cursor.execute(sql_query)
        columns_tuples = cursor.fetchall()

        columns = [tup[1] for tup in columns_tuples]
        print("Columns are {}".format(columns))
        return columns

    def retrieve_all(self, query, cnx):
        print("Getting models")
        sql_query = "SELECT * FROM {table};".format(table=query.get_model_name())
        print("Query is {}".format(sql_query))
        print("Path is {}".format(cnx.get_path()))

        connection = sqlite3.connect(cnx.get_path())
        cursor = connection.cursor()
        cursor.execute(sql_query)
        models = cursor.fetchall()

        # Models is a list of tuples, so we will convert it into a list of dictionaries
        columns = self.get_model_definition(query, cnx)

        list_of_models = []

        for model in models:
            model_dict = {column: model[index] for index, column in enumerate(columns)}
            list_of_models.append(model_dict)

        print(list_of_models)

        return list_of_models
