#!/usr/bin/env python3

import kxg, random
from . import messages, tokens

class Referee (kxg.Referee):

    def __init__(self):
        super().__init__()
        self.num_players_expected = None

        self.deck = []
        self.in_play = []
        self.in_hands = []
        self.discard_pile = []
        self.crib = []
        self.starter_card = []

    def on_start_game(self, num_players):
        self.num_players_expected = num_players

    @kxg.subscribe_to_message(messages.CreatePlayer)
    def on_create_player(self, message):
        num_players_joined = len(self.world.players)
        kxg.info("{num_players_joined} of {self.num_players_expected} players created.")

        if num_players_joined == self.num_players_expected:
            self >> messages.StartGame(self.world)

    @kxg.subscribe_to_message(messages.StartGame)
    def on_start_game_message(self, message):
        self.deck = list(self.world.cards.values())
        dealer = random.choice(self.world.players)
        self >> messages.StartDealing(self.world, dealer)

    @kxg.subscribe_to_message(messages.StartDealing)
    def on_start_dealing(self, message):
        world = self.world
        for player in world.players:
            kxg.info("Dealing to player {player}).")

            new_hand = self.draw_cards(6)
            self >> messages.DealToPlayer(player, new_hand)

    def on_update_game(self, dt):
        if not self.world.phase:
            self >> messages.StartDealing(self.world)


    def draw_card(self):

        # If the deck is empty, shuffle the discard pile back into it.

        if not self.deck:
            self.shuffle_discard_pile()

        # Draw a random card from the deck

        index = random.randrange(len(self.deck))
        card = self.deck.pop(index)
        self.in_hands.append(card)
        return card

    def draw_cards(self, number):
        return [self.draw_card() for x in range(number)]

    def discard_card(self, card):
        self.in_hands.remove(card)
        self.discard_pile.append(card)

    def discard_cards(self, cards):
        for card in cards:
            self.discard_card(card)

    def shuffle_discard_pile(self):
        self.deck += self.discard_pile
        self.discard_pile = []



