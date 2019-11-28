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


class Player:

    def __init__(self, number):
        self.number = number
        self.bust = False
        self.playing = True
        self.score = 0


def play(card, hand, table):
    table.draw(hand.play(card))
    print('Current table:', str(table))
    choice = input('  (1) End turn\n'
                   '  (2) Stand\n')
    return choice


def turn(deck, hand, table, player):
    table.draw(deck.deal())
    print(f'\n========== Player {player} ==========')
    print('Current table:', str(table))
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


def build_side_deck(player):
    side_deck_input = input(f'Player {player}, build your side deck of ten cards, '
                            'including suits and separating cards '
                            'by spaces (e.g. +5 -2 +/-3 ...):\n').split()
    if side_deck_input[0] == 'default':
        side_deck_input = '+1 +2 +3 +4 -1 -2 -3 -4 +/-2 +/-3'.split()
    valid = True
    if len(side_deck_input) != 10:
        valid = False
    for card in side_deck_input:
        if not len(card) == 2 and not len(card) == 4:
            valid = False
            break
        try:
            int(card[-1:])
        except ValueError:
            valid = False
            break
        if len(card) == 2:
            suit = card[0]
        else:
            suit = card[:3]
        if suit != '+' and suit != '-' and suit != '+/-':
            valid = False
            break
    while valid == False:
        side_deck_input = input('Invalid side deck entered. '
                                'Please try again:\n').split()
        for card in side_deck_input:
            if not len(card) == 2 and not len(card) == 4:
                break
            try:
                int(card[-1:])
            except ValueError:
                break
            if len(card) == 2:
                suit = card[0]
            else:
                suit = card[:3]
            if suit != '+' and suit != '-' and suit != '+/-':
                break
            valid = True
    side_deck_cards = []
    for card in side_deck_input:
        value = card[-1:]
        if len(card) == 2:
            suit = card[0]
        else:
            suit = card[:3]
        side_deck_cards.append(Card(value, suit))
    random.shuffle(side_deck_cards)
    return Hand(side_deck_cards[0:4])


if __name__ == "__main__":
    cards = []
    for i in range(10):
        for j in range(6):
            card = Card(i + 1)
            cards.append(card)
    deck = Deck(cards)
    deck.shuffle()
    player1 = Player(1)
    player2 = Player(2)
    side_deck_p1 = build_side_deck(player1.number)
    side_deck_p2 = build_side_deck(player2.number)
    while True:
        table_p1 = Table()
        table_p2 = Table()
        player1.playing = True
        player1.bust = False
        player2.playing = True
        player2.bust = False
        while True:
            if player1.playing:
                result = turn(deck, side_deck_p1, table_p1, player1.number)
                if table_p1.value > 20:
                    print('\nBust:', table_p1.value)
                    player1.playing = False
                    player1.bust = True
                    break
                if result == '3':
                    print('\nStanding at', table_p1.value)
                    player1.playing = False
            if player2.playing:
                result = turn(deck, side_deck_p2, table_p2, player2.number)
                if table_p2.value > 20:
                    print('\nBust:', table_p2.value)
                    player2.playing = False
                    player2.bust = True
                    break
                if result == '3':
                    print('\nStanding at', table_p2.value)
                    player2.playing = False
            if not player1.playing and not player2.playing:
                break
        if player1.bust:
            player2.score += 1
            print(f'\nPlayer 2 wins this round. Current score: {player1.score} - {player2.score}')
        elif player2.bust:
            player1.score += 1
            print(f'\nPlayer 1 wins this round. Current score: {player1.score} - {player2.score}')
        elif table_p1.value > table_p2.value:
            player1.score += 1
            print(f'\nPlayer 1 wins this round. Current score: {player1.score} - {player2.score}')
        elif table_p1.value < table_p2.value:
            player2.score += 1
            print(f'\nPlayer 2 wins this round. Current score: {player1.score} - {player2.score}')
        else:
            print(f'\nRound tied. Current score: {player1.score} - {player2.score}')
        if player1.score == 3:
            print(f'\nPlayer 1 wins. Final score: {player1.score} - {player2.score}')
            break
        if player2.score == 3:
            print(f'\nPlayer 2 wins. Final score: {player1.score} - {player2.score}')
            break