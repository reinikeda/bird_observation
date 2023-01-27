from tkinter import *
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('sqlite:///../data/birds_observation.db')
c = conn.cursor()

class ObserverList:
    def __init__(self, main):
        self.main = main
        self.main.iconbitmap(r'app/bird.ico')
        self.main.title('BOA: Bird Observation App')
        self.main.config(bg='#e4fafd')
        self.l_title = Label(self.main, text='Observers list from database', bg='#e4fafd')
        self.columns = ('id', 'f_name', 'l_name', 'birth_date', 'gender', 'email')
        self.tree = ttk.Treeview(self.main, columns=self.columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('f_name', text='First name')
        self.tree.heading('l_name', text='Last name')
        self.tree.heading('birth_date', text='Date of birth')
        self.tree.heading('gender', text='Gender')
        self.tree.heading('email', text='Email')
        self.tree.insert('', END, self.read_observers())
        # self.tree_scrollbar = Scrollbar(self.main, command=self.tree.yview)
        # self.tree.config(yscrollcommand=self.tree_scrollbar.set)

        self.b_exit = Button(self.main, text='Exit', bg='#c2e7ec', activebackground='#a4d8df', pady=10, width=20, command=self.main.destroy)

        self.l_title.pack()
        self.tree.pack()
        self.b_exit.pack(pady=10)

    def read_observers(self):
        with conn:
            c.execute('SELECT * FROM observer')
            rows = c.fetchall()
            for row in rows:
                self.tree.insert('', END, values=row)