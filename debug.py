
"""Since its based on console, these functions are mostly used
for displaying useful information and the game itself"""

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
def cards_by_object(players, middle):
    length = len(players)
    half = length / 2 if length % 2 == 0 else 2
    for n in range(length):
        if n == half:
            print("--------------Middle")
            print_cards(middle)
        print("--------------" + players[n].name)
        print_cards(players[n])
    print("--------------")

# DEBUG: function to print out who's turn it is
def check_turn(players):
    for player in players:
        if player.isturn == True:
            print("It is " + player.name + "'s turn")
            return
    Error.error(None, "Weird, it is no one's turn",
                self.lineon())
