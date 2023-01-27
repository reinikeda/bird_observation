from tkinter import *
from tkinter import ttk
from create_db import *
from app.back_end import *
import sqlite3

conn = sqlite3.connect('sqlite:///../data/birds_observation.db')
c = conn.cursor()

class MyButton(Button):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self['bg'] = kwargs.get('bg', '#c2e7ec')
        self['activebackground'] = kwargs.get('activebackground', '#a4d8df')
        self['width'] = kwargs.get('width', 20)
        self['pady'] = kwargs.get('pady', 10)

class ObservationList:
    def __init__(self, main):
        self.main = main
        self.main.iconbitmap(r'app/bird.ico')
        self.main.title('BOA: Bird Observation App')
        self.main.config(bg='#e4fafd')
        self.f_top = Frame(self.main, bg='#e4fafd')
        self.l_title = Label(self.f_top, text='Observations window', bg='#e4fafd')
        self.columns = ('id', 'observer_id', 'bird_id', 'number', 'place', 'date')
        self.tree = ttk.Treeview(self.f_top, columns=self.columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('observer_id', text='Observer')
        self.tree.heading('bird_id', text='Bird')
        self.tree.heading('number', text='Number of birds')
        self.tree.heading('place', text='Place')
        self.tree.heading('date', text='Date')
        self.tree.insert('', END, self.read_observations())
        self.tree_scrollbar = Scrollbar(self.f_top, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.tree_scrollbar.set)

        self.f_bottom = Frame(self.main, bg='#e4fafd')

        self.l_add = Label(self.f_bottom, text='Add new observation', bg='#e4fafd')
        self.l_observer = Label(self.f_bottom, text='Choose observer', bg='#e4fafd')
        self.observer = ttk.Combobox(self.f_bottom, state='readonly', values=self.read_observers())

        self.l_bird = Label(self.f_bottom, text='Choose bird', bg='#e4fafd')
        self.bird = ttk.Combobox(self.f_bottom, state='readonly', values=self.read_birds())

        self.l_number = Label(self.f_bottom, text='Enter count', bg='#e4fafd')
        self.e_number = Entry(self.f_bottom)

        self.l_place = Label(self.f_bottom, text='Choose place', bg='#e4fafd')
        self.place = ttk.Combobox(self.f_bottom, state='readonly', values=self.read_places())

        self.l_date = Label(self.f_bottom, text='Enter date', bg='#e4fafd')
        self.e_date = Entry(self.f_bottom)

        self.b_add = MyButton(self.f_bottom, text='Add to database', command=self.add_new)
        self.b_clear = MyButton(self.f_bottom, text='Clear boxes', command=self.clear)
        self.b_restart = MyButton(self.f_bottom, text='Show/Restart list', command=self.read_observations)
        self.b_exit = MyButton(self.f_bottom, text='Exit', command=self.main.destroy)

        self.status = Label(self.f_bottom, text='Latest database information', relief=SUNKEN, border=1, bg='#e4fafd')

        self.f_top.pack()
        self.l_title.pack()
        self.tree.pack(side=LEFT)
        self.tree_scrollbar.pack(side=RIGHT, fill=Y)

        self.f_bottom.pack()
        self.l_add.grid(row=0, column=0, columnspan=7, padx=5)
        self.l_observer.grid(row=1, column=0, padx=5)
        self.observer.grid(row=2, column=0, padx=5)
        self.l_bird.grid(row=1, column=1, padx=5)
        self.bird.grid(row=2, column=1, padx=5)
        self.l_number.grid(row=1, column=2, padx=5)
        self.e_number.grid(row=2, column=2, padx=5)
        self.l_place.grid(row=1, column=3, padx=5)
        self.place.grid(row=2, column=3, padx=5)
        self.l_date.grid(row=1, column=4, padx=5)
        self.e_date.grid(row=2, column=4, padx=5)
        self.b_add.grid(row=2, column=5, padx=5)
        self.b_clear.grid(row=3, column=5, padx=5)
        self.b_restart.grid(row=2, column=6, padx=5)
        self.status.grid(row=3, column=0, columnspan=5, sticky=NW, padx=5, pady=20)

        self.b_exit.grid(row=3, column=6, padx=10)

    def read_observations(self):
        self.tree.delete(*self.tree.get_children())
        with conn:
            c.execute('SELECT * FROM bird_observation')
            rows = c.fetchall()
            for row in rows:
                self.tree.insert('', END, values=row)

    def read_observers(self):
        with conn:
            c.execute('SELECT id, f_name, l_name FROM observer')
            rows = c.fetchall()
            observer_list = []
            for row in rows:
                observer_list.append(row[1:3])
            return observer_list

    def read_birds(self):
        with conn:
            c.execute('SELECT id, species_lt FROM bird')
            rows = c.fetchall()
            bird_list = []
            for row in rows:
                bird_list.append(row[1])
            return bird_list

    def read_places(self):
        with conn:
            c.execute('SELECT id, place FROM place')
            rows = c.fetchall()
            places_list = []
            for row in rows:
                places_list.append(row[1])
            return places_list

    def add_new(self):
        # reikia gauti ID vietoje NAME
        add_new_row(self.observer.get(), self.bird.get(), self.e_number.get(), self.place.get(), self.e_date.get())
        self.status['text'] = f'Added new entry {self.bird.get()} from {self.observer.get()}. Click button to restart the list.'

    def clear(self):
        self.observer.set('')
        self.bird.set('')
        self.e_number.delete(0, END)
        self.place.set('')
        self.e_date.delete(0, END)