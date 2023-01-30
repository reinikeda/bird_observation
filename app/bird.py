from tkinter import *
from tkinter import ttk
from create_db import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data/birds_observation.db')
session = sessionmaker(bind=engine)()


class BirdList:
    def __init__ (self, main):
        self.main = main
        self.main.iconbitmap(r'app/bird.ico')
        self.main.title('BOA: Bird Observation App')
        self.main.config(bg='#e4fafd')
        self.l_title = Label(self.main, text='Bird list from database', bg='#e4fafd')
        self.columns = ('id', 'species_lt', 'species_en', 'species_latin')
        self.tree = ttk.Treeview(self.main, columns=self.columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.column('id', width=50)
        self.tree.heading('species_lt', text='Species name in LT')
        self.tree.heading('species_en', text='Species name in EN')
        self.tree.heading('species_latin', text='Species name in latin')
        self.tree.insert('', END, self.read_birds())
        self.tree_scrollbar = Scrollbar(self.main, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.tree_scrollbar.set)

        self.b_exit = Button(self.main, text='Exit', bg='#c2e7ec', activebackground='#a4d8df', pady=10, width=20, command=self.main.destroy)

        self.l_title.grid(row=0, column=0, columnspan=2)
        self.tree.grid(row=1, column=0)
        self.tree_scrollbar.grid(row=1, column=1, sticky=NS)
        self.b_exit.grid(row=2, column=0, columnspan=2, pady=10)

    def read_birds(self):
        self.birds = session.query(Bird).all()
        for row in self.birds:
            self.tree.insert('', END, values=(row.id, row.species_lt, row.species_en, row.species_latin))