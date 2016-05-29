#!/usr/bin/env python3

import kxg
from vecrec import Rect

def get_card_key(suite, code):
    if suite:
        return suite + '-' + code
    else:
        return code


class World (kxg.World):

    card_size = 69, 93
    border = 2
    rows = 3
    cols = 10
    padding = 1
    field_size = cols * (2 * (padding + border) + card_size[0]), rows * (2 * (padding + border) + card_size[1])
    codes = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    suites = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
    phases = ('Dealing', 'Pegging', 'Scoring')

    def __init__(self):
        super().__init__()

        self.field = Rect.from_size(*self.field_size)
        self.cards = {} # do not remove items
        self.special_cards = {} # do not remove items
        
        self.starter_card = None
        self.pegging_stack = []

        self.players = []
        self.dealer = None
        self.pone = None
        self.active_player = None
        self.phase = None

        self.phase = None

    def get_value(self, name):
        return self.name_values[name]

    def get_card_key(self, suite, code):
        return get_card_key(suite, code)

    def on_start_dealing(self, dealer):
        self.phase = 'Dealing'
        
        self.dealer = dealer
        pone_index = self.players.index(dealer) - 1
        self.pone = self.players[pone_index]
        self.active_player = self.pone

        self.starting_card = None
        self.pegging_stack = []


    


