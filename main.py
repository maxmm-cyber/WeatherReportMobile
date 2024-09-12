from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton


class WScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class   WReportApp(MDApp):
    def build(self):
        Builder.load_file("style.kv")
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"

        return WScreen()
        

WReportApp().run()