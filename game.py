from card import Card
from error import Error
from holders import Holders
from player import Player
from scene import game, players

from debug import (display_points, display_winner,
        print_cards, cards_by_object, check_turn)

import random
import sys

class Game(Error):
    """A class to manage the essentials of the game"""

    types = ['Diamonds', 'Spades', 'Clovers', 'Hearts']
    numbers = ['Ace', 'Jack', 'Queen', 'King']

    def __init__(self):

        going = True
        while going:
            amount = input("How many players? (2-4) ")
            if amount.isdigit():
                amount = int(amount)

                if amount in range(2, 5):
                    going = False
                else:
                    self.error("Incorrect value for amount of players",
                        self.lineon())
            else:
                self.error("Incorrect value for amount of players",
                    self.lineon())

        for n in range(1, amount+1):
            players.append(Player('Player ' + str(n)))

        self.deck = []
        self.middle = Holders()

        if players:
            players[0].isturn = True
        else:
            self.error("No players", self.lineon())
        self.turn = 0

        self.build_deck()
        self.deal_cards()
        self.deal_middle(4)

    def build_deck(self):
        # Create a standard 52-card deck using the Card class
        # and shuffle it

        # Adding the numbers to numbers array
        for n in range(2,11):
            self.numbers.insert(n-1, str(n))

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
                self.deal(player, 2)
                # for i in range(0, 2):
                #     player.cards.append(self.deck.pop())

    def deal(self, player, amount):
        for n in range(amount):
            player.cards.append(self.deck.pop())

    def deal_middle(self, amount):
            # Placing 4 cards in middle

            # Separte from deal cards because no cards
            # are placed in the middle after each round
            for i in range(amount):
                self.middle.cards.append(self.deck.pop())

    def next_turn(self):
        players[self.turn].isturn = False

        if len(players) - 1 < self.turn + 1:
            self.turn = 0
            players[self.turn].isturn = True
        else:
            self.turn+=1
            players[self.turn].isturn = True
        self.next_round()

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

    def took(self, player):
        for p in players:
            if p is player:
                p.took = True
            else:
                p.took = False

    def check_points(self):
        for player in players:
            player.update_points()

        ##
        display_points(players)

        for player in players:
            if player.points >= 21:
                self.end_game()
        self.next_set()

    def next_round(self):
        if all([True if not player.cards else False for player in players]):
            if self.deck:
                 # Since ((52 - 4) ÷ 4) ÷ by a number of players from 2 to 4
                 # is always a whole number, there is no need to worry about
                 # having extra cards or not enough cards at the end
                self.deal_cards()
            else:
                # Give all the cards remaining in the middle to
                # the player who took last
                for player in players:
                    if player.took:
                        while self.middle.cards:
                            player.cards_taken.append(self.middle.cards.pop())

                self.check_points()

    def next_set(self):
        response = input("Would you like to continue playing? (Yes or No): ")
        if response.lower()[0] == "y":
            self.__init__()
        elif response.lower()[0] == "n":
            self.end_game()
        else:
            self.error("Unexpected response, please try again", self.lineon())
            self.next_set()

    def end_game(self):
        winner = [0, None]
        for player in players:
            if player.points > winner[0]:
                winner = [player.points, player]
        if winner[1]:
            ##
            display_winner(winner[1])
            # sys.exit()
        else:
            self.error("No player got any points", self.lineon())

##############
game = Game()

cards_by_object(players, game.middle)

check_turn(players)
