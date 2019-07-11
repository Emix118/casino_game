import random
import sys

class Error():
    def error(self, message, stop = False):
        print('ERROR: ' + message)
        if stop:
            sys.exit()

class Card():
    """A class to create cards with a number and type"""

    def __init__(self, number, type):
        self.number = number
        self.type = type

class Game(Error):
    """A class to manage the essentials of the game"""

    types = ['Diamonds', 'Spades', 'Clovers', 'Hearts']
    numbers = ['Ace', 'Jack', 'Queen', 'King']

    def __init__(self, players):
        if len(players) > 4:
            self.error("Too many players", True)

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

        if len(self.players) < self.turn + 1:
            self.turn = 0
            self.players[self.turn].isturn = True
        else:
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

class Holders():
    "A class encompassing the players and the middle area"

    def __init__(self):
        self.cards = []

class Middle(Holders):
    "A class for the middle area"

    def find_card(self, number, type):
        pos = -1
        for card in self.cards:
            pos+=1
            if card.number == number:
                if card.type == type:
                    return [pos, card]


class Player(Holders, Error):
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

    def take(self, number, type):
        if self.isturn:
            if isinstance(number, int):
                number = str(number)
            pos = self.game.middle.find_card(number, type)
            if pos:
                pos = self.game.middle.find_card(number, type)[0]
                self.cards_taken.append(game.middle.cards.pop(pos))
                self.game.next_turn()
            else:
                self.error("Card not found")

            ##
            cards_by_object([player1, game.middle, player2])



###############################################################

# DEBUG: function to print out each card's number and type
def print_cards(object):
    for card in object.cards:
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
    Error.error(None, "Weird, it is no one's turn")

# DEBUG: Convinient way to initialize a game with 4 players
def init4p():
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    player3 = Player("Player 3")
    player4 = Player("Player 4")

    game = Game([player1, player2, player3, player4])

    cards_by_object([player1, player2,
                    game.middle, player3,
                    player4])

    check_turn(game)

# DEBUG: Convinient way to initialize a game with two players
def init2p():
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    game = Game([player1, player2])

    cards_by_object([player1, game.middle, player2])

    check_turn(game)

    # player1.cards_taken = [Card("Ace", "Clovers")]
    # player2.cards_taken = [Card("Ace", "Spades")]
    # # player3.cards_taken = [1,2,3]
    # # player4.cards_taken = [1,2,3,4,5,6]
    #
    # for player in game.players:
    #     player.update_points()
    #     print(player.points, player.name)

# init2p()

player1 = Player("Player 1")
player2 = Player("Player 2")

game = Game([player1, player2])

cards_by_object([player1, game.middle, player2])

check_turn(game)
