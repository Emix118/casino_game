from player import Player, players
from error import Error

"""Since its based on console, these functions are mostly used
for displaying useful information and the game itself"""

class debug(Error):

    # DEBUG: function to print out each card's number and type
    def print_cards(self, object):
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
    def cards_by_object(self, objects):
        for o in objects:
            if isinstance(o, Player):
                print("--------------" + o.name)
            else:
                print("--------------Middle")
            self.print_cards(o)
        print("--------------")

    # DEBUG: function to print out who's turn it is
    def check_turn(self):
        for player in players:
            if player.isturn == True:
                print("It is " + player.name + "'s turn")
                return
        Error.error(None, "Weird, it is no one's turn",
                    self.lineon())
