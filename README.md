Casino Game

To start the game:
  1 - Run game.py

  2 - import the players from player.py:

      from player import player1, player2...
        or
      player1 = players[0]
      player2 = player[1]...

To select the amount of players:
  1 - Go to player.py and comment or uncomment the lines defining the Player instances, here you can also give a name to each player.

Syntax:

card numbers can be the letters A, J, K, Q or their respective words (NOT case sensitive) or the numbers 1-10 as intigers or strings

card types have to start with the letter D,C,H,S (Not case sensitive)

take(), stack(), combine() --> (your card's number, your card's type, [middle card number, middle card type], [middle card]...)
NOTE: These functions take an infinite number of middle cards, but these cant always be taken due to game rules

trail() --> (card number, card type)
