#!/usr/bin/env python3

import kxg
from . import messages, tokens

class Referee (kxg.Referee):

    def __init__(self):
        super().__init__()
        self.num_players_expected = None

    def on_start_game(self, num_players):
        self.num_players_expected = num_players

    @kxg.subscribe_to_message(messages.CreatePlayer)
    def on_create_player(self, message):
        num_players_joined = len(self.world.players)
        kxg.info("{num_players_joined} of {self.num_players_expected} players created.")

        if num_players_joined == self.num_players_expected:
            self >> messages.StartGame(self.world)

#    @kxg.subscribe_to_message(messages.StartGame)
#    def on_start_game(self, message):
#
#        #self >> messages.StartDealing(self.world)
#        pass

    def on_update_game(self, dt):
        pass

