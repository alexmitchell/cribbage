#!/usr/bin/env python3

import os.path
import kxg, pyglet, glooey, random
from vecrec import Vector
from . import world, tokens, messages

pyglet.resource.path = [
        os.path.join(os.path.dirname(__file__), '..', 'resources'),
        os.path.join(os.path.dirname(__file__), '..', 'resources','cards'),
        os.path.join(os.path.dirname(__file__), '..', 'resources','borders'),
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

        self.border_images = {}
        for border_name in "border", "border-over", "border-down", "border-selected":
                filename = border_name + '.png'
                self.border_images[border_name] = pyglet.resource.image(filename)

        # Center all the images, which we will want to rotate around it's 
        # leftmost edge.

        for image in self.images.values():
            image.anchor_x = image.width / 2
            image.anchor_y = image.height / 2
        
        # Create the viewing grid
        rows = world.World.rows
        cols = world.World.cols
        padding = world.World.padding
        self.root = glooey.Gui(self.window, batch=self.batch)
        self.grid = glooey.Grid(rows, cols, padding=padding)
        for row, col in self.grid.yield_cells():
            self.grid[row, col] = CardButton(self)
        self.root.add(self.grid)

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

        grid = self.gui.grid
        for row, col in grid.yield_cells():
            card_button = grid[row, col]
            card_button.setup_gui_actor(self)

        # Save special cells
        self.hand_buttons = [ grid[2, i] for i in range(1,7)]
        for button in self.hand_buttons:
            button.make_selectable()

        self.selected_cards = []
        self.max_selection = 2

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

                self.hand_buttons[i].assign_card(card)

                #x = card_x * (i + 0.5) + card_x
                #y = card_y / 2.0
                #ext = card.get_extension(self)
                #ext.activate(Vector(x,y))


    def select_card(self, card_button):
        # Remember the selected cards. Enforce a max of two selections
        self.selected_cards.append(card_button)
        if len(self.selected_cards) > self.max_selection:
            old = self.selected_cards.pop(0)
            old.unselect()

    def unselect_card(self, card_button):
        self.selected_cards.remove(card_button)



class SelectButton (glooey.Button):

    def __init__ (self, gui, selectable=True):
        super().__init__()

        self.gui = gui
        self.selectable = selectable

        # Set up the glooey button
        self.set_base_image(gui.border_images["border"])
        self.set_over_image(gui.border_images["border-over"])
        self.set_down_image(gui.border_images["border-down"])
        self.set_selected_image(gui.border_images["border-selected"])
        self.selected = False

    def setup_gui_actor(self, gui_actor):
        self.gui_actor = gui_actor

    def set_selected_image(self, image):
        # Glooey button functionality. Probably should be added to glooey.
        self.images['selected'] = image

    def make_selectable(self):
        self.selectable = True
    def make_unselectable(self):
        self.selectable = False
    def draw(self):
        super().draw()

    def select(self):
        self.state = 'selected'
        self.selected = True
        self.draw()

    def unselect(self):
        self.state = 'base'
        self.selected = False
        self.draw()

    def on_mouse_release(self, x, y, button, modifiers):
        # overload glooey's Button functionality. Again, probably should be 
        # added to glooey instead.

        if self.selectable:
            if self.selected:
                self.gui_actor.unselect_card(self)
                self.unselect()
                self.state = 'over'
            else:
                self.gui_actor.select_card(self)
                self.select()
        
    def on_mouse_leave(self, x, y):
        # overload glooey's Button functionality. Again, probably should be 
        # added to glooey instead.
        if self.selected:
            self.state = 'selected'
        else:
            self.state = 'base'
        self.draw()

    def on_mouse_drag_enter(self, x, y):
        # overload glooey's Button functionality. Again, probably should be 
        # added to glooey instead.
        if self.selectable:
            self.state = 'down'
            self.draw()

    def on_mouse_drag_leave(self, x, y):
        # overload glooey's Button functionality. Again, probably should be 
        # added to glooey instead.
        if self.selected:
            self.state = 'selected'
        else:
            self.state = 'base'
        self.draw()


class CardButton (SelectButton):

    def __init__ (self, gui, selectable=True):
        super().__init__(gui, selectable)

        self.gui = gui
        self.selectable = selectable

        # Set up the card handling
        self.card = None

    def setup_gui_actor(self, gui_actor):
        self.gui_actor = gui_actor

    def assign_card(self, card):
        self.card = card
        
        # set the position of the card_image
        x, y = self.rect.center
        ext = card.get_extension(self.gui_actor)
        ext.activate(Vector(x,y))

        self.draw()

    def unassign_card(self):
        ext = self.card.get_extension(self.gui_actor)
        ext.deactivate()
        self.card = None

    def draw(self):
        # Only draw the button if it contains a card.
        if self.card:
            super().draw()



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

    def activate(self, position):
        self.position = position
        self.card_image.position = position
        self.card_image.visible = True
        
    def deactivate(self):
        self.card_image.visible = False
        
    @kxg.watch_token
    def on_update_game(self, delta_t):
        pass

    @kxg.watch_token
    def on_remove_from_world(self):
        pass


