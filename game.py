from card import Card
from error import Error
from holders import Holders
from player import players

import random

class Game(Error):
    """A class to manage the essentials of the game"""

    types = ['Diamonds', 'Spades', 'Clovers', 'Hearts']
    numbers = ['Ace', 'Jack', 'Queen', 'King']

    def __init__(self):
        if len(players) > 4:
            self.error("Too many players", self.lineon(), True)

        self.deck = []
        self.middle = Holders()

        if players:
            players[0].isturn = True
        self.turn = 0

        self.build_deck()
        self.deal_cards()
        self.deal_middle()

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
            for player in players:
                for i in range(0, 2):
                    player.cards.append(self.deck.pop())

    def deal_middle(self):
            # Placing 4 cards in middle

            # Separte from deal cards because no cards
            # are placed in the middle after each round
            for i in range(0, 4):
                self.middle.cards.append(self.deck.pop())

    def next_turn(self):
        players[self.turn].isturn = False

        if len(players) - 1 < self.turn + 1:
            self.turn = 0
            players[self.turn].isturn = True
        else:
            self.turn+=1
            players[self.turn].isturn = True

    def most_cards(self):
        current_lead = [0, None]
        for player in players:
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
        for player in players:
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
        for player in players:
            if player.points >= 21:
                self.end_game()
            else:
                self.next_round()

    def end_game(self):
        pass

    def next_round():
        pass
