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

    def card_value(self, card, reset = False):
        number  = card.number

        if not card.value or reset:
            numbers = ['Ace', 'Jack', 'Queen', 'King']
            more = ['A', 'J', 'Q', 'K']
            lower = ['a', 'j', 'q', 'k']
            if number in numbers:
                i = numbers.index(number)
            elif number in more:
                i = more.index(number)
            elif number in lower:
                i = lower.index(number)
            elif self.number(number, True) != False:
                    number = self.number(number, True)
                    return number
            else:
                self.error("Incorrect format used", self.lineon())

            if i == 0:
                value=input("Pick the value of your Ace:")
                if value.isdigit():
                    value = int(value)

                    if value == 1 or value == 14:
                        card.value = value
                        return value

                self.error("Incorrect value passed in", self.lineon())
                return self.card_value(card)
            else:
                return 10+i
        else:
            return card.value

    def stack_value(self, card):
        lst = [self.card_value(x) for x in card.stack]
        lst.append(self.card_value(card))
        if card.call:
            return max(lst)
        return sum(lst)

    def find_card(self, number, type):
        number = self.number(number)
        pos = -1
        for card in self.cards:
            pos+=1
            try:
                if card.number.lower()[0] == number.lower()[0]:
                    if card.type.lower()[0] == type.lower()[0]:
                        return [pos, card]
            except AttributeError:
                self.error("Incorrect syntax used", self.lineon())

    def check_card(self, number, type):
        if self.find_card(number, type):
            return True
        return False

    def check_add(self, cards, val):
        result = []
        for upper in cards:
            up_val = self.card_value(upper)
            for lower in cards:
                low_val = self.card_value(lower)
                if up_val + low_val == val and upper is not lower:
                    if upper not in result and lower not in result:
                        result.append(upper)
                        result.append(lower)
        return result
