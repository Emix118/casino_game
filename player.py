from holders import Holders
from debug import print_cards, cards_by_object, check_turn

import itertools

class Player(Holders):
    "A class for the players"

    def __init__(self, name):
        Holders.__init__(self)
        self.name = name
        self.cards_taken = []
        self.points = 0
        self.isturn = False
        self.took_last = False

    def update_points(self):

        for card in self.cards_taken:
            if card.number == "10":
                if card.type == 'Diamonds':
                    self.points+=2
            if card.number == "2":
                if card.type == 'Spades':
                    self.points+=1
            if card.number == 'Ace':
                self.points+=1

        if game.most_spades()[1] == self:
            self.points+=1

        if game.most_cards()[1] == self:
            self.points+=3

    def take(self, your_number, your_type, *args):
        # Number and type of your card followed by the cards
        # to add and take (accept single cards)

        # Assumes the following format for args:
        # [Card number, Card type], [...], ...
        if self.isturn:
            if self.check_card(your_number, your_type):

                myCard = self.find_card(your_number, your_type)[1]

                val = self.card_value(myCard, True)

                found = []
                if not args:
                    self.error("No cards to take were passed in",
                        self.lineon())
                    return
                for card in args:
                    # try:
                    if game.middle.check_card(card[0], card[1]):

                        mid = game.middle.find_card(card[0], card[1])[1]
                        found.append(mid)
                    else:
                        self.error("One or more of those" +
" cards were not found in the middle area", self.lineon())
                        return
                    # except:
                    #     self.error("Format error", self.lineon())
                    #     return

                # Check if any card or stack values are equal to your card
                if any([True if self.stack_value(x) == val
                    or self.card_value(x) == val else False for x in found]):

                    of_value = []

                    of_value.extend(self.check_add([x for x in found
                                if not x in of_value and not x.stack], val))

                    for e in [x for x in found
                        if self.stack_value(x) == val]:

                        for s in e.stack:
                            if s not in of_value:
                                of_value.append(s)
                        if e not in of_value:
                            of_value.append(e)

                    if all(True if e in of_value else False for e in found):
                        self.take_success(your_number, your_type, of_value)
                    else:
                        self.error("Not all those cards are able to be taken",
                        self.lineon())
                else:
                    # Added cardLst to be able to add the stacked
                    # cards since tuples are not mutable
                    cardLst = []

                    total = 0
                    stacked = []

                    for mid in found:
                        try:
                            if mid.call:
                                if all([x.call for x in found]):
                                    total = self.stack_value(mid)
                                    for e in mid.stack:
                                        cardLst.append(e)
                                    cardLst.append(mid)
                                    break
                            elif mid.stack:
                                if mid not in stacked:
                                    stacked.append(mid)

                                    for e in mid.stack:
                                        if e not in stacked:
                                            stacked.append(e)

                                    total+=self.card_value(mid)

                                    total+=self.stack_value(mid)

                                    cardLst.append(mid)
                                    for e in mid.stack:
                                        cardLst.append(e)
                            else:
                                total+=self.card_value(mid)

                                cardLst.append(mid)
                        except TypeError:
                            self.error("There was an error..." +
                            "Are you sure you used the correct" +
                            " syntax?", self.lineon())
                            return

                    if self.card_value(myCard) == total:
                        self.take_success(your_number, your_type, cardLst)
                    else:
                        self.error("Those cards don't add up" +
                            " to your card", self.lineon())
            else:
                self.error("You do not have that card", self.lineon())
        else:
            self.error("Not your turn", self.lineon())

    def take_success(self, your_number, your_type, cardLst):
            for card in cardLst:
                self.to_taken(card.number, card.type)
            self.to_taken(your_number, your_type, True)

            game.took(self)

            game.next_turn()

            ##
            cards_by_object(players, game.middle)
            check_turn(players)

    def trail(self, number, type):
        # Place a card in middle without taking or stacking
        if self.isturn:
            if self.check_card(number, type):
                pos = self.find_card(number, type)[0]
                game.middle.cards.append(self.cards.pop(pos))
            else:
                self.error("You don't have that card", self.lineon())
                return

            game.next_turn()

            ##
            cards_by_object(players, game.middle)
            check_turn(players)

        else:
            self.error("Not your turn", self.lineon())

    def stack(self, your_number, your_type, *args):
        # Stack a card on top of another adding their values
        if self.isturn:
            if self.check_card(your_number, your_type):

                found = []
                for card in args:
                    try:
                        if game.middle.check_card(card[0], card[1]):

                            found.append(game.middle.find_card(
                                                card[0], card[1])[1])
                        else:
                            self.error("One or more of those cards"+
                            "were not found in the middle", self.lineon())
                            return
                    except:
                        self.error("There was an error..." +
                        "Are you sure you used the correct" +
                        " syntax?", self.lineon())
                        return

                pos, myCard = self.find_card(your_number, your_type)

                val = self.card_value(myCard, True)

                for midCard in found:
                    if midCard.call:
                        self.error("You cannot stack a build combination"+
                        "on top of a call combination", self.lineon())
                        return
                    val+=self.stack_value(midCard)

                for c in self.cards:
                    if c is not myCard:
                        if self.card_value(c, True) == val:

                            for midCard in found:
                                if midCard.stack:
                                    for e in midCard.stack:
                                        e.stack.append(myCard)
                                        myCard.stack.append(e)
                                myCard.stack.append(midCard)
                                midCard.stack.append(myCard)

                                for e in found:
                                    if not e in midCard.stack and e != midCard:
                                        midCard.stack.append(e)

                            game.middle.cards.append(
                                    self.cards.pop(pos))

                            game.next_turn()

                            ##
                            cards_by_object(players, game.middle)
                            check_turn(players)

                            return

                self.error("You don't have a card to" +
                " later collect this stack", self.lineon())
            else:
                self.error("Your card was not found", self.lineon())
        else:
            self.error("Not your turn", self.lineon())

    def combine(self, your_number, your_type, *args):
        # Stack a card on top of another but keep the original value
        if self.isturn:
            if self.check_card(your_number, your_type):

                pos, myCard = self.find_card(your_number, your_type)

                found = []
                for card in args:
                    try:
                        if game.middle.check_card(card[0], card[1]):

                            found.append(game.middle.find_card(
                                                card[0], card[1])[1])
                        else:
                            self.error("One or more of those cards"+
                            "were not found in the middle", self.lineon())
                            return
                    except:
                        self.error("There was an error..." +
                        "Are you sure you used the correct" +
                        " syntax?", self.lineon())
                        return

                found.append(myCard)
                val = max([self.card_value(c, True) for c in found])

                # Removing myCard so that it doesn't interfere
                # with the code below
                found.pop(found.index(myCard))

                of_value = [c for c in found if self.card_value(c) == val]

                for card in found:
                    if self.stack_value(card) == val:
                        if card not in of_value:
                            of_value.append(card)
                        of_value.extend(card.stack)

                # Create a list with all possible combinations of the cards
                combs = []
                for i in range(1, len(found)+1):
                    res = [list(x) for x in itertools.combinations(found, i)]
                    combs.extend(res)

                # Iterate through that list and check if any of the
                # combinations equal the value of you card
                for upper in combs:
                    total = 0
                    for lower in upper:
                        if not lower in of_value:
                            if lower.stack:
                                total+=self.stack_value(lower)
                            else:
                                total+=self.card_value(lower)
                            if total == val:
                                if lower.stack:
                                    of_value.extend(lower.stack)
                                of_value.extend(upper)

                if of_value:
                    if len(of_value) >= len(found):
                        for c in self.cards:
                            valHand = self.card_value(c)
                            if valHand == val and c != myCard:

                                for card in of_value:
                                    for e in of_value:
                                        if not e in card.stack and e != card:
                                            card.stack.append(e)

                                    myCard.stack.append(card)
                                    myCard.call = True
                                    card.stack.append(myCard)
                                    card.call = True

                                game.middle.cards.append(
                                      self.cards.pop(pos))

                                game.next_turn()

                                ##
                                cards_by_object(players, game.middle)
                                check_turn(players)

                                return

                        self.error("You dont have an extra"+
                        " card to later collect this", self.lineon())
                    else:
                        self.error("Some of the cards did not add up to" +
                        " your card", self.lineon())
                else:
                    self.error("None of those cards match your card",
                     self.lineon())
            else:
                self.error("You do not have that card", self.lineon())
        else:
            self.error("Not your turn", self.lineon())



    def to_taken(self, number, type, to_self = False):
        if to_self:
            try:
                pos = self.find_card(number, type)[0]
                self.cards_taken.append(self.cards.pop(pos))
                return
            except:
                self.error("Your card was not found", self.lineon())
                return
        try:
            pos = game.middle.find_card(number, type)[0]
            self.cards_taken.append(game.middle.cards.pop(pos))
        except:
            self.error("Card not found", self.lineon())

from game import Game, players
game = Game()
# players = game.players

###############################################################

    # player1 = Player("Player 1")
    # player2 = Player("Player 2")
    # player3 = Player("Player 3")
    # player4 = Player("Player 4")

# from card import Card
#
# player1.cards = [
# Card("10", "Clovers"),
# Card("4", "Hearts"),
# ]
#
# game.middle.cards = [
# Card("6", "Clovers")
# ]
#
# player2.cards = [
# # Card("Ace", "Diamonds"),
# Card("10", "Hearts")
# ]

##
# cards_by_object(players, game.middle)
#
# check_turn(players)
