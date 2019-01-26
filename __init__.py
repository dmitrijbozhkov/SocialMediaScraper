from tkinter import *

class Window(Frame):
    """ GUI class """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Profile scraper")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text="Quit")
        quitButton.place(x=0, y=0)

if __name__ == "__main__":
    root = Tk()
    root.geometry("400x800")
    app = Window(root)
    root.mainloop()