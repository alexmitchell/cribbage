#!/usr/bin/env python3

import os.path
import kxg, pyglet, glooey, random
from vecrec import Vector
from . import world, tokens, messages

pyglet.resource.path = [
        os.path.join(os.path.dirname(__file__), '..', 'resources'),
        os.path.join(os.path.dirname(__file__), '..', 'resources','cards'),
]

class Gui:

    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_visible(True)
        self.window.set_size(*world.World.field_size)
        self.batch = pyglet.graphics.Batch()

        self.bg_color = glooey.drawing.white

        # Load all the sprite images from resource files.

        self.images = {}
        for code in world.World.codes:
            for suite in world.World.suites:
                key = world.get_card_key(suite, code)
                filename = suite[0] + code + '.png'
                self.images[key] = pyglet.resource.image(filename)

        # Center all the images, which we will want to rotate around it's 
        # leftmost edge.

        for image in self.images.values():
            image.anchor_x = image.width / 2
            image.anchor_y = image.height / 2

    def on_refresh_gui(self):
        pyglet.gl.glClearColor(*self.bg_color)
        self.window.clear()
        self.batch.draw()

    def get_card_image(self, suite, code):
        key = world.get_card_key(suite, code)
        return self.images[key]


class GuiActor (kxg.Actor):

    def __init__(self):
        super().__init__()
        self.player = None

    def on_setup_gui(self, gui):
        self.gui = gui
        self.gui.window.set_handlers(self)

    def on_start_game(self, num_players):
        self.player = tokens.Player()
        self >> messages.CreatePlayer(self.player)

    def on_draw(self):
        self.gui.on_refresh_gui()

    def on_update_game(self, dt):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    @kxg.subscribe_to_message(messages.DealToPlayer)
    def on_deal_to_player(self, message):
        (card_x, card_y) = self.world.card_size
        if self.player == message.player:
            codes = [card.code for card in self.player.hand]
            kxg.info("Cards deltith to {self.player}. Cards: {codes}")

            for (i, card) in enumerate(self.player.hand):
                x = card_x * (i + 0.5) + card_x
                y = card_y / 2.0
                ext = card.get_extension(self)
                ext.activate_card(Vector(x,y))


class CardExtension (kxg.TokenExtension):

    @kxg.watch_token
    def on_add_to_world(self, world):
        
        self.position = world.field.center
        suite = self.token.suite
        code = self.token.code

        self.card_image = pyglet.sprite.Sprite(
                self.actor.gui.get_card_image(suite, code),
                x=self.position.x,
                y=self.position.y,
                batch=self.actor.gui.batch,
                group=pyglet.graphics.OrderedGroup(1),
        )
        
        self.card_image.visible = False

    def activate_card(self, position):
        self.position = position
        self.card_image.position = position
        self.card_image.visible = True
        
    @kxg.watch_token
    def on_update_game(self, delta_t):
        if not self.token.in_play:
            self.card_image.visible = False

    @kxg.watch_token
    def on_remove_from_world(self):
        pass


