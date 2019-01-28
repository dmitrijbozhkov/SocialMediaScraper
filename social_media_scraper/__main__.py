""" Run program """
from tkinter import Tk
from social_media_scraper.interface import Window

root = Tk()
root.geometry("400x350")
app = Window(root)
# app = Window(root, setup_drivers(True))
root.mainloop()