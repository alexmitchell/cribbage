#!/usr/bin/env python3

import kxg, random
from vecrec import Rect

def get_card_key(suite, code):
    return suite + '-' + code


class World (kxg.World):

    field_size = 975, 400
    codes = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    suites = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
    phases = ('Dealing', 'Pegging', 'Scoring')

    def __init__(self):
        super().__init__()


        self.field = Rect.from_size(*self.field_size)
        self._deck = {} # do not remove items

        
        self.deck = [] # security? have referee store it instead?
        self.in_play = [] # security? have referee store it instead?
        self.discard_pile = [] # security? have referee store it instead?
        self.crib = [] # security? have referee store it instead?
        self.starter_card = [] # security? have referee store it instead?
        self.pegging_stack = []

        self.players = []
        self.dealer = None
        self.active_player = None
        self.phase = None

        #self.phase?

    def get_value(self, name):
        return self.name_values[name]

    """
    def draw_card(self):

        # If the deck is empty, shuffle the discard pile back into it.

        if not self.deck:
            self.shuffle_discard_pile()

        # Draw a random card from the deck

        index = random.randrange(len(self.deck))
        card = self.deck.pop(index)
        self.in_play.append(card)
        return card

    def draw_cards(self, num):
        return [self.draw_card() for x in range(num)]

    def discard_card(self, card):
        self.discard_pile.append(card)

    def on_start_dealing(self):
        #self.discard_cards(self.crib)
        #self.discard_card(self.starting_card)
        #self.discard_cards(self.pegging_stack)

        #world.phase = 'Dealing'
        pass
    """
