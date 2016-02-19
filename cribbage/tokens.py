#!/usr/bin/env python

import kxg

class Player(kxg.Token):

    def __init__(self):
        super().__init__()
        from getpass import getuser
        self.name = getuser()

        self.hand = []


class Card (kxg.Token):

    def __init__(self, card_info, suite):
        super().__init__()

        code, name, value = card_info

        self.code = code
        self.name = name
        self.value = value
        self.suite = suite

        self.in_play = False

    def __extend__(self):
        from . import gui
        return {
                gui.GuiActor: gui.CardExtension,
        }

