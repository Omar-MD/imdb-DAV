import io
import tkinter as tk
import pandas as pd
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import IMDB.analysis.movie_analysis as movie_analysis
import IMDB.visualisation.imdb_visuals as imdb_visuals
from IMDB.gui.IMDB_Msg_Obj import IMDBMsg
from IMDB.analysis.summary_analsis import summary_statistics


class IMDBSummaryTab(ttk.Frame):
    def __init__(self, parent, logger, imdb_data):
        ttk.Frame.__init__(self, parent)
        self.title = "IMDB Summary Analysis"
        self.logger = logger
        self.imdb_data = imdb_data

        self.selected_year = None


    def create_widgets(self):
        # Heading
        label_summary_heading = ttk.Label(self, text="IMDB Summary")
        label_summary_heading.grid(row=0, column=0, columnspan=2, rowspan=1, sticky="nswe", padx=5, pady=5)

        # Select Year Label and Combobox
        label_year = ttk.Label(self, text="Select Year:")
        years = ['All'] + movie_analysis.get_movie_years(self.imdb_data.merged_movies)
        self.selected_year = tk.StringVar()
        combo_year = ttk.Combobox(self, textvariable=self.selected_year, values=years, state='readonly')
        combo_year.set('All')
        label_year.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        combo_year.grid(row=1, column=1, pady=5, padx=5, sticky="we")

        summary_button = tk.Button(self, text="Generate Summary", command=self.generate_summary)
        summary_button.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")


        label_movie = ttk.Label(self, text="Movie:")
        movie_count_button = tk.Button(self, text="Movie Count vs Year", command=self.plot_movie_count_vs_year)
        movie_fine_button = tk.Button(self, text="Movie Rank vs Avg (Fine)", command=lambda: self.plot_movie_rank(True))
        movie_broad_button = tk.Button(self, text="Movie Count vs Avg (Broad)",
                                       command=lambda: self.plot_movie_rank(False))
        label_movie.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        movie_count_button.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")
        movie_broad_button.grid(row=5, column=0, pady=5, padx=5, sticky="nswe")
        movie_fine_button.grid(row=5, column=1, pady=5, padx=5, sticky="nswe")


        label_actor = ttk.Label(self, text="Actor:")
        genre_distribution_button = tk.Button(self, text="Genre Distribution", command=self.plot_genre_distribution)
        gender_distribution_button = tk.Button(self, text="Gender Distribution", command=self.plot_gender_distribution)
        label_actor.grid(row=6, column=0, pady=5, padx=5, sticky="w")
        genre_distribution_button.grid(row=7, column=0, pady=5, padx=5, sticky="nswe")
        gender_distribution_button.grid(row=7, column=1, pady=5, padx=5, sticky="nswe")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)


    def generate_summary(self):
        year = self.selected_year.get()
        log_buffer = io.StringIO()

        if year == 'All':
            summary_statistics(self.imdb_data.merged_movies, self.imdb_data.merged_actors, logger=log_buffer)
        else:
            int_year = int(year)
            summary_statistics(self.imdb_data.merged_movies, self.imdb_data.merged_actors,
                               year=int_year, logger=log_buffer)

        summary_info = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(summary_info)

        IMDBMsg.show_imdb_msg(self, "Summary Statistics", summary_info)

    def plot_movie_count_vs_year(self):
        year = self.selected_year.get()
        movies_df = self.imdb_data.merged_movies

        if year != 'All':
            int_year = int(year)
            movies_df = movies_df[movies_df['movie_year'] == int_year]
            movie_count = len(movies_df['movie_id'].unique())

            IMDBMsg.show_imdb_msg(self, f"Movie Count for year:{year}",
                                  f"Movies released in {year}: {movie_count}")
        else:
            new_window = tk.Toplevel(self)
            new_window.title("Movie Count vs Year")

            figure = imdb_visuals.plot_movie_count_vs_year(movies_df, return_figure=True)

            canvas = FigureCanvasTkAgg(figure, master=new_window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack()

    def plot_movie_rank(self, fine=False):
        year = self.selected_year.get()
        movies_df = self.imdb_data.merged_movies
        new_window = tk.Toplevel(self)

        if year != 'All':
            int_year = int(year)
            movies_df = movies_df[movies_df['movie_year'] == int_year]
            new_window.title(f"Movie Rank Binning Year:{year}")
            figure = movie_analysis.movie_rank_binning(movies_df, f"Movie Rank Year:{year}",
                                                       fine=fine, return_figure=True)
        else:
            new_window.title("Movie Rank Binning")
            figure = movie_analysis.movie_rank_binning(movies_df, f"Movie Rank",
                                                       fine=fine, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def plot_genre_distribution(self):
        year = self.selected_year.get()
        movies_df = self.imdb_data.merged_movies

        new_window = tk.Toplevel(self)

        if year != 'All':
            int_year = int(year)
            movies_df = movies_df[movies_df['movie_year'] == int_year]
            new_window.title(f"Genre Distribution year: {year}")
            figure = imdb_visuals.plot_genre_distribution(movies_df, return_figure=True)
        else:
            new_window.title("Genre Distribution")
            figure = imdb_visuals.plot_genre_distribution(movies_df, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def plot_gender_distribution(self):
        year = self.selected_year.get()
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        new_window = tk.Toplevel(self)

        if year != 'All':
            int_year = int(year)
            new_window.title(f"Actor Gender Distribution year: {year}")
            movies_df = movies_df[movies_df['movie_year'] == int_year]
            merged_df = pd.merge(movies_df, actors_df, on='movie_id', how='inner')
            figure = imdb_visuals.plot_gender_distribution(merged_df, return_figure=True)
        else:
            new_window.title("Actor Gender Distribution")
            merged_df = pd.merge(movies_df, actors_df, on='movie_id', how='inner')
            figure = imdb_visuals.plot_gender_distribution(merged_df, return_figure=True)

        if isinstance(figure, str):
            IMDBMsg.show_imdb_msg(self, f"Actor Gender Distribution year:{year}", figure)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
