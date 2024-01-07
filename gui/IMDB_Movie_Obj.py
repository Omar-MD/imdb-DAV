import io
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from IMDB.gui.IMDB_Msg_Obj import IMDBMsg
from IMDB.analysis import movie_analysis
from IMDB.visualisation.imdb_visuals import plot_movie_rank_binning

MOVIE_PARAMETERS = {
    'id': 129185,
    'name': 'gladiator',
    'year': 2000,
    'genre': 'action',
    'director_id': 71703,
    'actor_id': 101665
}

BIN_TYPES = ['Coarse', 'Fine', 'Very Fine']


class IMDBMovieTab(ttk.Frame):
    def __init__(self, parent, logger, imdb_data):
        ttk.Frame.__init__(self, parent)
        self.title = "IMDB Movie Analysis"
        self.logger = logger
        self.imdb_data = imdb_data

        self.selected_movie = None
        self.selected_genre = None
        self.selected_year = None
        self.selected_bin = None

    def create_widgets(self):
        movies_df = self.imdb_data.merged_movies
        label_movie_heading = ttk.Label(self, text="IMDB Movie Analysis")
        label_movie_heading.grid(row=0, column=0, columnspan=2, sticky="nswe", padx=5, pady=5)

        # Movie Selection Section
        label_movie_name = ttk.Label(self, text="Select Movie:")
        self.selected_movie = tk.StringVar()
        movie_names = movie_analysis.get_movies(movies_df)
        combo_movie = ttk.Combobox(self, textvariable=self.selected_movie, values=movie_names, state='readonly')
        combo_movie.set(MOVIE_PARAMETERS['name'])
        label_movie_name.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")
        combo_movie.grid(row=1, column=1, pady=5, padx=5, sticky="nswe")

        label_genre_name = ttk.Label(self, text="Select Genre:")
        self.selected_genre = tk.StringVar()
        genre_names = movie_analysis.get_genres_list(movies_df)
        combo_genre = ttk.Combobox(self, textvariable=self.selected_genre, values=genre_names, state='readonly')
        combo_genre.set(MOVIE_PARAMETERS['genre'])
        label_genre_name.grid(row=2, column=0, pady=5, padx=5, sticky="nswe")
        combo_genre.grid(row=2, column=1, pady=5, padx=5, sticky="nswe")

        label_year = ttk.Label(self, text="Select Year:")
        self.selected_year = tk.StringVar()
        years = movie_analysis.get_movie_years(movies_df)
        combo_year = ttk.Combobox(self, textvariable=self.selected_year, values=years, state='readonly')
        combo_year.set(str(MOVIE_PARAMETERS['year']))
        label_year.grid(row=3, column=0, pady=5, padx=5, sticky="nswe")
        combo_year.grid(row=3, column=1, pady=5, padx=5, sticky="nswe")

        label_bin = ttk.Label(self, text="Select Bin:")
        self.selected_bin = tk.StringVar()
        combo_bin = ttk.Combobox(self, textvariable=self.selected_bin, values=BIN_TYPES, state='readonly')
        combo_bin.set(BIN_TYPES[0])
        label_bin.grid(row=4, column=0, pady=5, padx=5, sticky="nswe")
        combo_bin.grid(row=4, column=1, pady=5, padx=5, sticky="nswe")

        # Buttons Section
        label_summary = ttk.Label(self, text="Summary:")
        summary_button = tk.Button(self, text="Movie Summary", command=self.generate_movie_summary)
        actors_button = tk.Button(self, text="Movie Actors", command=self.show_actors)
        label_summary.grid(row=5, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")
        summary_button.grid(row=6, column=0, pady=5, padx=5, sticky="nswe")
        actors_button.grid(row=6, column=1, pady=5, padx=5, sticky="nswe")

        # Movie Rank Section
        label_movie_rank = ttk.Label(self, text="Movie Rank:")
        movie_overall_button = tk.Button(self, text="Movie Rank vs All", command=self.plot_movie_rank_overall)
        movie_year_button = tk.Button(self, text="Movie Rank vs Year", command=self.plot_movie_rank_year)
        movie_genre_button = tk.Button(self, text="Movie Rank vs Genre", command=self.plot_movie_rank_genre)
        movie_director_button = tk.Button(self, text="Movie Rank vs Director Works",
                                          command=self.plot_movie_rank_director)
        label_movie_rank.grid(row=7, column=0, pady=5, padx=5, sticky="nswe")
        movie_overall_button.grid(row=8, column=0, pady=5, padx=5, sticky="nswe")
        movie_year_button.grid(row=8, column=1, pady=5, padx=5, sticky="nswe")
        movie_genre_button.grid(row=9, column=0, pady=5, padx=5, sticky="nswe")
        movie_director_button.grid(row=9, column=1, pady=5, padx=5, sticky="nswe")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)

    def plot_movie_rank_overall(self):
        movies_df = self.imdb_data.merged_movies
        movie = movie_analysis.get_movie_by_name(movies_df, self.selected_movie.get())

        new_window = tk.Toplevel(self)
        new_window.title("Movie Rank vs Overall")

        figure = plot_movie_rank_binning(
            movies_df, self.get_selected_bin(),
            f"{self.selected_movie.get()} vs Overall Avg ({self.selected_bin.get()})",
            movie['rank'], return_figure=True
        )

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def plot_movie_rank_year(self):
        year = int(self.selected_year.get())
        movies_df = self.imdb_data.merged_movies
        movie = movie_analysis.get_movie_by_name(movies_df, self.selected_movie.get())

        movies_df = movies_df[movies_df['movie_year'] == year]
        new_window = tk.Toplevel(self)
        new_window.title("Movie Rank vs Year")

        figure = plot_movie_rank_binning(
            movies_df, self.get_selected_bin(),
            f"{self.selected_movie.get()} vs {year} Avg ({self.selected_bin.get()})",
            movie['rank'], return_figure=True
        )
        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def plot_movie_rank_genre(self):
        genre = self.selected_genre.get()
        movies_df = self.imdb_data.merged_movies
        movies_df = movies_df[movies_df['movie_genre'] == genre]

        movie = movie_analysis.get_movie_by_name(movies_df, self.selected_movie.get())

        new_window = tk.Toplevel(self)
        new_window.title("Movie Rank vs Genre")

        figure = plot_movie_rank_binning(
            movies_df, self.get_selected_bin(),
            f"{self.selected_movie.get()} vs {genre} Avg ({self.selected_bin.get()})",
            movie['rank'], return_figure=True
        )

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def plot_movie_rank_director(self):
        movies_df = self.imdb_data.merged_movies
        movie = movie_analysis.get_movie_by_name(movies_df, self.selected_movie.get())
        movies_df = movies_df[movies_df['director_id'] == movie['director'][0]]

        new_window = tk.Toplevel(self)
        new_window.title("Movie Rank vs Director Works")

        figure = plot_movie_rank_binning(
            movies_df, self.get_selected_bin(),
            f"{self.selected_movie.get()} vs Director Avg ({self.selected_bin.get()})",
            movie['rank'], return_figure=True
        )

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def generate_movie_summary(self):
        movie_name = self.selected_movie.get()
        movies_df = self.imdb_data.merged_movies

        log_buffer = io.StringIO()

        movie_analysis.movie_summary(movies_df, movie_name, logger=log_buffer)

        movie_info = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(movie_info)

        IMDBMsg.show_imdb_msg(self, "Movie Summary", movie_info)


    def show_actors(self):
        movie_name = self.selected_movie.get()
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        log_buffer = io.StringIO()

        movie_analysis.get_movie_actors(movies_df, actors_df, movie_name, logger=log_buffer)

        movie_actors = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(movie_actors)

        IMDBMsg.show_imdb_msg(self, "Movie Actors", movie_actors)

    def get_selected_bin(self):
        bin_type = self.selected_bin.get()
        if bin_type == BIN_TYPES[0]:
            return 1.0
        elif bin_type == BIN_TYPES[1]:
            return 0.25
        else:
            return 0.1
