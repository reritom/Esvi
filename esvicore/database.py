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

    max_char_for_size = 5 # Length of size can be up to 10^this_var

    type_to_string = {str: 'string',
                      int: 'int',
                      bool: 'bool'}

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

    def get_model_definitions(self):
        print("Getting model definitions")
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

        if not end_of_model_definition == Database.models_tail_definition:
            if not self.repair:
                raise Exception("Expected to find {} at {} but found {}".format(Database.models_tail_definition,
                                                                            cursor - len(Database.models_tail_definition),
                                                                            read_model_block[-len(Database.models_tail_definition):]))

            else:
                # Lets try and repair it by searching for the end tag and recalculating the size
                new_size = 0
                buffer = 'x' * len(Database.models_tail_definition)
                with open(self.path, 'r') as f:
                    f.seek(start_of_models)

                    while True:
                        char = f.read(1)

                        if not char:
                            # EOF
                            raise Exception("End of file reached searching for {} in repair attempt".format(Database.models_tail_definition))
                            break

                        new_size += 1
                        buffer = buffer[1:] + char

                        if buffer == Database.models_tail_definition:
                            # The closing elem has been found
                            print("Tail definition has been found ending at {} with size {}".format(f.tell(), new_size))
                            break

                # From here will we pass the block beginning, and new block size to the size updater
                self.__update_size_elem(start_of_models, new_size)


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

    def __update_size_elem(self, cursor, block_size):
        """
        For a ..
        """
        print("Updating size elem at {}".format(cursor))
        current_size, _ = self.__read_size_elem(cursor)
        print("Current size elem is {}".format(current_size))
        block_size_before_b = '%d' % block_size
        print("New blocksize is {}".format(block_size_before_b))

        new_size_length_difference = len(current_size) - len(block_size_before_b)
        block_size_after_b = '%d' % (block_size + new_size_length_difference)
        print("Adjusted blocksize is {}".format(block_size_after_b))

        with open(self.path, 'r') as f:
            f.seek(cursor)
            print(f.read(len(Database.size_header_element)))
            cursor_at_end_of_size_header = f.tell()
            # The cursor is now at the end of <size>

        _, here_to_end = self._get_cursor_to_end(cursor_at_end_of_size_header)
        print(here_to_end)
        updated_here_to_end = block_size_after_b + here_to_end[len(block_size_after_b):]

        print("Updated")
        print(updated_here_to_end)

        with open(self.path, 'r+') as f:
            f.seek(cursor)
            f.read(len(Database.size_header_element))
            f.write(updated_here_to_end)

        with open(self.path, 'r') as f:
            f.seek(cursor)
            print(f.read())

        print

        pass

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
                                 'name': {'type: str}}
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

        print("Writing new definition")
        start_to_beginning_of_size = self._get_start_to_here(start_of_models)
        _, rest_of_db = self._get_cursor_to_end(end_of_size_elem)

        with open(self.path, 'w+') as f:
            f.write(start_to_beginning_of_size)
            f.write(new_size_elem)
            f.write(definition)
            f.write(rest_of_db)

    def _create_size_elem(self, size):
        size = "{}{}{}".format(Database.size_header_element,
                               str(size),
                               Database.size_tail_element)

        return size

    def get_model_definition(self, model_name):
        pass

    def remove_model_definition(self, model_name):
        pass

    def insert_model(self, model):
        pass

    def remove_model(self, model_pk):
        pass

    def _check_model_fits_definition(self):
        pass

    @classmethod
    def initialise_empty_db(cls, path):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "empty.esvi"), 'r') as f:
            database_string = f.read()

        with open(path, 'w') as f:
            f.write(database_string)

        return cls(path=path)
