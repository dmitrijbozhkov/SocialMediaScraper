""" User interface class """
from tkinter import *
from tkinter import messagebox
from typing import List
from concurrent.futures import ThreadPoolExecutor
import tkinter.filedialog as filedialog
from tkinter.scrolledtext import ScrolledText
from social_media_scraper.external_resources import (
    read_csv,
    throttle_emissions,
    prepare_browsers,
    database_writer)
from social_media_scraper.account.process_scraping import account_scraper
from social_media_scraper.account.model import Base

INPUT_PLACEHOLDER = "Choose input file name..."
OUTPUT_PLACEHOLDER = "Choose output directory..."

class Window(Frame):
    """ GUI class """

    def __init__(self, master, args):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=True)
        self.show_browser = BooleanVar()
        self.input_file_name = None
        self.output_file_directory = None
        self.running_job = False
        self.database = None
        self.driver = None
        self.file = None
        self.args = args
        self.init_window()

    def init_window(self):
        """ Set up ui layout """
        self.master.title("Profile scraper")
        self.init_choose_input_file()
        self.init_choose_output_directory()
        self.init_output_file_name_input()
        self.init_wait_time()
        self.init_debug_menu()
        self.init_footer_buttons()

    def init_choose_input_file(self):
        """ Initializes input file choosing dialogue """
        self.input_button = Button(self, text="Choose", command=self.choose_input_file)
        self.input_button.grid(column=0, row=0)
        self.input_file_name_label = Entry(self, width=40, disabledforeground="black")
        set_entry(self.input_file_name_label, INPUT_PLACEHOLDER)
        self.input_file_name_label.grid(column=1, row=0, columnspan=3)

    def init_choose_output_directory(self):
        """ Initializes output directory choosing dialogue """
        self.output_directory_button = Button(self, text="Choose", command=self.choose_output_directory)
        self.output_directory_button.grid(column=0, row=1)
        self.output_directory_name_label = Entry(self, width=40, disabledforeground="black")
        set_entry(self.output_directory_name_label, OUTPUT_PLACEHOLDER)
        self.output_directory_name_label.grid(column=1, row=1, columnspan=3)

    def init_output_file_name_input(self):
        """ Initializes output file name input """
        self.output_file_name_label = Label(self, text="Output file Name")
        self.output_file_name_label.grid(column=0, row=2)
        self.output_file_name = Entry(self, width=40)
        self.output_file_name.grid(column=1, row=2)

    def init_wait_time(self):
        """ Initializes fields for setting time between requests """
        self.wait_label = Label(self, text="Time between requests")
        self.wait_label.grid(column=0, row=3, columnspan=4)
        self.wait_min = Entry(self, width=4)
        self.wait_max = Entry(self, width=4)
        Placeholder(self.wait_min, "Min").init_placeholder()
        Placeholder(self.wait_max, "Max").init_placeholder()
        self.wait_min.grid(column=0, row=4)
        self.wait_max.grid(column=1, row=4)

    def init_debug_menu(self):
        """ Initializes show browsers checker and debug log """
        self.show_browser_check = Checkbutton(self, text="show browser", variable=self.show_browser)
        self.show_browser_check.grid(column=0, row=5)
        self.debug_log_label = Label(self, text="Debg log")
        self.debug_log_label.grid(column=0, row=6)
        self.debug_log_field = ScrolledText(self, height=10, width=53)
        self.debug_log_field.grid(column=0, row=7, columnspan=4)
        self.debug_log_field.config(state=DISABLED)

    def init_footer_buttons(self):
        """ Intializes start and stop buttons """
        self.start_button = Button(self, text="Start", command=self.start_scraping)
        self.start_button.grid(column=1, row=8)
        self.stop_button = Button(self, text="Stop", command=self.stop_scraping)
        self.stop_button.grid(column=0, row=8)

    def log_window(self, message: str):
        """ Log message into debug window """
        self.debug_log_field.config(state=NORMAL)
        self.debug_log_field.insert(END, message + "\n")
        self.debug_log_field.config(state=DISABLED)

    def choose_input_file(self):
        """ Choose input file button callback """
        chosen = filedialog.askopenfilename(filetypes=[("Comma Separated Values File", "*.csv")])
        if chosen:
            self.input_file_name = chosen
            set_entry(self.input_file_name_label, self.input_file_name)

    def choose_output_directory(self):
        """ Choose output directory button callback """
        chosen = filedialog.askdirectory()
        if chosen:
            self.output_file_directory = chosen
            set_entry(self.output_directory_name_label, self.output_file_directory)

    def check_startup_errors(self):
        """ Checks for startup errors on startup """
        if not self.input_file_name:
            messagebox.showerror("Error", "Please provide input file name")
            return False
        if not self.output_file_directory:
            messagebox.showerror("Error", "Please provide output file directory")
            return False
        if not self.output_file_name.get():
            messagebox.showerror("Error", "Please provide output file name")
            return False
        try:
            request_min = int(self.wait_min.get())
            request_max = int(self.wait_max.get())
            if request_min > request_max:
                messagebox.showerror("Error", "min value cannot be bigger, than max")
                return False
        except ValueError:
            messagebox.showerror("Error", "Please provide correct min and max time between requests")
            return False
        return True

    def interface_scraping(self):
        """ Scrape accounts with interface """
        database_path = "{}/{}.db".format(self.output_file_directory, self.output_file_name.get())
        executor = ThreadPoolExecutor(3)
        browsers = prepare_browsers(self.show_browser.get(), self.args.geckodriver)
        reader = read_csv(self.input_file_name, True)
        scraper = throttle_emissions(account_scraper(browsers, executor), int(self.wait_min.get()), int(self.wait_max.get()))
        writer = database_writer(database_path, Base, self.args.sql)
        for row in reader:
            if not self.running_job:
                break
            temp = scraper.send(row)
            log_accounts = []
            if temp.twitterAccount:
                log_accounts.append("Twitter account @" + temp.twitterAccount.atName)
            if temp.linkedInAccount:
                log_accounts.append("LinkedIn account " + temp.linkedInAccount.name)
            if temp.xingAccount:
                log_accounts.append("Xing account " + temp.xingAccount.name)
            self.log_window("Wrting account of {} with accounts:\n {}".format(temp.name, ",\n".join(log_accounts)))
            writer.send(temp)
        scraper.close()
        writer.close()
        executor.shutdown()
        browsers.Twitter.quit()
        browsers.LinkedIn.quit()
        browsers.Xing.quit()
        self.log_window("Scraping end")

    def start_scraping(self):
        """ Start button callback to start scraping information """
        if self.check_startup_errors():
            self.log_window("Starting scraping...")
            self.start_button.config(state=DISABLED)
            self.running_job = True
            self.interface_scraping()
            self.running_job = False
            self.start_button.config(state=NORMAL)
            self.log_window("Scraping stopped")

    def stop_scraping(self):
        """ Stop scraping callback to stop running scraper """
        if self.running_job:
            self.log_window("Stopping scraping...")
            self.running_job = False

def set_entry(entry, message):
    """ Appends text to window """
    entry.config(state=NORMAL)
    entry.delete(0, END)
    entry.insert(0, message)
    entry.config(state=DISABLED)

class Placeholder(object):
    """ Adds placeholder to an Entry """

    def __init__(self, entry, placeholder):
        self.entry = entry
        self.placeholder = placeholder
        self.with_placeholder = True

    def on_focusin(self, event):
        """ <FocusIn> event handler """
        if self.with_placeholder:
            self.entry.delete(0, "end")
            self.with_placeholder = False

    def on_focusout(self, event):
        """ <FocusOut> event handler """
        if self.entry.get() == "":
            self.entry.insert(0, self.placeholder)
            self.with_placeholder = True

    def init_placeholder(self):
        """ Binds placeholder events """
        self.entry.insert(0, self.placeholder)
        self.entry.bind("<FocusIn>", self.on_focusin, add="+")
        self.entry.bind("<FocusOut>", self.on_focusout, add="+")
