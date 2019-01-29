""" User interface class """
from tkinter import *
from tkinter import messagebox
from typing import List
import tkinter.filedialog as filedialog
from tkinter.scrolledtext import ScrolledText
from social_media_scraper.commons import (prepare_database,
                                          prepare_driver,
                                          dispose_resources,
                                          read_input)
from social_media_scraper.logging import (LogObserver,
                                          run_concurrently,
                                          prepare_pool_scheduler,
                                          write_window)
from social_media_scraper.person import process_person
from social_media_scraper.twitter.compose import process_twitter
from social_media_scraper.xing.compose import process_xing
from social_media_scraper.linked_in.compose import process_linked_in
from social_media_scraper.login import Credentials

class Window(Frame):
    """ GUI class """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
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
        self.pack(fill=BOTH, expand=True)
        self.init_choose_input_file()
        self.init_choose_output_directory()
        self.init_output_file_name_input()
        self.init_linkedin_credentials()
        self.init_xing_credentials()
        self.init_debug_menu()
        self.init_footer_buttons()

    def init_choose_input_file(self):
        """ Initializes input file choosing dialogue """
        self.inputButton = Button(self, text="Choose", command=self.choose_input_file)
        self.inputButton.grid(column=0, row=0)
        self.inputFileNameLabel = Label(self, text="Choose input file...")
        self.inputFileNameLabel.grid(column=1, row=0, columnspan=3)

    def init_choose_output_directory(self):
        """ Initializes output directory choosing dialogue """
        self.outputDirectoryButton = Button(self, text="Choose", command=self.choose_output_directory)
        self.outputDirectoryButton.grid(column=0, row=1)
        self.outputDirectoryNameLabel = Label(self, text="Choose output directory...")
        self.outputDirectoryNameLabel.grid(column=1, row=1, columnspan=3)

    def init_output_file_name_input(self):
        """ Initializes output file name input """
        self.outputFileNameLabel = Label(self, text="Output file Name")
        self.outputFileNameLabel.grid(column=0, row=2)
        self.outputFileName = Entry(self, width=35)
        self.outputFileName.grid(column=1, row=2)

    def init_linkedin_credentials(self):
        """ Initializes linkedin input credentials form """
        self.linkedInCredentialsLabel = Label(self, text="LinkedIn credentials")
        self.linkedInCredentialsLabel.grid(column=0, row=3)
        self.linkedInUsernameLabel = Label(self, text="Username")
        self.linkedInUsernameLabel.grid(column=0, row=4)
        self.linkedInUsername = Entry(self, width=35)
        self.linkedInUsername.grid(column=1, row=4)
        self.linkedInPasswordLabel = Label(self, text="Password")
        self.linkedInPasswordLabel.grid(column=0, row=5)
        self.linkedInPassword = Entry(self, width=35, show="*")
        self.linkedInPassword.grid(column=1, row=5)

    def init_xing_credentials(self):
        """ Initializes xing input credentials form """
        self.xingCredentialsLabel = Label(self, text="Xing credentials")
        self.xingCredentialsLabel.grid(column=0, row=6)
        self.xingUsernameLabel = Label(self, text="Username")
        self.xingUsernameLabel.grid(column=0, row=7)
        self.xingUsername = Entry(self, width=35)
        self.xingUsername.grid(column=1, row=7)
        self.xingPasswordLabel = Label(self, text="Password")
        self.xingPasswordLabel.grid(column=0, row=8)
        self.xingPassword = Entry(self, width=35, show="*")
        self.xingPassword.grid(column=1, row=8)

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
        if not self.linkedInUsername.get():
            messagebox.showerror("Error", "Please provide LinkedIn username")
            return False
        if not self.linkedInPassword.get():
            messagebox.showerror("Error", "Please provide LinkedIn password")
            return False
        if not self.xingUsername.get():
            messagebox.showerror("Error", "Please provide Xing username")
            return False
        if not self.xingPassword.get():
            messagebox.showerror("Error", "Please provide Xing password")
            return False
        return True

    def get_credentials(self) -> List[Credentials]:
        """ Get credentials from input fields """
        return [
            Credentials(self.linkedInUsername.get(), self.linkedInPassword.get()),
            Credentials(self.xingUsername.get(), self.xingPassword.get())
        ]

    def start_scraping(self):
        """ Start button callback to start scraping information """
        if self.check_startup_errors():
            write_window(self.debugLogField, "Starting scraping...")
            database_path = "{}/{}.db".format(self.outputFileDirectory, self.outputFileName.get())
            self.database = prepare_database(database_path)
            self.driver = prepare_driver(self.showBrowser.get(), self.get_credentials())
            read = read_input(self.inputFileName)
            self.file = read[0]
            scheduler = prepare_pool_scheduler()
            people = process_person(read[1], self.database.scoped_factory)
            twitter = process_twitter(people, self.driver, self.database.scoped_factory)
            linked_in = process_linked_in(twitter, self.driver, self.database.scoped_factory)
            xing = process_xing(linked_in, self.driver, self.database.scoped_factory)
            observer = LogObserver(self.debugLogField, self.database, self.driver, self.file)
            self.running_job = run_concurrently(xing, observer, self.master, scheduler)

    def stop_scraping(self):
        """ Stop scraping callback to stop running scraper """
        if self.running_job:
            self.running_job.dispose()
            dispose_resources(self.file, self.driver, self.database.engine)
            self.running_job = None
