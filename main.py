from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class AnthobizApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Anthobiz', font_size='40sp', bold=True))
        layout.add_widget(Label(text='Business Management App\n\nReady to Build!', font_size='20sp'))
        return layout

if __name__ == '__main__':
    AnthobizApp().run()
