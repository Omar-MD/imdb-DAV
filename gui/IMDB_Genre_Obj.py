import io
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from IMDB.gui.IMDB_Msg_Obj import IMDBMsg
from IMDB.analysis import movie_analysis
from IMDB.analysis.summary_analsis import genre_summary, genre_specific
from IMDB.visualisation.imdb_visuals import plot_genre_count_vs_year, plot_genre_avg_vs_year


class IMDBGenreTab(ttk.Frame):
    def __init__(self, parent, logger, imdb_data):
        ttk.Frame.__init__(self, parent)
        self.title = "IMDB Movie Analysis"
        self.logger = logger
        self.imdb_data = imdb_data

        self.selected_genre = None

    def create_widgets(self):
        movies_df = self.imdb_data.merged_movies
        label_genre_heading = ttk.Label(self, text="IMDB Genre Analysis")
        label_genre_heading.grid(row=0, column=0, columnspan=2, rowspan=1, sticky="nswe", padx=5, pady=5)

        # Genre Label & Combobox
        label_genre_name = ttk.Label(self, text="Select Genre:")
        self.selected_genre = tk.StringVar()
        genre_names = movie_analysis.get_genres_list(movies_df)
        combo_genre = ttk.Combobox(self, textvariable=self.selected_genre, values=genre_names, state='readonly')
        combo_genre.set('drama')
        label_genre_name.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        combo_genre.grid(row=1, column=1, pady=5, padx=5, sticky="nswe")

        # Genre Summary & Movie Actors
        label_summary = ttk.Label(self, text="Summary:")
        summary_button = tk.Button(self, text="All Genre Summary", command=self.overall_genre_summary)
        label_summary.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        summary_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")

        label_genre = ttk.Label(self, text="Genre:")
        genre_summary_button = tk.Button(self, text="Genre Summary", command=self.genre_summary)
        genre_count_button = tk.Button(self, text="Genre Count vs Year", command=self.plot_genre_count_year)
        genre_rank_button = tk.Button(self, text="Genre Rank vs Year", command=self.plot_genre_rank_year)
        label_genre.grid(row=4, column=0, pady=5, padx=5, sticky="w")
        genre_summary_button.grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")
        genre_count_button.grid(row=6, column=0, pady=5, padx=5, sticky="nswe")
        genre_rank_button.grid(row=6, column=1, pady=5, padx=5, sticky="nswe")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)


    def overall_genre_summary(self):
        movies_df = self.imdb_data.merged_movies

        log_buffer = io.StringIO()

        genre_summary(movies_df, logger=log_buffer)

        genre_summary_info = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(genre_summary_info)

        IMDBMsg.show_imdb_msg(self, "Genre Summary", genre_summary_info)

    def genre_summary(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors
        genre = self.selected_genre.get()

        log_buffer = io.StringIO()

        genre_specific(movies_df, actors_df, genre, logger=log_buffer)

        genre_info = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(genre_info)

        IMDBMsg.show_imdb_msg(self, f"{genre} Summary", genre_info)


    def plot_genre_count_year(self):
        movies_df = self.imdb_data.merged_movies
        genre = self.selected_genre.get()

        new_window = tk.Toplevel(self)
        new_window.title("Genre Count vs Year")

        figure = plot_genre_count_vs_year(movies_df, genre, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()


    def plot_genre_rank_year(self):
        movies_df = self.imdb_data.merged_movies
        genre = self.selected_genre.get()

        new_window = tk.Toplevel(self)
        new_window.title("Genre Rank vs Year")

        figure = plot_genre_avg_vs_year(movies_df, genre, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
