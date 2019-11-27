import random
import warnings


class Card:

    def __init__(self, value, suit=''):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.suit}{self.value}"

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit


class Deck:

    def __init__(self, deck):
        self.deck = deck

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += card.__str__() + ' '
        return f"{deck_comp}"

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Table:

    def __init__(self):
        self.cards = []
        self.value = 0

    def __str__(self):
        deck_comp = ''
        for card in self.cards:
            deck_comp += card.__str__() + ' '
        return f"{self.value} <= {deck_comp}"

    def draw(self, card):
        self.cards.append(card)
        if card.suit == '+/-':
            card.suit = input('Choose operator:\n')
        if card.suit == '+' or card.suit == '':
            self.value += int(card.value)
        else:
            self.value -= int(card.value)


class Hand:

    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        deck_comp = ''
        for card in self.cards:
            deck_comp += card.__str__() + ' '
        return f"{deck_comp}"

    def play(self, card):
        self.cards.remove(card)
        return card


def play(card, hand, table):
    table.draw(hand.play(card))
    print('\nCurrent table:', str(table))
    choice = input('  (1) End turn\n'
                   '  (2) Stand\n')
    return choice


def turn(deck, hand, table):
    table.draw(deck.deal())
    print('\nCurrent table:', str(table))
    print('Hand:', str(hand))
    choice = input('  (1) End turn\n'
                   '  (2) Play a card\n'
                   '  (3) Stand\n')
    while choice != '1' and choice != '2' and choice != '3':
        choice = input('Invalid choice. Please pick again.\n')

    if choice == '1' or choice == '3':
        return choice
    elif choice == '2':
        card = input('What card would you like to play?\n')
        value = card[-1:]
        if len(card) == 2:
            suit = card[0]
        else:
            suit = card[:3]
        choice = play(Card(value, suit), hand, table)
        if choice == '2':
            choice = '3'
        return choice


cards = []
for i in range(10):
    for j in range(4):
        card = Card(i + 1)
        cards.append(card)
deck = Deck(cards)
deck.shuffle()
side_deck_input = input('Build your side deck of four cards, '
                        'including suits and separating cards '
                        'by spaces (e.g. +5 -2 +/-3 -4):\n').split()
side_deck_cards = []
for card in side_deck_input:
    value = card[-1:]
    if len(card) == 2:
        suit = card[0]
    else:
        suit = card[:3]
    side_deck_cards.append(Card(value, suit))
side_deck = Hand(side_deck_cards)
table = Table()
while True:
    result = turn(deck, side_deck, table)
    if result == '3':
        print('\nStanding at', table.value)
        break
    if table.value > 20:
        print('\nBust:', table.value)
        break
