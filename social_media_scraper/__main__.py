""" Run program """
from tkinter import Tk
from social_media_scraper.interface import Window

root = Tk()
root.geometry("450x300")
app = Window(root)
root.mainloop()
