from error import Error

class Holders(Error):
    "A class encompassing the players and the middle area"

    def __init__(self):
        self.cards = []

    def number(self, number, to_int = False):
        if to_int:
            if isinstance(number, str):
                if number.isdigit():
                    return int(number)
                else:
                    return False
            else:
                return number
        else:
            if isinstance(number, int):
                return str(number)
            else:
                return number

    def card_value(self, number):
        numbers = ['Ace', 'Jack', 'Queen', 'King']
        more = ['A', 'J', 'Q', 'K']
        if number in numbers:
            i = numbers.index(number)
        elif number in more:
            i = more.index(number)
        else:
            if self.number(number, True) != False:
                number = self.number(number, True)
                return number

        if i == 0:
            value=int(input("Pick the value of your Ace:"))
            if value == 1 or value == 14:
                return value
            else:
                self.error("Incorrect value passed in", self.lineon())
                self.card_value(number)
        return 10+i

    def stack_value(self, card):
        lst = [self.card_value(x.number) for x in card.stack]
        if card.call:
            return max(lst)
        return sum(lst)

    def find_card(self, number, type):
        number = self.number(number)
        pos = -1
        for card in self.cards:
            pos+=1
            if card.number.lower()[0] == number.lower()[0]:
                if card.type.lower()[0] == type.lower()[0]:
                    return [pos, card]

    def check_card(self, number, type):
        if self.find_card(number, type):
            return True
        return False

"""

player = players[0]
player.combine(5, "s", [5, "d"], [3, "d"], [2, "c"], [2, "d"], [3, "h"])

from player import game

cards = [x for x in game.middle.cards if x.call]

for e in cards:
	player.stack_value(e)

"""
