from kivy.app import App
from kivy.uix.label import Label

class AnthobizApp(App):
    def build(self):
        return Label(text="Anthobiz Business Management App - Working!")

if __name__ == '__main__':
    AnthobizApp().run()
