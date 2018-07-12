import os

class Database():
    database_header_definition = b'<Database>'
    database_tail_definition = b'</Database>'
    models_header_definiton = b'<Models>'
    models_tail_definition = b'</Models>'
    size_header_element = b'<Size>'
    size_tail_element = b'</Size>'

    max_char_for_size = 5 # Length of size can be up to 10^this_var

    def __init__(self, path):
        self.path = path
        self.repair = True
        self._validate_db_header()
        self._validate_db_tail()
        self._validate_models_header()
        self.get_model_definitions()
        self.cursor = 0

    def _validate_db_header(self):
        with open(self.path, 'rb') as f:
            header = f.read(len(Database.database_header_definition))
            print(header)
            self.cursor = f.tell()

        if not Database.database_header_definition == header:
            raise Exception("Invalid DB header")

    def _validate_models_header(self):
        cursor = len(Database.database_header_definition)
        with open(self.path, 'rb') as f:
            f.seek(cursor)
            content_header = f.read(len(Database.models_header_definiton))
            print(content_header)
            self.cursor = f.tell()

    def _validate_models_tail(self):
        pass



    def _validate_db_tail(self):
        with open(self.path, 'rb') as f:
            f.seek(-len(Database.database_tail_definition), os.SEEK_END) # Offset from file, and start at end of file
            tail = f.read(len(Database.database_tail_definition))
            print(tail)

        if not Database.database_tail_definition == tail:
            raise Exception("Invalid DB tail")

    def insert_model_definition(self, definition):
        pass

    def get_model_definitions(self):
        start_of_models = len(Database.database_header_definition) + len(Database.models_header_definiton)
        size_of_models, _ = self.__read_size_elem(start_of_models)
        print(size_of_models)

        with open(self.path, 'rb') as f:
            f.seek(start_of_models)
            expected_model_block = f.read(int(size_of_models))
            print(expected_model_block)
            cursor = f.tell()
            # The cursor is now at the end of the expected model definition block, we will check for the closing elem

        if not expected_model_block[-len(Database.models_tail_definition):] == Database.models_tail_definition:
            if not self.repair:
                raise Exception("Expected to find {} at {} but found {}".format(Database.models_tail_definition,
                                                                            cursor - len(Database.models_tail_definition),
                                                                            expected_model_block[-len(Database.models_tail_definition):]))

            else:
                # Lets try and repair it by searching for the end tag and recalculating the size
                new_size = 0
                buffer = b'x' * len(Database.models_tail_definition)
                with open(self.path, 'rb') as f:
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
        with open(self.path, 'rb') as f:
            f.seek(cursor)
            expected_size_elem = f.read(len(Database.size_header_element))
            cursor = f.tell()
            print("Expected size elem {}".format(expected_size_elem))
            print("Cursor at {}".format(cursor))

        if not Database.size_header_element == expected_size_elem:
            raise Exception("{} expected at char {} but found {} instead".format(Database.size_header_element,
                                                                                 start_of_models,
                                                                                 expected_size_elem))

        buffer = b""
        with open(self.path, 'rb') as f:
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
        block_size_before_b = b'%d' % block_size
        print("New blocksize is {}".format(block_size_before_b))

        new_size_length_difference = len(current_size) - len(block_size_before_b)
        block_size_after_b = b'%d' % (block_size + new_size_length_difference)
        print("Adjusted blocksize is {}".format(block_size_after_b))

        with open(self.path, 'rb') as f:
            f.seek(cursor)
            print(f.read(len(Database.size_header_element)))
            cursor_at_end_of_size_header = f.tell()
            # The cursor is now at the end of <size>

        _, here_to_end = self._get_cursor_to_end(cursor_at_end_of_size_header)
        print(here_to_end)
        updated_here_to_end = block_size_after_b + here_to_end[len(block_size_after_b):]

        print("Updated")
        print(updated_here_to_end)

        with open(self.path, 'rb+') as f:
            f.seek(cursor)
            f.read(len(Database.size_header_element))
            f.write(updated_here_to_end)

        with open(self.path, 'rb') as f:
            f.seek(cursor)
            print(f.read())

        print

        pass

    def _get_cursor_to_end(self, cursor):
        with open(self.path, 'rb') as f:
            f.seek(cursor)
            here_to_end = f.read()

        return cursor, here_to_end



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
