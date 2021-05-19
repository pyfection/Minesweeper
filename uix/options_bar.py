

from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.lang.builder import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image


Builder.load_file('uix/options_bar.kv')


class Option(ButtonBehavior, Image):
    _color = ListProperty([1, 1, 1, 0])
    active = BooleanProperty(False)
    name = StringProperty()

    def on_active(self, _, active):
        self._color = (1, 1, 1, 0.5) if active else (1, 1, 1, 0)


class OptionsBar(MDBoxLayout):
    options = ListProperty()
    current = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._options = {}

    def on_options(self, _, options):
        def _set_current(widget):
            self.current = widget.name
            for other in self.children:
                other.active = False
            widget.active = True

        self.clear_widgets()
        for data in options:
            option = Option(**data)
            option.bind(on_press=_set_current)
            self._options[data['name']] = option
            self.add_widget(option)
        self.children[-1].active = True
