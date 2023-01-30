from tkinter import *
from tkinter import ttk
from create_db import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3

conn = sqlite3.connect('sqlite:///../data/birds_observation.db')
c = conn.cursor()

engine = create_engine('sqlite:///data/birds_observation.db')
session = sessionmaker(bind=engine)()


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
        self.tree.column('id', width=50)
        self.tree.heading('observer_id', text='Observer')
        self.tree.heading('bird_id', text='Bird')
        self.tree.heading('number', text='Number of birds')
        self.tree.heading('place', text='Place')
        self.tree.heading('date', text='Date')
        self.tree.insert('', END, self.read_observations())
        self.tree_scrollbar = Scrollbar(self.f_top, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.tree_scrollbar.set)

        self.f_insert = Frame(self.main, bg='#e4fafd')
        self.l_add = Label(self.f_insert, text='Add new observation', bg='#e4fafd')
        self.l_observer = Label(self.f_insert, text='Choose observer', bg='#e4fafd')
        self.observer = ttk.Combobox(self.f_insert, state='readonly', values=self.read_observers())
        self.l_bird = Label(self.f_insert, text='Choose bird', bg='#e4fafd')
        self.bird = ttk.Combobox(self.f_insert, state='readonly', values=self.read_birds())
        self.l_number = Label(self.f_insert, text='Enter count', bg='#e4fafd')
        self.e_number = Entry(self.f_insert)
        self.l_place = Label(self.f_insert, text='Choose place', bg='#e4fafd')
        self.place = ttk.Combobox(self.f_insert, state='readonly', values=self.read_places())
        self.l_date = Label(self.f_insert, text='Enter date', bg='#e4fafd')
        self.e_date = Entry(self.f_insert)
        self.b_add = MyButton(self.f_insert, text='Add to database', command=self.add_new)
        self.b_delete = MyButton(self.f_insert, text='Delete selected', command=self.delete_row)

        self.f_search = Frame(self.main, bg='#e4fafd')
        self.l_search = Label(self.f_search, text='Search', bg='#e4fafd')
        self.e_search = Entry(self.f_search)
        self.b_search = MyButton(self.f_search, text='Search', command=self.search)
        self.b_all = MyButton(self.f_search, text='Show all', command=self.read_observations)
        self.b_exit = MyButton(self.f_search, text='Exit', command=self.main.destroy)

        self.f_top.pack()
        self.l_title.pack()
        self.tree.pack(side=LEFT)
        self.tree_scrollbar.pack(side=RIGHT, fill=Y)

        self.f_insert.pack()
        self.l_add.grid(row=0, column=0, columnspan=8, padx=5)
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
        self.b_delete.grid(row=2, column=6, padx=5)

        self.f_search.pack(side=RIGHT, padx=10)
        self.l_search.grid(row=0, column=0, padx=5)
        self.e_search.grid(row=1, column=0, padx=5)
        self.b_search.grid(row=1, column=1, padx=5)
        self.b_all.grid(row=1, column=2, padx=5)
        self.b_exit.grid(row=2, column=2, padx=5, pady=10)

    def read_observations(self):
        self.tree.delete(*self.tree.get_children())
        with conn:
            c.execute('SELECT bird_observation.id, observer.f_name || " " || observer.l_name as observer_name, bird.species_lt, bird_observation.number, place.place, bird_observation.date FROM bird_observation JOIN observer ON observer_id = observer.id JOIN bird ON bird_id = bird.id JOIN place ON place_id = place.id;')
            rows = c.fetchall()
            for row in rows:
                self.tree.insert('', END, values=row)

    def read_observers(self):
        observers = session.query(Observer).all()
        observer_list = []
        for row in observers:
            observer_list.append(str(row.id) + ': ' + row.f_name + ' ' + row.l_name)
        return observer_list

    def read_birds(self):
        birds = session.query(Bird).all()
        bird_list = []
        for row in birds:
            bird_list.append(str(row.id) + ': ' + row.species_lt)
        return bird_list

    def read_places(self):
        places = session.query(Place).all()
        places_list = []
        for row in places:
            places_list.append(str(row.id) + ': ' + row.place)
        return places_list

    def clear(self):
        self.observer.set('')
        self.bird.set('')
        self.e_number.delete(0, END)
        self.place.set('')
        self.e_date.delete(0, END)
        self.e_search.delete(0, END)

    def add_new(self):
        self.new_observation = BirdObservation(int(self.observer.get()[0]), int(self.bird.get()[0]), int(self.e_number.get()), int(self.place.get()[0]), self.e_date.get())
        session.add(self.new_observation)
        session.commit()
        self.read_observations()
        self.clear()

    def delete_row(self):
        self.selected_row = self.tree.focus()
        self.row_id = int((self.tree.item(self.selected_row, 'values'))[0])
        self.delete = session.query(BirdObservation).get(self.row_id)
        session.delete(self.delete)
        session.commit()
        self.tree.delete(*self.tree.get_children())
        self.read_observations()

    def search(self):
        for rows in self.tree.get_children():
            self.tree.delete(rows)
        self.search_all = self.e_search.get()
        self.search_all = f'%{self.search_all}%'
        with conn:
            c.execute('SELECT bird_observation.id, observer.f_name || " " || observer.l_name as observer_name, bird.species_lt, bird_observation.number, place.place, bird_observation.date FROM bird_observation JOIN observer ON observer_id = observer.id JOIN bird ON bird_id = bird.id JOIN place ON place_id = place.id WHERE observer.f_name LIKE ? OR observer.l_name LIKE ? OR bird.species_lt LIKE ? OR place.place LIKE ? ', (self.search_all, self.search_all, self.search_all, self.search_all,))
            rows = c.fetchall()
            for row in rows:
                self.tree.insert('', END, values=row)
        self.clear()