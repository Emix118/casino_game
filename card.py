class Card():
    """A class to create cards with a number and type"""

    def __init__(self, number, type):
        self.number = number
        self.type = type
        self.stack = []
        self.call = False
