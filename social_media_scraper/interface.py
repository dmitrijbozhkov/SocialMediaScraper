""" User interface class """
from tkinter import *
from tkinter import messagebox
from typing import List
import tkinter.filedialog as filedialog
from tkinter.scrolledtext import ScrolledText
from social_media_scraper.job_manager import DatabaseManager
from social_media_scraper.logging import write_window

class Window(Frame):
    """ GUI class """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=True)
        self.showBrowser = BooleanVar()
        self.inputFileName = None
        self.outputFileDirectory = None
        self.running_job = None
        self.database = None
        self.driver = None
        self.file = None
        self.init_window()

    def init_window(self):
        """ Set up ui layout """
        self.master.title("Profile scraper")
        self.init_choose_input_file()
        self.init_choose_output_directory()
        self.init_output_file_name_input()
        self.init_debug_menu()
        self.init_footer_buttons()

    def init_choose_input_file(self):
        """ Initializes input file choosing dialogue """
        self.inputButton = Button(self, text="Choose", command=self.choose_input_file)
        self.inputButton.grid(column=0, row=0)
        self.inputFileNameLabel = Entry(self, text="Choose input file...")
        self.inputFileNameLabel.grid(column=1, row=0, columnspan=3)

    def init_choose_output_directory(self):
        """ Initializes output directory choosing dialogue """
        self.outputDirectoryButton = Button(self, text="Choose", command=self.choose_output_directory)
        self.outputDirectoryButton.grid(column=0, row=1)
        self.outputDirectoryNameLabel = Entry(self, text="Choose output directory...")
        self.outputDirectoryNameLabel.grid(column=1, row=1, columnspan=3)

    def init_output_file_name_input(self):
        """ Initializes output file name input """
        self.outputFileNameLabel = Label(self, text="Output file Name")
        self.outputFileNameLabel.grid(column=0, row=2)
        self.outputFileName = Entry(self, width=35)
        self.outputFileName.grid(column=1, row=2)

    def init_debug_menu(self):
        """ Initializes show browsers checker and debug log """
        self.showBrowserCheck = Checkbutton(self, text="show browser", variable=self.showBrowser)
        self.showBrowserCheck.grid(column=0, row=9)
        self.debugLogLabel = Label(self, text="Debg log")
        self.debugLogLabel.grid(column=0, row=10)
        self.debugLogField = ScrolledText(self, height=10, width=53)
        self.debugLogField.grid(column=0, row=11, columnspan=4)
        self.debugLogField.config(state=DISABLED)

    def init_footer_buttons(self):
        """ Intializes start and stop buttons """
        self.startButton = Button(self, text="Start", command=self.start_scraping)
        self.startButton.grid(column=1, row=12)
        self.stopButton = Button(self, text="Stop", command=self.stop_scraping)
        self.stopButton.grid(column=0, row=12)

    def choose_input_file(self):
        """ Choose input file button callback """
        chosen = filedialog.askopenfilename(filetypes=[("Comma Separated Values File","*.csv")])
        if chosen:
            self.inputFileName = chosen
            self.inputFileNameLabel.config(text=self.inputFileName)

    def choose_output_directory(self):
        """ Choose output directory button callback """
        chosen = filedialog.askdirectory()
        if chosen:
            self.outputFileDirectory = chosen
            self.outputDirectoryNameLabel.config(text=self.outputFileDirectory)
 
    def check_startup_errors(self):
        """ Checks for startup errors on startup """
        if not self.inputFileName:
            messagebox.showerror("Error", "Please provide input file name")
            return False
        if not self.outputFileDirectory:
            messagebox.showerror("Error", "Please provide output file directory")
            return False
        if not self.outputFileName.get():
            messagebox.showerror("Error", "Please provide output file name")
            return False
        return True

    def start_scraping(self):
        """ Start button callback to start scraping information """
        if self.check_startup_errors():
            write_window(self.debugLogField, "Starting scraping...")
            database_path = "{}/{}.db".format(self.outputFileDirectory, self.outputFileName.get())
            job = DatabaseManager()
            self.running_job = job.init_database(database_path) \
                .init_drivers(self.showBrowser.get()) \
                .init_schedulers(self.master) \
                .process_person(self.inputFileName) \
                .compose_streams(1, 3) \
                .init_job(self.debugLogField) \
                .start_scraping()

    def stop_scraping(self):
        """ Stop scraping callback to stop running scraper """
        if self.running_job:
            self.running_job.stop_scraping()
            self.running_job = None
