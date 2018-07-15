class Car():
    def __init__(self, colour=None, size=None, speed=None):
        self.colour = colour
        self.size = size
        self.speed = speed

    def serialise(self):
        return {'colour': self.colour,
                'size': self.size,
                'speed': self.speed}


    def deserialise(self, core: dict):
        print("Deserialising {}".format(core))
        self.colour = core['colour']
        self.size = core['size']
        self.speed = core['speed']
