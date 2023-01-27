from tkinter import *
from app.main import MainApp

def run_main_app():
    window = Tk()
    window.iconbitmap(r'app/bird.ico')
    window.title('BOA: Bird Observation App')
    window.geometry('500x400')
    window.config(bg='#e4fafd')
    app = MainApp(window)
    window.mainloop()

if __name__ == '__main__':
    run_main_app()