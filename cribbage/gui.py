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
        self.debug_ran_once = False

    def on_setup_gui(self, gui):
        self.gui = gui
        self.gui.window.set_handlers(self)

    def on_start_game(self, num_players):
        self.player = tokens.Player()
        self >> messages.CreatePlayer(self.player)

    def on_draw(self):
        self.gui.on_refresh_gui()

    def on_update_game(self, dt):
        if not self.debug_ran_once:
            self.set_extension_positions()
            self.debug_ran_once = True

    def on_key_press(self, symbol, modifiers):

        suites_dict = {
                pyglet.window.key.H : "Hearts",
                pyglet.window.key.D : "Diamonds",
                pyglet.window.key.S : "Spades",
                pyglet.window.key.C : "Clubs",
                pyglet.window.key.A : "",
        }

        if symbol in suites_dict:
            for card in self.world._deck:
                ext = card.get_extension(self)

                if card.suite == suites_dict[symbol] or symbol == pyglet.window.key.A:
                    ext.card_image.visible = True
                else:
                    ext.card_image.visible = False


    def set_extension_positions(self):
        # Set initial card positions for testing

        i = 0
        coors = []
        for card in self.world._deck:
            x = i%13 * 75 + 37.5
            y = i//13 * 100 + 50
            ext = card.get_extension(self)

            ext.position = Vector(x,y)

            coors.append((x,y))

            i += 1


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

    @kxg.watch_token
    def on_update_game(self, delta_t):
        self.card_image.position = self.position

    @kxg.watch_token
    def on_remove_from_world(self):
        pass


