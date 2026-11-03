from kivy.app import App
from kivy.uix.label import Label

class AnthobizApp(App):
    def build(self):
        return Label(text="Anthobiz Works!")

AnthobizApp().run()
