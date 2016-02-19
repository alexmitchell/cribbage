#!/usr/bin/env python



import kxg, random
from . import tokens

class CreatePlayer (kxg.Message):
    """
    Create a player.
    """

    def __init__(self, player):
        self.player = player

    def tokens_to_add(self):
        yield self.player

    def on_check(self, world):
        if self.player in world.players:
            raise kxg.MessageCheck("player already exists")

    def on_execute(self, world):
        world.players.append(self.player)


class StartGame (kxg.Message):
    """
    Create the cards
    """

    def __init__(self, world):

        card_data = (
                ('A',   "Ace",      1 ),
                ('2',   "Two",      2 ),
                ('3',   "Three",    3 ),
                ('4',   "Four",     4 ),
                ('5',   "Five",     5 ),
                ('6',   "Six",      6 ),
                ('7',   "Seven",    7 ),
                ('8',   "Eight",    8 ),
                ('9',   "Nine",     9 ),
                ('10',  "Ten",      10),
                ('J',   "Jack",     10),
                ('Q',   "Queen",    10),
                ('K',   "King",     10),
        )
        suites = ["Hearts", "Diamonds", "Spades", "Clubs"]
        self.cards = [ tokens.Card(card_datum, suite)
                for card_datum in card_data
                for suite in suites
        ]

    def tokens_to_add(self):
        yield from self.cards

    def on_check(self, world):
        if world.cards:
            raise kxg.MessageCheck("cards already exists")

    def on_execute(self, world):
        world.cards = self.cards[:]


class StartDealing (kxg.Message):
    """
    Being the Dealing phase
    """

    def __init__(self, world, dealer):
        self.dealer = dealer

    def on_check(self, world):
        phase = world.phase
        if not (phase == 'Scoring' or phase == None):
            raise kxg.MessageCheck("Not in correct phase to start dealing")

    def on_execute(self, world):
        world.on_start_dealing(self.dealer)


class DiscardToCrib (kxg.Message):

    """
    Discard two cards to the crib.
    """

    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def on_check(self, world):
        if not len(self.cards) == 2:
            raise kxg.MessageCheck("Player must discard exactly two cards")
        if not (cards[0] in self.player.hand and cards[1] in self.player.hand):
            raise kxg.MessageCheck("Card not in player's hand.")

    def on_execute(self, world):
        for card in self.cards:
            self.player.hand.remove(card)
            world.crib.append(card)


class DealToPlayer (kxg.Message):

    """
    Deal 6 cards to a player.
    """

    def __init__(self, player, cards):
        self.player = player
        self.cards = cards

    def on_check(self, world):
        if not self.was_sent_by_referee():
            raise kxg.MessageCheck("Only the referee can deal cards.")

    def on_execute(self, world):
        for card in self.cards:
            card.in_play = True
        self.player.hand = self.cards[:]

        codes = [card.code for card in self.cards]
        kxg.info("Dealing cards to {self.player}. Cards: {codes}")



