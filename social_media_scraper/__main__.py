""" Run program """
from tkinter import Tk
import platform
from social_media_scraper.interface import Window

root = Tk()
pl = platform.system()
if pl == "Linux" or pl == "Darwin":
    root.geometry("400x280")
else:
    root.geometry("460x360")
app = Window(root)
root.mainloop()