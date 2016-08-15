from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

Builder.load_string("""
<Task>:
    size_hint: 0.5, 0.5
    pos_hint: {'center': [0.5, 0.5]}
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            Spinner:
                id: tablesel
                text: 'Choose data:'
                values: [child[0] for child in app.root.tables]
                on_text:
                    root.tablenum = root.get_table_pos(self.text, self.values)

        BoxLayout:
            id: container

        BoxLayout:
            size_hint_y: None
            height: dp(60)
            Button:
                text: 'Cancel'
                on_release: root.dismiss()

            Button:
                text: 'Run'
                disabled: True if tablesel.text == '' else False
                on_release: root.try_run()

<CountLayout>:
    orientation: 'vertical'
    TextInput:
        id: name

<SmallLargeLayout>:
    orientation: 'vertical'
    BoxLayout:
        Label:
            text: 'Address'
        TextInput:
            id: name
    BoxLayout:
        Label:
            text: 'k ='
        TextInput:
            id: order
    Label:
        text: 'Example: k=2 for the second smallest value.'
""")


class CountLayout(BoxLayout):
    pass


class SmallLargeLayout(BoxLayout):
    pass


class Task(Popup):
    run = ObjectProperty(None)

    def __init__(self, **kw):
        super(Task, self).__init__(**kw)
        self.app = App.get_running_app()
        self.run = kw.get('run', None)
        wdg = kw.get('wdg', None)
        self.call = kw.get('call', None)
        self.from_address = self.app.root.from_address
        self.set_page = self.app.root.set_page
        if wdg:
            self.ids.container.add_widget(wdg)

    def get_table_pos(self, text, values, *args):
        print values
        gen = (i for i, val in enumerate(values) if val == text)
        for i in gen:
            return i

    def try_run(self, *args):
        try:
            self.run(*args)
            if self.call:
                but = Button(size_hint_y=None, height='25dp',
                             text=self.call[0])
                but.bind(on_release=self.call[1])
                self.app.root.ids.recenttasks.add_widget(but)
            self.dismiss()
        except Exception as err:
            Logger.exception(err)
