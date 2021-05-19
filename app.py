

from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.settings import InterfaceWithSpinner


Factory.register('Grid', module='uix.grid')
Factory.register('OptionsBar', module='uix.options_bar')
Factory.register('ImageButton', module='uix.image_button')


class Minesweeper(MDApp):
    def build_config(self, config):
        config.setdefaults(
            'minesweeper',
            {
                'number_satisfied': False,
            }
        )

    def build_settings(self, settings):
        settings.add_json_panel(
            "Minesweeper",
            self.config,
            filename='config.json'
        )

    def on_config_change(self, config, section, key, value):
        # e.g: "<kivy.config.ConfigParser object at 0x7f7a9922fc50> minesweeper number_satisfied 1"
        print(config, section, key, value)
