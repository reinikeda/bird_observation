from tkinter import *
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('sqlite:///../data/birds_observation.db')
c = conn.cursor()


class BirdList:
    def __init__ (self, main):
        self.main = main
        self.main.iconbitmap(r'app/bird.ico')
        self.main.title('BOA: Bird Observation App')
        self.main.config(bg='#e4fafd')
        self.l_title = Label(self.main, text='Bird list from database', bg='#e4fafd')
        self.columns = ('id', 'species_lt', 'species_en', 'species_latin', 'status_id')
        self.tree = ttk.Treeview(self.main, columns=self.columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('species_lt', text='Species name in LT')
        self.tree.heading('species_en', text='Species name in EN')
        self.tree.heading('species_latin', text='Species name in latin')
        self.tree.heading('status_id', text='Bird status')
        self.tree.insert('', END, self.read_birds())
        # self.tree_scrollbar = Scrollbar(self.main, command=self.tree.yview)
        # self.tree.config(yscrollcommand=self.tree_scrollbar.set)

        self.b_exit = Button(self.main, text='Exit', bg='#c2e7ec', activebackground='#a4d8df', pady=10, width=20, command=self.main.destroy)

        self.l_title.pack()
        self.tree.pack()
        self.b_exit.pack(pady=10)

    def read_birds(self):
        with conn:
            c.execute('SELECT * FROM bird')
            rows = c.fetchall()
            for row in rows:
                self.tree.insert('', END, values=row)