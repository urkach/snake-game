from tkinter import *
from juego import gameLoop

BACKGROUND_COLOR = "#ffffff"
window = Tk()
window.title("Juego de la serpiente")

label = Label(window, text="¡Juego de la serpiente!")
label.config(font=("Verdana", 24))
label.pack()

botonplay = Button(text="PLAY", height=10, width=20, command=gameLoop)
botonplay.place(relx=0.5, rely=0.5, anchor='center')

botontienda = Button(text="TIENDA", height=10, width=20)
botontienda.place(relx=0.5, rely=0.25, anchor='center')

botonconfig = Button(text="CONFIGURACION", height=10, width=20)
botonconfig.place(relx=0.5, rely=0.75, anchor='center')

width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))
window.mainloop()
