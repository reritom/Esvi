from esvi import fields
import sqlite3

class Sqlite3Adapter():
    def __init__(self, cnx):
        self.cnx = cnx
        self.db = sqlite3.connect(cnx.get_path())

    def initialise(self, query, cnx):
        field_list = []
        print("Query fields are {}".format(query.get_fields()))
        for key, value in query.get_fields().items():
            field_string = "{} {}".format(key, value.get_type())

            if value.is_primary():
                field_string += " PRIMARY KEY"
            field_list.append(field_string)

        joined_fields = "(" + ','.join(field_list) + ")"


        sql_query = 'CREATE TABLE {} '.format(query.get_model_name()) + joined_fields + ';'
        print("Query is {}".format(sql_query))

        with sqlite3.connect(cnx.get_path()) as conn:
            conn.cursor().execute(sql_query)
        if conn:
            conn.close

        # Try and retrieve

        # If success, make sure the fields match our model

        # If so, continue

        # Else, raise exception that a migration is needed

        # if not retrieved

        # Insert new model
        pass

    def create(self, query, cnx):
        base_query = 'INSERT INTO {} '.format(query.get_model_name())

        key_list = []
        value_list = []

        print("Creating model with:")
        for key, value in query.get_content().items():
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

        with sqlite3.connect(cnx.get_path()) as conn:
            conn.cursor().execute(sql_query)
            print("Model created {}".format(conn.cursor().lastrowid))
        if conn:
            conn.close

    def delete(self):
        pass

    def retrieve(self, query, cnx):
        for field_name, field_value in query.get_fields().items():
            if field_value.__class__ == fields.PrimaryKey:
                pk_name = field_name
                break

        sql_query = "SELECT * FROM {table} WHERE {pk_name} = {pk_value};".format(table=query.get_model_name(),
                                                                                 pk_name=pk_name,
                                                                                 pk_value=query.get_content())

        with sqlite3.connect(cnx.get_path()) as conn:
            conn.cursor().execute(sql_query)
            models = conn().cursor.fetchall()
        if conn:
            conn.close

        return models



    def update(self, query):
        def retrieve(self, query):
            with sqlite3.connect(cnx.get_path()) as conn:
                pass
            if conn:
                conn.close

    def filter(self, query):
        def retrieve(self, query):
            with sqlite3.connect(cnx.get_path()) as conn:
                pass
            if conn:
                conn.close

    def get_models(self, query, cnx):
        print("Getting models")
        sql_query = "SELECT * FROM {table};".format(table=query.get_model_name())
        print("Query is {}".format(sql_query))

        with sqlite3.connect(cnx.get_path()) as conn:
            conn.cursor().execute(sql_query)
            models = conn.cursor().fetchall()
        if conn:
            conn.close

        print(models)

        return models
