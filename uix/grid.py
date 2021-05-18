import random

from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, ListProperty, OptionProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


Builder.load_file('uix/grid.kv')


class GridButton(ButtonBehavior, Image):
    coord = ListProperty()
    status = OptionProperty('covered', options=['covered', 'uncovered', 'flagged'])
    has_bomb = False
    images = {
        'covered': 'img/tile_full.png',
        'uncovered': 'img/tile_empty.png',
        'flagged': 'img/tile_flag.png',
        'number': 'img/tile_{num}.png',
        'bomb': 'img/tile_bomb.png',
    }

    def on_status(self, _, status):
        number = self.number
        if status == 'uncovered' and number:
            self.source = self.images['number'].format(num=number)
        elif status == 'uncovered' and number is None:
            self.source = self.images['bomb']
        else:
            self.source = self.images[status]

    @property
    def number(self):
        if self.has_bomb:
            return None

        num = 0
        x, y = self.coord

        for rx in range(-1, 2):
            ax = x + rx
            if not (0 <= ax < self.parent.cols):
                continue

            for ry in range(-1, 2):
                ay = y + ry
                if not (0 <= ay < self.parent.rows):
                    continue

                if self.parent.field[(ax, ay)].has_bomb:
                    num += 1

        return num

    @property
    def flagged(self):
        if self.has_bomb:
            return None

        num = 0
        x, y = self.coord

        for rx in range(-1, 2):
            ax = x + rx
            if not (0 <= ax < self.parent.cols):
                continue

            for ry in range(-1, 2):
                ay = y + ry
                if not (0 <= ay < self.parent.rows):
                    continue

                if self.parent.field[(ax, ay)].status == 'flagged':
                    num += 1

        return num


class Grid(GridLayout):
    cols = NumericProperty(10)
    rows = NumericProperty(10)
    bombs = 10
    is_new = True
    mode = OptionProperty('uncover', options=['uncover', 'flag'])

    def __init__(self, **kwargs):
        self.field = {}
        super().__init__(**kwargs)
        self.refresh()

    def refresh(self):
        self.is_new = True
        self.clear_widgets()
        self.field = {(x, y): GridButton(coord=(x, y)) for y in range(self.rows) for x in range(self.cols)}
        for btn in self.field.values():
            self.add_widget(btn)

    def generate(self, x, y):
        fields = list(self.field.keys())

        for rx in range(-1, 2):
            ax = x + rx
            if not (0 <= ax < self.cols):
                continue

            for ry in range(-1, 2):
                ay = y+ry
                if not (0 <= ay < self.rows):
                    continue

                fields.remove((ax, ay))

        for i in range(self.bombs):
            j = random.randint(0, len(fields)-1)
            field = fields.pop(j)
            self.field[field].has_bomb = True

    def uncover(self, x, y):
        field = self.field[(x, y)]
        if field.status in ('uncovered', 'flagged'):
            return

        field.status = 'uncovered'
        if field.number == 0:
            self.uncover_neighbours(x, y)

    def uncover_neighbours(self, x, y):
        for rx in range(-1, 2):
            ax = x + rx
            if not (0 <= ax < self.cols):
                continue

            for ry in range(-1, 2):
                ay = y + ry
                if not (0 <= ay < self.rows):
                    continue

                self.uncover(ax, ay)

    def on_click(self, btn):
        if self.mode == 'flag':
            if btn.status == 'covered':
                btn.status = 'flagged'
                return
            elif btn.status == 'flagged':
                btn.status = 'covered'
                return

        if btn.status == 'uncovered':
            if btn.flagged == btn.number:
                self.uncover_neighbours(*btn.coord)

        if self.is_new:
            self.generate(*btn.coord)
            self.is_new = False

        self.uncover(*btn.coord)

    def on_cols(self, cols):
        self.refresh()

    def on_rows(self, rows):
        self.refresh()
