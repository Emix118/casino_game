import random
import sys
import inspect

class Error():
    def error(self, message, line, stop = False):
        print('ERROR: ' + message, line)
        if stop:
            sys.exit()

    def lineon(self):
        # Determines the current line in the program
        return inspect.currentframe().f_back.f_lineno

class Card():
    """A class to create cards with a number and type"""

    def __init__(self, number, type):
        self.number = number
        self.type = type
        self.stack = []
        self.call = False

class Game(Error):
    """A class to manage the essentials of the game"""

    types = ['Diamonds', 'Spades', 'Clovers', 'Hearts']
    numbers = ['Ace', 'Jack', 'Queen', 'King']

    def __init__(self, players):
        if len(players) > 4:
            self.error("Too many players", self.lineon(), True)

        self.players = players

        self.deck = []
        self.middle = Middle()

        self.set_players_game()
        self.players[0].isturn = True
        self.turn = 0

        self.build_deck()
        self.deal_cards()
        self.deal_middle()

    def set_players_game(self):
        # Allowing all players to access paramaters
        # from the game class without the need to inherit
        for player in self.players:
            player.game = self

    def build_deck(self):
        # Create a standard 52-card deck using the Card class
        # and shuffle it

        # Adding the numbers to numbers array
        for n in range(2,11):
            self.numbers.insert(n, str(n))

        for t in self.types:
            for n in self.numbers:
                self.deck.append(Card(n, t))
        random.shuffle(self.deck)

    def deal_cards(self):
        # Dealing the cards in a 2-2 format to the
        # players and middle area

        # NOTE: Since the computer is dealing the cards
        # there is no need to have a dealer

        # Dealing two cards to each player twice
        for i in range(0, 2):
            for player in self.players:
                for i in range(0, 2):
                    player.cards.append(self.deck.pop())

    def deal_middle(self):
            # Placing 4 cards in middle

            # Separte from deal cards because no cards
            # are placed in the middle after each round
            for i in range(0, 4):
                self.middle.cards.append(self.deck.pop())

    def next_turn(self):
        self.players[self.turn].isturn = False

        if len(self.players) - 1 < self.turn + 1:
            self.turn = 0
            self.players[self.turn].isturn = True
        else:
            # self.turn+=1
            self.players[self.turn].isturn = True

    def most_cards(self):
        current_lead = [0, None]
        for player in self.players:
            if len(player.cards_taken) >= current_lead[0]:
                if len(player.cards_taken) == current_lead[0]:
                    amount = len(player.cards_taken)
                    current_lead = [amount, None]
                else:
                    amount = len(player.cards_taken)
                    current_lead = [amount, player]
        return current_lead

    def most_spades(self):
        current_lead = [0, None]
        for player in self.players:
            spades = 0
            for card in player.cards_taken:
                if card.type == 'Spades':
                    spades+=1
            if spades >= current_lead[0]:
                if spades == current_lead[0]:
                    current_lead = [spades, None]
                else:
                    current_lead = [spades, player]
        return current_lead


    def check_points():
        for player in self.players:
            if player.points >= 21:
                self.end_game()
            else:
                self.next_round()

    def end_game(self):
        pass

    def next_round():
        pass

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

class Middle(Holders):
    "A class for the middle area"

class Player(Holders):
    "A class for the players"

    def __init__(self, name):
        Holders.__init__(self)
        self.name = name
        self.cards_taken = []
        self.points = 0
        self.isturn = False

        # For access to the current game's list
        # of players to compare
        self.game = None

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

        if self.game.most_spades()[1] == self:
            self.points+=1

        if self.game.most_cards()[1] == self:
            self.points+=3

    def take(self, your_number, your_type, *args):
        # Number and type of your card followed by the cards
        # to add and take (accept single cards)

        # Assumes the following format for args:
        # [Card number, Card type], [...], ...
        if self.isturn:
            if self.check_card(your_number, your_type):

                found = []
                for card in args:
                    if self.game.middle.check_card(card[0], card[1]):

                        mid = self.game.middle.find_card(
                                    card[0], card[1])[1]
                        found.append(mid)
                    else:
                        self.error("One or more of those" +
" cards were not found in the middle area", self.lineon())
                        return

                # Added cardLst to be able to add the stacked
                # cards since tuples are not mutable
                cardLst = []

                total = 0
                stacked = []

                for mid in found:
                    try:
                        if mid.stack and mid.call:
                            if [x.call for x in found if x.call]:
                                total = self.card_value(mid.number)
                                for e in mid.stack:
                                    cardLst.append(e)
                                cardLst.append(mid)
                                break
                        elif mid.stack:
                            if mid not in stacked:
                                stacked.append(mid)
                                stacked.append(mid.stack)

                                total+=self.card_value(mid.number)

                                for e in mid.stack:
                                    total+=self.card_value(e.number)

                                cardLst.append(mid)
                                for e in mid.stack:
                                    cardLst.append(e)
                        else:
                            ph = self.game.middle.find_card(
                                            card[0], card[1])[1]
                            total+=self.card_value(ph.number)

                            cardLst.append(mid)
                    except TypeError:
                        self.error("There was an error..." +
                        "Are you sure you used the correct" +
                        " syntax?", self.lineon())
                        return

                if self.card_value(your_number) == total:
                    for card in cardLst:
                        self.to_taken(card.number, card.type)
                    self.to_taken(your_number, your_type, True)

                    self.game.next_turn()

                    ##
                    cards_by_object([player1, game.middle, player2])

                    check_turn(game)

                else:
                    self.error("Those cards don't add up" +
                        " to your card", self.lineon())
            else:
                self.error("You do not have that card", self.lineon())
        else:
            self.error("Not your turn", self.lineon())


    def trail(self, number, type):
        # Place a card in middle without taking or stacking
        if self.isturn:
            if self.check_card(number, type):
                pos = self.find_card(number, type)[0]
                self.game.middle.cards.append(self.cards.pop(pos))
            else:
                self.error("You don't have that card", self.lineon())
                return

            self.game.next_turn()

            ##
            cards_by_object([player1, game.middle, player2])
            check_turn(game)
        else:
            self.error("Not your turn", self.lineon())

    def stack(self, your_number, your_type, number, type):
        # Stack a card on top of another
        if self.isturn:
            if self.check_card(your_number, your_type):
                if self.game.middle.check_card(number, type):

                    pos, myCard = self.find_card(your_number, your_type)

                    midCard = self.game.middle.find_card(
                                                number, type)[1]

                    val = self.card_value(myCard.number)

                    if midCard.stack:
                        for n in midCard.stack:
                            val+=self.card_value(n.number)
                    val+=self.card_value(midCard.number)

                    for card in self.cards:
                        if self.card_value(card.number) == val:

                            for e in midCard.stack:
                                e.stack.append(myCard)
                                myCard.stack.append(e)

                            myCard.stack.append(midCard)
                            midCard.stack.append(myCard)

                            self.game.middle.cards.append(
                                    self.cards.pop(pos))

                            self.game.next_turn()

                            ##
                            cards_by_object([player1,
                                            game.middle, player2])
                            check_turn(game)

                            return
                    self.error("You don't have a card to" +
                    " later collect this stack", self.lineon())
                else:
                    self.error("That card was not found"+
                    " in the middle", self.lineon())
            else:
                self.error("Your card was not found", self.lineon())
        else:
            self.error("Not your turn", self.lineon())

    def combine(self, your_number, your_type, number, type):
        # Stack two cards of same value and keep that value
        if self.isturn:
            if self.check_card(your_number, your_type):
                if self.game.middle.check_card(number, type):

                    pos, myCard = self.find_card(your_number, your_type)

                    midCard = self.game.middle.find_card(
                                            number, type)[1]

                    myval = self.card_value(myCard.number)
                    midval= self.card_value(midCard.number)

                    if myval == midval:
                        for card in self.cards:
                            val = self.card_value(card.number)
                            if val == myval and card != myCard:

                                for e in midCard.stack:
                                    e.stack.append(myCard)
                                    myCard.stack.append(e)
                                    e.call = True

                                myCard.stack.append(midCard)
                                myCard.call = True
                                midCard.stack.append(myCard)
                                midCard.call = True

                                self.game.middle.cards.append(
                                      self.cards.pop(pos))

                                self.game.next_turn()

                                ##
                                cards_by_object([player1,
                                        game.middle, player2])
                                check_turn(game)

                                return

                        self.error("You dont have an extra"+
                        " card to later collect this", self.lineon())
                    else:
                        self.error("Those cards don't have" +
                        " the same value", self.lineon())
                else:
                    self.error("That card was not found"+
                    " in the middle", self.lineon())
            else:
                self.error("Your card was not found", self.lineon())
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
            pos = self.game.middle.find_card(number, type)[0]
            self.cards_taken.append(self.game.middle.cards.pop(pos))
        except:
            self.error("Card not found", self.lineon())

###############################################################
"""Since its based on console, these functions are mostly used
for displaying useful information"""

# DEBUG: function to print out each card's number and type
def print_cards(object):
    stacked = []
    for card in object.cards:
        if card.stack:
            if not card in stacked:

                print("{",card.number,"of",card.type)

                for e in card.stack:
                    stacked.append(e)
                    print(e.number,"of",e.type,"}")
        else:
            print(card.number, "of", card.type)

# DEBUG: function to print out the cards of a list of objects
# in an organized fashion
def cards_by_object(objects):
    for o in objects:
        if isinstance(o, Player):
            print("--------------" + o.name)
        else:
            print("--------------Middle")
        print_cards(o)
    print("--------------")

# DEBUG: function to print out who's turn it is
def check_turn(game):
    for player in game.players:
        if player.isturn == True:
            print("It is " + player.name + "'s turn")
            return
    Error.error(None, "Weird, it is no one's turn",
                self.lineon())


    # player1 = Player("Player 1")
    # player2 = Player("Player 2")
    # player3 = Player("Player 3")
    # player4 = Player("Player 4")
    #
    # game = Game([player1, player2, player3, player4])
    #
    # cards_by_object([player1, player2,
    #                 game.middle, player3,
    #                 player4])
    #


player1 = Player("Player 1")
player2 = Player("Player 2")

game = Game([player1, player2])

player1.cards = [
Card("5", "Diamonds"),
Card("2", "Spades"),
Card("Jack", "Hearts"),
Card("5", "Clovers")
]

game.middle.cards = [
Card("2", "Diamonds"),
Card("9", "Clovers"),
Card("Ace", "Spades"),
Card("5", "Hearts")
]

cards_by_object([player1, game.middle, player2])

check_turn(game)
