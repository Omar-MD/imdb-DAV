import tkinter as tk
from tkinter import ttk

from IMDB.gui.IMDB_Actor_Obj import IMDBActorTab
from IMDB.gui.IMDB_Corr_Obj import IMDBCorrTab
from IMDB.gui.IMDB_Genre_Obj import IMDBGenreTab
from IMDB.gui.IMDB_Movie_Obj import IMDBMovieTab
from IMDB.gui.IMDB_Summary_Obj import IMDBSummaryTab


class IMDBAnalyzerChild(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.root = root
        self.protocol('WM_DELETE_WINDOW', self.OverrideWindow)
        self.title("IMDB Analysis")
        self.geometry("600x500")

        self.instantiated = False

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")

        switch_frame = tk.Button(self, text="IMDB Data", command=self.show_data)
        switch_frame.pack(expand=0, fill="both")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def show_data(self):
        self.root.show()
        self.withdraw()

    def show(self):
        self.update()
        self.deiconify()

    def OverrideWindow(self):
        self.withdraw()
        self.root.show()


    def create_imdb_tabs(self, imdb_data):
        # IMDB Summary Analyis
        summary_tab = IMDBSummaryTab(self.notebook, logger=self.root, imdb_data=imdb_data)
        summary_tab.create_widgets()
        self.notebook.add(summary_tab, text='Summary')

        # IMDB Movie Analyis
        movie_tab = IMDBMovieTab(self.notebook, logger=self.root, imdb_data=imdb_data)
        movie_tab.create_widgets()
        self.notebook.add(movie_tab, text='Movie')

        # IMDB Genre Analyis
        genre_tab = IMDBGenreTab(self.notebook, logger=self.root, imdb_data=imdb_data)
        genre_tab.create_widgets()
        self.notebook.add(genre_tab, text='Genre')

        # IMDB Actor Analyis
        actor_tab = IMDBActorTab(self.notebook, logger=self.root, imdb_data=imdb_data)
        actor_tab.create_widgets()
        self.notebook.add(actor_tab, text='Actor')

        # IMDB Correlation Analyis
        corr_tab = IMDBCorrTab(self.notebook, logger=self.root, imdb_data=imdb_data)
        corr_tab.create_widgets()
        self.notebook.add(corr_tab, text='Correlation')
