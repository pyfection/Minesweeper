import random
from time import time

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty, NumericProperty, ListProperty, OptionProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior


Builder.load_file('uix/grid.kv')


class GridButton(ButtonBehavior, RelativeLayout):
    coord = ListProperty()
    status = OptionProperty('covered', options=['covered', 'uncovered', 'flagged'])
    has_bomb = False
    flagged = NumericProperty(0)
    images = {
        'covered': 'img/tile_full.png',
        'uncovered': 'img/tile_empty.png',
        'flagged': 'img/tile_flag.png',
        'bomb': 'img/tile_bomb.png',
    }

    def on_status(self, _, status):
        number = self.number
        if status == 'uncovered' and number is None:
            self.main_img.source = self.images['bomb']
        else:
            self.main_img.source = self.images[status]

        if status == 'uncovered' and number is not None:
            self.number_img.source = f'img/num_{number}.png'
            ann = max(number - self.flagged, 0)
            self.annotate_img.source = f'img/num_{ann}.png'

        # Update flags set on neighbours
        x, y = self.coord
        if status in ('flagged', 'covered'):
            f = 1 if status == 'flagged' else -1
            for rx in range(-1, 2):
                ax = x + rx
                if not (0 <= ax < self.parent.cols):
                    continue

                for ry in range(-1, 2):
                    ay = y + ry
                    if not (0 <= ay < self.parent.rows):
                        continue

                    field = self.parent.field[(ax, ay)]
                    field.flagged = max(field.flagged + f, 0)

    def on_flagged(self, _, flagged):
        if self.status == 'uncovered' and MDApp.get_running_app().config.get('minesweeper', 'number_satisfied'):
            ann = max(self.number-flagged, 0)
            self.annotate_img.source = f'img/num_{ann}.png'

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


class Grid(GridLayout):
    cols = NumericProperty(10)
    rows = NumericProperty(10)
    bombs = NumericProperty(10)
    flags = NumericProperty(0)
    mode = OptionProperty('uncover', options=['uncover', 'flag'])
    status = OptionProperty('setup', options=['new', 'active', 'won', 'lost', 'setup'])
    time = NumericProperty(0)  # in seconds
    _start_time = 0

    def __init__(self, **kwargs):
        self.field = {}
        super().__init__(**kwargs)
        self.refresh()

    def get_max_widgets(self):
        # Overwriting to avoid error
        return None

    def refresh(self):
        self.status = 'setup'
        self.flags = 0
        self.time = 0
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
        elif field.number is None:
            self.status = 'lost'

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
        def update_time(dt):
            if self.status != 'active':
                Clock.unschedule(update_time)
            self.time = time() - self._start_time

        if self.status in ('won', 'lost', 'setup'):
            return

        if self.mode == 'flag':
            if btn.status == 'covered':
                btn.status = 'flagged'
                self.flags += 1
                return
            elif btn.status == 'flagged':
                btn.status = 'covered'
                self.flags -= 1
                return

        if btn.status == 'uncovered':
            if btn.flagged == btn.number:
                self.uncover_neighbours(*btn.coord)

        if self.status == 'new':
            self.generate(*btn.coord)
            self.status = 'active'
            self._start_time = time()
            Clock.schedule_interval(update_time, 1)

        self.uncover(*btn.coord)

        # Check if all fields are uncovered
        covered = len([field for field in self.field.values() if field.status in ('covered', 'flagged')])
        if covered == self.bombs:
            self.status = 'won'

    def on_cols(self, _, cols):
        self.refresh()

    def on_rows(self, _, rows):
        self.refresh()
