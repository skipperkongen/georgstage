class Model(object):
    """docstring for Model."""

    def __init__(self):
        super(Model, self).__init__()
        self.value = 0

    def incr(self):
        print('Calculating increment')
        self.value += 1
        return self.value
