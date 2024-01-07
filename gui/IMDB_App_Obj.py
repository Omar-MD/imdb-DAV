import tkinter as tk
from tkinter import ttk, filedialog

from IMDB.gui.IMDB_Analysis_Child_Obj import IMDBAnalyzerChild
from IMDB.gui.IMDB_Msg_Obj import IMDBMsg
from IMDB.gui.SplashScreen import Splash
from IMDB.gui.IMDB_Data_Obj import IMDBDataTab


class IMDBAnalyzer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)  # Initialize superclass
        self.title("IMDB Data")
        self.geometry("600x500")
        self.resizable(False, False)

        self.child_frame = IMDBAnalyzerChild(self)
        self.child_frame.withdraw()
        self.logger = None
        self.data_tab = None

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")

        analysis_button = tk.Button(self, text="IMDB Analysis", command=self.show_analysis)
        analysis_button.pack(expand=0, fill="both")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # self.create_splash_screen()
        self.create_data_tabs()

    def show_analysis(self):
        if not self.child_frame.instantiated:
            if self.data_tab.ready:
                self.child_frame.create_imdb_tabs(self.data_tab.imdb_db)
                self.child_frame.instantiated = True
                self.child_frame.show()
                self.withdraw()
            else:
                IMDBMsg.show_imdb_msg(self, "INFO message",
                                      "Data not ready ! Fetch OR Load it")
        else:
            self.child_frame.show()
            self.withdraw()

    def show(self):
        self.update()
        self.deiconify()

    # def create_splash_screen(self):
    #     Splash(self, timeout=3000, image="splash.png")

    def create_data_tabs(self):
        # App Logs
        logs_tab = ttk.Frame(self.notebook)
        self.create_logs_widgets(logs_tab)
        self.notebook.add(logs_tab, text='Logs')

        # IMDB Data Preparation
        self.data_tab = IMDBDataTab(self.notebook, logger=self)
        self.data_tab.create_widgets()
        self.notebook.add(self.data_tab, text='Data')

    def create_logs_widgets(self, parent):
        # Heading
        label_log_heading = tk.Label(parent, text="IMDB Analyzer Logs")
        label_log_heading.grid(row=0, column=0, columnspan=2, rowspan=1, sticky="nswe", padx=5, pady=5)

        # Buttons
        clear_logs_button = tk.Button(parent, text="Clear Logs", command=self.clear_logs)
        save_csv_button = tk.Button(parent, text="Save Logs", command=self.save_logs)
        clear_logs_button.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")
        save_csv_button.grid(row=1, column=1, pady=5, padx=5, sticky="nswe")

        # Output log
        log_paned = ttk.PanedWindow(parent, orient=tk.VERTICAL)
        self.logger = tk.Text(log_paned, state="disabled", wrap="none", width=100)
        log_paned.add(self.logger)
        log_paned.grid(row=2, column=0, columnspan=2, sticky="nswe")

        # Configure row and column weights
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(0, weight=0)
        parent.rowconfigure(1, weight=0)
        parent.rowconfigure(2, weight=1)

    def write(self, text):
        self.logger.configure(state=tk.NORMAL)
        if self.logger.index('end-1c') != '1.0':
            self.logger.insert('end', '\n')
        self.logger.insert(tk.END, text)
        self.logger.yview(tk.END)
        self.logger.see('end')
        self.logger.configure(state=tk.DISABLED)

    def clear_logs(self):
        self.logger.configure(state=tk.NORMAL)
        self.logger.delete('1.0', tk.END)
        self.logger.configure(state=tk.DISABLED)

    def save_logs(self):
        logs_content = self.logger.get('1.0', tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, 'w') as file:
                file.write(logs_content)
