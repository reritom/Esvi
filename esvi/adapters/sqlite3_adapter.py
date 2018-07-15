from esvi import fields
from esvi.query import Query
from esvi import exceptions
from typing import Optional
import sqlite3
import datetime
import json

class Sqlite3Adapter():
    def __init__(self, cnx):
        self.cnx = cnx

    def initialise_model(self, query: Query) -> None:
        field_list = []
        add_to_end = []  # Foreign keys need an extra bit of string added to the end

        print("Query fields are {}".format(query.get_fields()))

        for key, value in query.get_fields().items():
            is_foreign = False

            if value.get_type() == "ForeignKey":
                is_foreign = True

                # It is a foreign key, so we will get the primary key of the foreign key
                reference = value.get_reference()
                reference_fields = reference.get_fields()
                reference_model_name = reference.get_model_name()

                for reference_field_name, reference_field in reference_fields.items():
                    if reference_field.is_primary():
                        # We will overwrite the key, value, with that of the reference primary key for the rest of this process
                        key = reference_field_name
                        value = reference_field
                        foreign_query = 'FOREIGN KEY({key}) REFERENCES {reference_table}(id)'.format(key=key,
                                                                                                     reference_table=reference_model_name)
                        add_to_end.append(foreign_query)

            if value.get_type() == "StringField":
                sql_type = "TEXT"

            elif value.get_type() == "IntegerField":
                sql_type = "INTEGER"

            elif value.get_type() == "DateTimeField":
                sql_type = "TIMESTAMP"

            elif value.get_type() == "ObjectField":
                sql_type = "TEXT"

            elif value.get_type() == "JSONField":
                sql_type = "TEXT"

            else:
                raise exceptions.UnsupportedAdapterField()

            if value.is_primary() and not is_foreign:
                sql_type += " PRIMARY KEY"


            field_string = "{} {}".format(key, sql_type)
            field_list.append(field_string)

        joined_fields = "(" + ','.join(field_list + add_to_end) + ")"


        sql_query = 'CREATE TABLE IF NOT EXISTS {} '.format(query.get_model_name()) + joined_fields + ';'
        print("Query is {}".format(sql_query))

        with sqlite3.connect(self.cnx.get_path(), detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            conn.cursor().execute(sql_query)
        if conn:
            conn.close

    def _encode_model(self, query: Query):
        encoded_content = {}

        for field_name, field_item in query.get_fields().items():
            value = query.get_content()[field_name]

            print("In encode, item is {}".format(field_name))
            if field_item.get_type() == "ObjectField":
                encoded = json.dumps(value.serialise()).replace('\'', '\"')
                encoded_content[field_name] = "'{}'".format(encoded)

            elif field_item.get_type() == "JSONField":
                encoded = json.dumps(value).replace('\'', '\"')
                encoded_content[field_name] = "'{}'".format(encoded)

            elif field_item.get_type() == "StringField" or field_item.get_type() == "DateTimeField":
                encoded = value
                encoded_content[field_name] = "'{}'".format(encoded)
            else:
                encoded = value
                encoded_content[field_name] = str(encoded)

        return encoded_content

    def _decode_model(self, sql_encoded_content: dict, query: Query) -> dict:
        decoded_content = {}

        for field_name, field_item in query.get_fields().items():
            encoded_value = sql_encoded_content[field_name]

            if field_item.get_type() == "ObjectField":
                print("Trying to load object field {}".format(encoded_value[1:-1]))
                decoded = json.loads(encoded_value[1:-1])
                decoded_content[field_name] = decoded

            elif field_item.get_type() == "JSONField":
                print("Trying to load json field {}".format(encoded_value[1:-1]))
                decoded = json.loads(encoded_value[1:-1])
                decoded_content[field_name] = decoded

            elif field_item.get_type() == "StringField":
                decoded = encoded_value[1:-1]
                decoded_content[field_name] = decoded

            elif field_item.get_type() == "DateTimeField":
                decoded = encoded_value[1:-1]
                decoded_content[field_name] = decoded
                # TODO, return datetime object

            elif field_item.get_type() == "IntegerField":
                decoded = int(encoded_value)
                decoded_content[field_name] = decoded

            else:
                raise Exception("Unsupported field type")

        return decoded_content


    def create_model(self, query: Query) -> str:
        sql_encoded_content = self._encode_model(query)

        columns = self.get_model_definition(query)

        base_query = 'INSERT INTO {} '.format(query.get_model_name())

        key_list = []
        value_list = []

        print("Creating model with: {}".format(query.get_content()))
        for key in columns:
            value = sql_encoded_content[key]
            print(key, value)
            key_list.append(key)
            value_list.append(value)

        key_string = "(" + ' , '.join(key_list) + ")"
        value_string = "(" + ' , '.join(value_list) + ")"

        sql_query = base_query + key_string + ' VALUES ' + value_string + ';'
        print("Query is {}".format(sql_query))

        connection = sqlite3.connect(self.cnx.get_path(), detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
        print("Model created {}".format(cursor.lastrowid))
        if cursor.lastrowid:
            return self._decode_model(sql_encoded_content, query)

    def delete_model(self, query: Query) -> bool:
        print("In delete_model")
        # Determine the name and value of the primary key
        for field_name in query.get_fields().keys():
            field_value = query.get_fields()[field_name]
            if field_value.is_primary():
                pk_name = field_name
                pk_value = query.get_content()[field_name]
                break

        sql_query = "DELETE FROM {table} WHERE {pk_name} = '{pk_value}';".format(table=query.get_model_name(),
                                                                              pk_name=pk_name,
                                                                              pk_value=pk_value)

        print("The query is {}".format(sql_query))
        connection = sqlite3.connect(self.cnx.get_path(), detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        print("Result is {}".format(result))
        connection.commit()

    def retrieve_by_pk(self, query: Query) -> Optional[dict]:
        print("In retrieve_by_pk")
        for field_name, field_value in query.get_fields().items():
            if field_value.is_primary():
                pk_name = field_name
                break

        sql_query = "SELECT * FROM {table} WHERE {pk_name} = '{pk_value}';".format(table=query.get_model_name(),
                                                                                 pk_name=pk_name,
                                                                                 pk_value=query.get_content())

        print("Query is {}".format(sql_query))

        connection = sqlite3.connect(self.cnx.get_path(), detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()

        if result:
            model = result[0]
            print(model)

            columns = self.get_model_definition(query)
            model_dict = {column: model[index] for index, column in enumerate(columns)}
            return self._decode_model(model_dict, query)

        else:
            raise exceptions.DoesNotExist()


    def update_model(self, query: Query) -> dict:
        # Retrieve the list of column names in the correct order
        columns = self.get_model_definition(query)

        # Determine the name of the primary key
        for field_name in query.get_fields().keys():
            field_value = query.get_fields()[field_name]
            if field_value.is_primary():
                pk_name = field_name
                break

        # Encode the content into an SQL format
        sql_encoded_content = self._encode_model(query)

        # Create list of 'key=value' strings
        key_value_list = []
        for key in columns:
            print("Key is {}".format(key))
            value = sql_encoded_content[key]
            print(key, value)

            key_value_list.append('{}={}'.format(key, value))

        key_value_string = ' , '.join(key_value_list)
        pk_value = sql_encoded_content[pk_name]

        sql_query = 'UPDATE {model_name} SET {key_value_string} WHERE {pk_name} = {pk_value}'.format(model_name=query.get_model_name(),
                                                                                                     key_value_string=key_value_string,
                                                                                                     pk_name=pk_name,
                                                                                                     pk_value=pk_value)

        print("Query is {}".format(sql_query))

        connection = sqlite3.connect(self.cnx.get_path(), detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
        if cursor.rowcount:
            return self._decode_model(sql_encoded_content, query)
        else:
            raise Exception("Model update failed")

    def filter_models(self, query: Query) -> list:
        pass

    def get_model_definition(self, query: Query) -> list:
        print("In get_model_definition for {}".format(query.get_model_name()))
        sql_query = 'PRAGMA TABLE_INFO({})'.format(query.get_model_name())

        connection = sqlite3.connect(self.cnx.get_path())
        cursor = connection.cursor()
        cursor.execute(sql_query)
        columns_tuples = cursor.fetchall()

        columns = [tup[1] for tup in columns_tuples]
        print("Columns are {}".format(columns))
        return columns

    def retrieve_all(self, query: Query) -> list:
        print("Getting models")
        sql_query = "SELECT * FROM {table};".format(table=query.get_model_name())
        print("Query is {}".format(sql_query))
        print("Path is {}".format(self.cnx.get_path()))

        connection = sqlite3.connect(self.cnx.get_path(), detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute(sql_query)
        models = cursor.fetchall()

        # Models is a list of tuples, so we will convert it into a list of dictionaries
        columns = self.get_model_definition(query)

        list_of_models = []

        for model in models:
            model_dict = {column: model[index] for index, column in enumerate(columns)}
            decoded_dict = self._decode_model(model_dict, query)
            list_of_models.append(decoded_dict)

        print(list_of_models)

        return list_of_models
