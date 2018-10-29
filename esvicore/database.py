import os

class Database():
    database_header_definition = '<Database>'
    database_tail_definition = '</Database>'
    models_header_definiton = '<Models>'
    models_tail_definition = '</Models>'
    definition_header_definition = '<Definition>'
    definition_tail_definition = '</Definition>'
    size_header_element = '<Size>'
    size_tail_element = '</Size>'
    index_header_element = '<Index>'
    index_tail_element = '</Index>'
    rows_header_element = '<Rows>'
    rows_tail_element = '</Rows>'

    max_char_for_size = 5 # Length of size can be up to 10^this_var

    type_to_string = {str: 'string',
                      int: 'int',
                      bool: 'bool'}

    string_to_type = {'string': str,
                      'int': int,
                      'bool': bool}

    def __init__(self, path, repair=False):
        self.path = path
        self.repair = repair
        self._validate_db_header()
        self._validate_db_tail()
        self._validate_model_block()
        self._validate_index_block()
        self.cursor = 0

    def _validate_db_header(self):
        print("Validating DB header")
        with open(self.path, 'r') as f:
            header = f.read(len(Database.database_header_definition))
            print(header)
            self.cursor = f.tell()
            print("DB header is valid")

        if not Database.database_header_definition == header:
            raise Exception("Invalid DB header")

    def _validate_db_tail(self):
        with open(self.path, 'r') as f:
            f.seek(0, os.SEEK_END)
            f.seek(f.tell() - len(Database.database_tail_definition), os.SEEK_SET)
            tail = f.read(len(Database.database_tail_definition))
            print(tail)

        if not Database.database_tail_definition == tail:
            raise Exception("Invalid DB tail")

    def _validate_index_block(self):
        print("Validating index header")
        start_of_models = len(Database.database_header_definition) + len(Database.models_header_definiton)
        size_of_models, end_of_size_elem = self.__read_size_elem(start_of_models)
        print("Size of models {}, cursor at end of size elem {}".format(size_of_models, end_of_size_elem))
        start_of_index = end_of_size_elem +int(size_of_models) + len(Database.models_tail_definition)

        with open(self.path, 'r') as f:
            f.seek(start_of_index)
            read_index_header = f.read(len(Database.index_header_element))
            print("Read index header {}".format(read_index_header))
            start_of_size = f.tell()
            size_of_index, end_of_size_elem = self.__read_size_elem(start_of_size)
            print("Size of index is {}".format(size_of_index))

        if not read_index_header == Database.index_header_element:
            raise Exception("Index header invalid, read {} at {}".format(read_index_header,
                                                                         start_of_index))
        with open(self.path, 'r') as f:
            f.seek(int(size_of_index) + end_of_size_elem)
            read_index_tail = f.read(len(Database.index_tail_element))
            end_of_index = f.tell()

        if not read_index_tail == Database.index_tail_element:
            raise Exception("Index tail invalid, read {} at {}".format(read_index_tail,
                                                                       end_of_index))

        print("Index block valid")
        return start_of_index, end_of_size_elem, end_of_index

    def _validate_model_block(self):
        start_of_model_block = len(Database.database_header_definition)

        with open(self.path, 'r') as f:
            f.seek(start_of_model_block)
            read_content_header = f.read(len(Database.models_header_definiton))
            print("Models header is {}".format(read_content_header))
            self.cursor = f.tell()
            print("Models header is valid")

        if not read_content_header == Database.models_header_definiton:
            raise Exception("Models header is invalid {}".format(read_content_header))

        print("Validation model definitions block")
        start_of_models = len(Database.database_header_definition) + len(Database.models_header_definiton)
        size_of_models, end_of_size_elem = self.__read_size_elem(start_of_models)
        print("Size of models {0}".format(size_of_models))

        if not size_of_models:
            raise Exception("Size elem at {} is empty".format(start_of_models))

        with open(self.path, 'r') as f:
            f.seek(end_of_size_elem)
            read_model_block = f.read(int(size_of_models))
            print(read_model_block)
            cursor = f.tell()
            # The cursor is now at the end of the expected model definition block, we will check for the closing elem

            end_of_model_definition = f.read(len(Database.models_tail_definition))
            end_of_model_cursor = f.tell()

        if not end_of_model_definition == Database.models_tail_definition:
            raise Exception("Expected to find {} at {} but found {}".format(Database.models_tail_definition,
                                                                            cursor - len(Database.models_tail_definition),
                                                                            read_model_block[-len(Database.models_tail_definition):]))
        print("Model block is valid")
        return start_of_model_block, end_of_size_elem, end_of_model_cursor

    def __read_size_elem(self, cursor):
        print("Reading the size elem")
        with open(self.path, 'r') as f:
            f.seek(cursor)
            expected_size_elem = f.read(len(Database.size_header_element))
            cursor = f.tell()
            print("Expected size elem {}".format(expected_size_elem))
            print("Cursor at {}".format(cursor))

        if not Database.size_header_element == expected_size_elem:
            raise Exception("{} expected at char {} but found {} instead".format(Database.size_header_element,
                                                                                 cursor,
                                                                                 expected_size_elem))

        buffer = ""
        with open(self.path, 'r') as f:
            f.seek(cursor)
            print("Reading from {}".format(cursor))

            # We will populate a buffer reading each character until we get something which ends with the size_tail_element
            for i in range(len(Database.size_tail_element) + Database.max_char_for_size):
                buffer += f.read(1)
                print(buffer)
                if buffer.endswith(Database.size_tail_element):
                    # Return the size value, and the cursor position
                    return buffer[:-len(Database.size_tail_element)], f.tell()

        raise Exception("No immediate end tag found for size element starting at {}".format(cursor))

    def _get_cursor_to_end(self, cursor):
        with open(self.path, 'r') as f:
            f.seek(cursor)
            here_to_end = f.read()

        return cursor, here_to_end

    def _get_start_to_here(self, cursor):
        with open(self.path, 'r') as f:
            start_to_here = f.read(cursor)

        return start_to_here


    def add_model_definition(self, definition):
        """
        definition = {'model_name': str,
                      'fields': {'age': {'type': int, 'pk': True, 'default': 0},
                                 'name': {'type: str}}}
        """
        model_name = definition.get('model_name')
        fields = definition.get('fields')
        field_strings = []

        for key in fields:
            attributes = fields[key]

            attribute_list = []
            for attribute in attributes:
                if attribute == 'type':
                    value = Database.type_to_string[attributes[attribute]]
                else:
                    value = attributes[attribute]

                attribute_list.append('{}="{}"'.format(attribute, value))

            attributes = ' '.join(attribute_list)
            this_field_string = '<{} {}/>'.format(key, attributes)
            field_strings.append(this_field_string)

        field_string = ''.join(field_strings)

        definition = '{start_name}{start_size}{size}{end_size}{start_definition}{fields}{end_definition}{end_name}'.format(
            start_name='<{}>'.format(model_name),
            start_size=Database.size_header_element,
            size=len(field_string) + len(Database.definition_header_definition) + len(Database.definition_tail_definition),
            end_size=Database.size_tail_element,
            start_definition=Database.definition_header_definition,
            fields=field_string,
            end_definition=Database.definition_tail_definition,
            end_name='</{}>'.format(model_name)
        )

        size_of_definition = len(definition)
        print(definition)

        start_of_models = len(Database.database_header_definition) + len(Database.models_header_definiton)
        size_of_models, end_of_size_elem = self.__read_size_elem(start_of_models)
        new_size = int(size_of_models) + size_of_definition
        new_size_elem = self._create_size_elem(new_size)

        with open(self.path, 'r') as f:
            f.seek(end_of_size_elem)
            existing_models = f.read(int(size_of_models))
            print("Reading models tail as {}".format(f.read(len(Database.models_tail_definition))))
            end_of_models = f.tell()

        print("Writing new definition")
        start_to_beginning_of_size = self._get_start_to_here(start_of_models)

        index_tail_buffer = 'x' * len(Database.index_tail_element)
        index_block = ''

        with open(self.path, 'r') as f:
            f.seek(end_of_models)
            while True:
                char = f.read(1)

                if not char:
                    raise Exception("End of file reached searching for index tail")

                index_tail_buffer = index_tail_buffer[1:] + char
                index_block += char

                if index_tail_buffer == Database.index_tail_element:
                    break

            end_of_index = f.tell()

        # Now we are at the end of the index, and need to add a new row body
        new_row = '<{}>{}0{}</{}>'.format(model_name,
                                          Database.size_header_element,
                                          Database.size_tail_element,
                                          model_name)

        size_of_rows, end_of_size_elem = self.__read_size_elem(end_of_index + len(Database.rows_header_element))
        new_size = int(size_of_rows) + len(new_row)
        new_rows_size_elem = self._create_size_elem(new_size)


        # When reading the rest, we read based on the existing stuff in the db
        _, rest_of_db = self._get_cursor_to_end(end_of_size_elem)

        with open(self.path, 'w+') as f:
            f.write(start_to_beginning_of_size)
            f.write(new_size_elem)
            f.write(definition)
            f.write(existing_models)
            f.write(Database.models_tail_definition)
            f.write(index_block)
            f.write(Database.rows_header_element)
            f.write(new_rows_size_elem)
            f.write(new_row)
            f.write(rest_of_db)
            print("REST OF DB")
            print(rest_of_db)

    def _create_size_elem(self, size):
        size = "{}{}{}".format(Database.size_header_element,
                               str(size),
                               Database.size_tail_element)

        return size

    def get_model_definition(self, model_name):
        if not isinstance(model_name, str):
            raise Exception("Model name expected as str, received {}".format(type(model_name)))

        start_of_models = len(Database.database_header_definition) + len(Database.models_header_definiton)
        size_of_models, end_of_size_elem = self.__read_size_elem(start_of_models)

        this_model_header = '<{}>'.format(model_name)
        this_model_tail = '</{}>'.format(model_name)

        this_model_header_buffer = 'x' * len(this_model_header)
        this_model_tail_buffer = 'x' * len(this_model_tail)

        with open(self.path, 'r') as f:
            while True:
                char = f.read(1)

                if not char:
                    # EOF
                    raise Exception("End of file reached searching for {}".format(model_name))
                    break

                this_model_header_buffer = this_model_header_buffer[1:] + char

                if this_model_header_buffer == this_model_header:
                    print("Model {} found at {}".format(model_name, f.tell() - len(this_model_header)))
                    break

            this_model_size, end_of_size_elem = self.__read_size_elem(f.tell())
            cursor = f.seek(end_of_size_elem)
            definition = self._parse_definition_block(cursor)

        return {'model_name': model_name, 'fields': definition}

    def _find_models_block_in_rows(self):
        pass

    def _parse_definition_block(self, cursor):
        with open(self.path, 'r') as f:
            f.seek(cursor)

            if not f.read(len(Database.definition_header_definition)) == Database.definition_header_definition:
                raise Exception("Definition header expected at {} but not found".format(end_of_size_elem))

            #model_definition = f.read(int(this_model_size))[len(Database.definition_header_definition):-len(Database.definition_tail_definition)]
            #print("Model is {}".format(model_definition))
            end_of_definition_buffer = 'x' * len(Database.definition_tail_definition)

            parsing_field_name, parsing_attribute_name, parsing_attribute_value = False, False, False
            this_field_name, this_attribute_name, this_attribute_value = '', '', ''
            fields = {}

            print("Beginning definition parsing")
            while True:
                char = f.read(1)

                if not char:
                    # EOF
                    raise Exception("End of file reached searching for {}".format(model_name))
                    break

                end_of_definition_buffer = end_of_definition_buffer[1:] + char

                if end_of_definition_buffer == Database.definition_tail_definition:
                    print("End of definition reached")
                    break

                if char == '<':
                    # Start parsing the name
                    #print("Start parsing field name")
                    parsing_field_name = True
                elif char == '>':
                    # Refresh the values because we have reached the end of this field
                    #print("Reached end of field")
                    this_field_name = ''
                elif parsing_field_name and char == ' ':
                    # Reached the end of the field name, so we'll start parsing the attributes
                    #print("Creating field name")
                    parsing_field_name = False
                    fields[this_field_name] = {}
                    parsing_attribute_name = True
                elif parsing_field_name:
                    this_field_name += char
                    #print("Field name is {}".format(this_field_name))
                elif parsing_attribute_name and char == '=':
                    # Reached the separator
                    #print("End of attribute {}".format(this_attribute_name))
                    parsing_attribute_name = False
                    parsing_attribute_value = True
                elif parsing_attribute_name:
                    this_attribute_name += char
                elif parsing_attribute_value and char == ' ':
                    # Reached end of this attribute, but not the end of all attributes
                    fields[this_field_name][this_attribute_name] = self._render_attribute_pair(this_attribute_name, this_attribute_value)
                    parsing_attribute_name, parsing_attribute_value = True, False
                    this_attribute_name, this_attribute_value = '', ''
                elif parsing_attribute_value and char == '/':
                    # Reached end of this attribute, and all attributes for this field
                    fields[this_field_name][this_attribute_name] = self._render_attribute_pair(this_attribute_name, this_attribute_value)
                    parsing_field_name, parsing_attribute_name, parsing_attribute_value = False, False, False
                    this_field_name, this_attribute_name, this_attribute_value = '', '', ''
                elif parsing_attribute_value:
                    this_attribute_value += char
                else:
                    pass

        return fields

    def _render_attribute_pair(self, key, value):
        """
        For a key and value read from the definition, convert them into the correct formats
        """
        value = value.strip('"')

        if key == 'pk':
            value = value in ['True', 'true']
        elif key == 'type':
            value = Database.string_to_type[value]
        else:
            pass

        return value

    def remove_model_definition(self, model_name):
        # This will remove any associated models instances too
        pass

    def insert_model(self, model_name, model_instance):
        model_definition = self.get_model_definition(model_name)
        model_instance = self._check_model_fits_definition(model_definition, model_instance)

        # TODO Find start of this model block
        # TODO Insert
        pass

    def update_model(self, model):
        pass

    def remove_model(self, model_pk):
        pass

    def _check_model_fits_definition(self, model_definition, model_instance):
        # Raise an exception if the model doesn't fit the definition, fill any default values otherwise
        # TODO If no one else has touched the db, use the definitions retrieved on init
        for key, definition in model_definition.get('fields').items():
            if key not in model_instance and 'default' not in definition:
                raise Exception("Model {} requires {} which has no default value".format(
                    model_definition['model_name'],
                    key
                    ))
            elif key not in model_instance:
                model_instance[key] = definition['default']
            else:
                if not isinstance(model_instance[key], definition['type']):
                    raise Exception("Key {} for model {} expected to be type {} not {}".format(
                        key,
                        model_definition['model_name'],
                        definition['type'],
                        type(model_instance[key])
                        ))


    @classmethod
    def initialise_empty_db(cls, path):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "empty.esvi"), 'r') as f:
            database_string = f.read()

        with open(path, 'w') as f:
            f.write(database_string)

        return cls(path=path)
