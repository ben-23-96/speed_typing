from tkinter import Tk
from gui import SpeedTypeGui
import database

window = Tk()

gui = SpeedTypeGui(window)

gui.load_gui()

window.mainloop()
