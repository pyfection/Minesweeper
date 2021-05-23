from time import time

from kivy.lang.builder import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


Builder.load_string("""
<ImageButton>:
    canvas:
        Color:
            rgba: app.theme_cls.accent_color
        Rectangle:
            texture: self.texture
            pos: self.pos
            size: self.size
""")


class ImageButton(ButtonBehavior, Image):
    double_press_time = 0.5
    last_touch_type = None
    _touch_time = 0

    def on_touch_down(self, touch):
        if time() - self._touch_time <= self.double_press_time:
            self.last_touch_type = 'double'
        else:
            self.last_touch_type = 'single'
        self._touch_time = time()
        return super().on_touch_down(touch)
