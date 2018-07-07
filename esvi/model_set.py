class ModelSet():
    """
    This is an iterator for a list of Model Instances, with some additional bulk methods
    """
    def __init__(self, models):
        self.models = models
        self.iteration_index = 0

    def exists(self):
        return True if self.models else False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            model = self.models[self.iteration_index]
        except IndexError:
            raise StopIteration

        self.iteration_index += 1
        return model
