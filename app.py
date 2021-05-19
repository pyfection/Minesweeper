

from kivymd.app import MDApp
from kivy.factory import Factory


Factory.register('Grid', module='uix.grid')
Factory.register('OptionsBar', module='uix.options_bar')
Factory.register('ImageButton', module='uix.image_button')


class Minesweeper(MDApp):
    foreground_color = (.57, .72, .97)
    background_color = (.15, .16, .19)

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
        print(config, section, key, value)
