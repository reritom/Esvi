class EsviModel():

    def __init__(self):
        print("In init")
        print(dir(self.__class__))

        # Initialise the model name
        self.name = getattr(self.__class, 'name')

        

        # Here we grab all the child attributes
        for value in dir(self.__class__):
            if not value.startswith('_'):
                print(value)
                print(getattr(self.__class__, value))
