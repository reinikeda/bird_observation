from tkinter import *
from app.bird import BirdList
from app.observer import ObserverList
from app.observation import ObservationList

class MyButton(Button):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self['bg'] = kwargs.get('bg', '#c2e7ec')
        self['activebackground'] = kwargs.get('activebackground', '#a4d8df')
        self['font'] = kwargs.get('font', 'Helvetica')
        self['width'] = kwargs.get('width', 20)
        self['pady'] = kwargs.get('pady', 20)

class MainApp():
    def __init__(self, main):
        self.main = main
        self.b_bird = MyButton(self.main, text='Birds list', command=self.run_bird)
        self.b_observer = MyButton(self.main, text='Observers list', command=self.run_observer)
        self.b_observation = MyButton(self.main, text='Bird observations list', command=self.run_observation)
        self.b_exit = MyButton(self.main, text='Exit', command=self.main.destroy)

        self.b_bird.pack(pady=10)
        self.b_observer.pack(pady=10)
        self.b_observation.pack(pady=10)
        self.b_exit.pack(pady=10)

    def run_bird(self):
        self.window_bird = Toplevel(self.main)
        self.app = BirdList(self.window_bird)

    def run_observer(self):
        self.window_observer = Toplevel(self.main)
        self.app = ObserverList(self.window_observer)

    def run_observation(self):
        self.window_observation = Toplevel(self.main)
        self.app = ObservationList(self.window_observation)