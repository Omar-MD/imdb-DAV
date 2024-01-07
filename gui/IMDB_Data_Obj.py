import tkinter as tk
from tkinter import ttk

from IMDB.data.IMDB_Database_Obj import IMDBConnection

# Constants
IMDB_PARAMETERS = {
    'host': "relational.fit.cvut.cz",
    'user': "guest",
    'password': "relational",
    'port': 3306,
    'database': "imdb_ijs"
}


class IMDBDataTab(ttk.Frame):
    def __init__(self, parent, logger):
        ttk.Frame.__init__(self, parent)
        self.title = "IMDB Data Preparation"
        self.logger = logger
        self.imdb_db = IMDBConnection(IMDB_PARAMETERS.values(), client=self, logger=self.logger)
        self.ready = False

    def create_widgets(self):
        # Heading
        label_app_heading = tk.Label(self, text="IMDB Data Preparation")
        label_app_heading.grid(row=0, column=0, columnspan=2, sticky="nswe", padx=5, pady=5)

        # Data Fetching
        label_data = tk.Label(self, text="Data Fetch:")
        label_data.grid(row=1, column=0, sticky="nswe", padx=5, pady=5)
        load_data_button = tk.Button(self, text="Load Data", command=self.imdb_db.load_df)
        fetch_data_button = tk.Button(self, text="Fetch Data", command=self.imdb_db.fetch_df)
        clean_data_button = tk.Button(self, text="Clean Data", command=self.imdb_db.clean_df)
        load_data_button.grid(row=2, column=0, pady=5, padx=5, sticky="nswe")
        fetch_data_button.grid(row=3, column=0, pady=5, padx=5, sticky="nswe")
        clean_data_button.grid(row=4, column=0, pady=5, padx=5, sticky="nswe")

        # EDA
        label_eda = tk.Label(self, text="Exploratory Data Analysis:")
        label_eda.grid(row=1, column=1, sticky="nswe", padx=5, pady=5)

        tables_eda_button = tk.Button(self, text="Table", command=self.imdb_db.table_EDA)
        movies_eda_button = tk.Button(self, text="Merged Movies", command=self.imdb_db.movies_EDA)
        actors_eda_button = tk.Button(self, text="Merged Actors", command=self.imdb_db.actors_EDA)
        tables_eda_button.grid(row=2, column=1, pady=5, padx=5, sticky="nswe")
        movies_eda_button.grid(row=3, column=1, pady=5, padx=5, sticky="nswe")
        actors_eda_button.grid(row=4, column=1, pady=5, padx=5, sticky="nswe")

        # Spacer row
        spacer_label = tk.Label(self, text="")
        spacer_label.grid(row=5, column=0, columnspan=2, pady=5, padx=5)

        # Configure row and column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
