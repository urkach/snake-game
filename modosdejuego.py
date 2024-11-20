    # MENU DE LOS MODOS DE JUEGO
from tkinter import *
from modo_obstaculos import gameLoop

def modos_de_juego():    

    BACKGROUND_COLOR = "#ffffff"
    window = Tk()
    window.title("Modos de juego")

    label = Label(window, text="Modos de juego")
    label.config(font=("Verdana", 24))
    label.pack()

    botonplay = Button(text="Modo sin obstaculos", height=10, width=20)
    botonplay.place(relx=0.5, rely=0.5, anchor='center')

    botontienda = Button(text="Modo con obstaculos", height=10, width=20, command=gameLoop)
    botontienda.place(relx=0.5, rely=0.25, anchor='center')

    botonconfig = Button(text="Multijugador", height=10, width=20)
    botonconfig.place(relx=0.5, rely=0.75, anchor='center')

    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))
