from tkinter import *
from tkinter import ttk
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

class ObserverList:
    def __init__(self, main):
        self.main = main
        self.main.iconbitmap(r'app/bird.ico')
        self.main.title('BOA: Bird Observation App')
        self.main.config(bg='#e4fafd')
        self.f_top = Frame(self.main, bg='#e4fafd')
        self.l_title = Label(self.f_top, text='Observers list from database', bg='#e4fafd')
        self.columns = ('id', 'f_name', 'l_name', 'birth_date', 'gender', 'email')
        self.tree = ttk.Treeview(self.f_top, columns=self.columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.column('id', width=50)
        self.tree.heading('f_name', text='First name')
        self.tree.heading('l_name', text='Last name')
        self.tree.heading('birth_date', text='Date of birth')
        self.tree.heading('gender', text='Gender')
        self.tree.heading('email', text='Email')
        self.tree.insert('', END, self.read_observers())
        self.tree_scrollbar = Scrollbar(self.f_top, command=self.tree.yview)
        self.tree.config(yscrollcommand=self.tree_scrollbar.set)

        self.f_input = Frame(self.main, bg='#e4fafd')
        self.l_add = Label(self.f_input, text='Edit observer list', bg='#e4fafd')
        self.l_f_name = Label(self.f_input, text='First name', bg='#e4fafd')
        self.e_f_name = Entry(self.f_input)
        self.l_l_name = Label(self.f_input, text='Last name', bg='#e4fafd')
        self.e_l_name = Entry(self.f_input)
        self.l_birth_date = Label(self.f_input, text='Birth date', bg='#e4fafd')
        self.e_birth_date = Entry(self.f_input)
        self.l_gender = Label(self.f_input, text='Gender', bg='#e4fafd')
        self.gender = ttk.Combobox(self.f_input, state='readonly', values=('female', 'male'))
        self.l_email = Label(self.f_input, text='Email', bg='#e4fafd')
        self.e_email = Entry(self.f_input)
        self.b_add = MyButton(self.f_input, text='Add', command=self.add_new)
        self.b_delete = MyButton(self.f_input, text='Delete selected', command=self.delete_row)
        self.b_exit = MyButton(self.f_input, text='Exit', bg='#c2e7ec', activebackground='#a4d8df', pady=10, width=20, command=self.main.destroy)

        self.f_top.pack()
        self.l_title.grid(row=0, column=0, columnspan=2)
        self.tree.grid(row=1, column=0)
        self.tree_scrollbar.grid(row=1, column=1, sticky=NS)
        self.f_input.pack()
        self.l_add.grid(row=0, column=0, columnspan=7, padx=5)
        self.l_f_name.grid(row=1, column=0, padx=5)
        self.e_f_name.grid(row=2, column=0, padx=5)
        self.l_l_name.grid(row=1, column=1, padx=5)
        self.e_l_name.grid(row=2, column=1, padx=5)
        self.l_birth_date.grid(row=1, column=2, padx=5)
        self.e_birth_date.grid(row=2, column=2, padx=5)
        self.l_gender.grid(row=1, column=3, padx=5)
        self.gender.grid(row=2, column=3, padx=5)
        self.l_email.grid(row=1, column=4, padx=5)
        self.e_email.grid(row=2, column=4, padx=5)
        self.b_add.grid(row=2, column=5, padx=5)
        self.b_delete.grid(row=2, column=6, padx=5)
        self.b_exit.grid(row=3, column=6, padx=5, pady=10)

    def read_observers(self):
        self.tree.delete(*self.tree.get_children())
        with conn:
            c.execute('SELECT * FROM observer')
            rows = c.fetchall()
            for row in rows:
                self.tree.insert('', END, values=row)

    def clear(self):
        self.e_f_name.delete(0, END)
        self.e_l_name.delete(0, END)
        self.e_birth_date.delete(0, END)
        self.gender.set('')
        self.e_email.delete(0, END)

    def add_new(self):
        add_new_observer(self.e_f_name.get(), self.e_l_name.get(), self.e_birth_date.get(), self.gender.get(), self.e_email.get())
        self.read_observers()
        self.clear()

    def delete_row(self):
        self.selected_row = self.tree.focus()
        self.row_id = int((self.tree.item(self.selected_row, 'values'))[0])
        c.execute('DELETE FROM observer WHERE id=?', (self.row_id,))
        conn.commit()
        self.read_observers()