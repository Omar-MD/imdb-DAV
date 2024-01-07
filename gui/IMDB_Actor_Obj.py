import io
import tkinter as tk
from tkinter import ttk

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from IMDB.gui.IMDB_Msg_Obj import IMDBMsg
from IMDB.analysis import actor_analysis
from IMDB.analysis.summary_analsis import actors_general, actors_specific
from IMDB.visualisation.imdb_visuals import (
    plot_actor_activity, plot_actor_genre_distribution, plot_actor_performance,
    plot_actor_occurrences, plot_actor_count_over_years, plot_actor_by_genre)

ACTOR_PARAMETERS = {
    'name': 'russell (i) crowe',
    'gender': 'm',
    'id': 101665,
    'role': 'maximus'
}


class IMDBActorTab(ttk.Frame):
    def __init__(self, parent, logger, imdb_data):
        ttk.Frame.__init__(self, parent)
        self.title = "IMDB Actor Analysis"
        self.logger = logger
        self.imdb_data = imdb_data

        self.selected_actor = None

    def create_widgets(self):
        actors_df = self.imdb_data.merged_actors
        label_actor_heading = ttk.Label(self, text="IMDB Actor Analysis")
        label_actor_heading.grid(row=0, column=0, columnspan=2, rowspan=1, sticky="nswe", padx=5, pady=5)

        # Actor Name Label & Combobox
        label_actor_name = ttk.Label(self, text="Select Actor:")
        self.selected_actor = tk.StringVar()
        actor_names = actor_analysis.get_actors(actors_df)
        combo_actor = ttk.Combobox(self, textvariable=self.selected_actor, values=actor_names, state='readonly')
        combo_actor.set(ACTOR_PARAMETERS['name'])
        label_actor_name.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")
        combo_actor.grid(row=1, column=1, pady=5, padx=5, sticky="nswe")

        # Actors Summary
        label_summary = ttk.Label(self, text="Summary:")
        summary_button = tk.Button(self, text="Actors Summary", command=self.generate_summary)
        actor_occurrences_button = tk.Button(self, text="Actors Occurrence", command=self.show_actor_occurrences)
        actor_distribution_button = tk.Button(
            self, text="Actors Genre Distribution", command=self.show_actor_distribution
        )
        actor_count_button = tk.Button(self, text="Actor Count vs Year", command=self.show_actor_count_year)
        label_summary.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        summary_button.grid(row=3, column=0, pady=5, padx=5, sticky="nswe")
        actor_occurrences_button.grid(row=3, column=1, pady=5, padx=5, sticky="nswe")
        actor_distribution_button.grid(row=4, column=0, pady=5, padx=5, sticky="nswe")
        actor_count_button.grid(row=4, column=1, pady=5, padx=5, sticky="nswe")

        # Actor
        label_actor = ttk.Label(self, text="Actor:")
        actor_summary_button = tk.Button(self, text="Summary", command=self.generate_actor_summary)
        actor_roles_button = tk.Button(self, text="Roles", command=self.show_actor_roles)
        actor_genre_button = tk.Button(self, text="Genre Distribution", command=self.show_actor_genre)
        actor_performance_button = tk.Button(self, text="Performance", command=self.show_actor_performance)
        actor_activity_button = tk.Button(self, text="Activity", command=self.show_actor_activity)
        label_actor.grid(row=5, column=0, pady=5, padx=5, sticky="w")
        actor_summary_button.grid(row=6, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")
        actor_roles_button.grid(row=7, column=0, pady=5, padx=5, sticky="nswe")
        actor_activity_button.grid(row=7, column=1, pady=5, padx=5, sticky="nswe")
        actor_genre_button.grid(row=8, column=0, pady=5, padx=5, sticky="nswe")
        actor_performance_button.grid(row=8, column=1, pady=5, padx=5, sticky="nswe")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        for i in range(9):
            self.grid_rowconfigure(i, weight=1)

    def show_actor_distribution(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        movies_df = movies_df.drop_duplicates(subset=['movie_id']).copy()
        merged_df = pd.merge(movies_df, actors_df, on='movie_id', how='inner')

        new_window = tk.Toplevel(self)
        new_window.title("Actor Count vs Year")

        figure = plot_actor_by_genre(merged_df, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_actor_count_year(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        movies_df = movies_df.drop_duplicates(subset=['movie_id']).copy()
        merged_df = pd.merge(movies_df, actors_df, on='movie_id', how='inner')

        new_window = tk.Toplevel(self)
        new_window.title("Actor Count vs Year")

        figure = plot_actor_count_over_years(merged_df, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_actor_occurrences(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        movies_df = movies_df.drop_duplicates(subset=['movie_id']).copy()
        merged_df = pd.merge(movies_df, actors_df, on='movie_id', how='inner')
        actor_occurrences = merged_df['actor_id'].value_counts()

        new_window = tk.Toplevel(self)
        new_window.title("Actor Occurrence")

        figure = plot_actor_occurrences(actor_occurrences, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_actor_performance(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        actor = actor_analysis.get_actor_by_name(movies_df, actors_df, self.selected_actor.get())
        actor_roles = actor['movie_roles']

        new_window = tk.Toplevel(self)
        new_window.title("Actor Performance")

        figure = plot_actor_performance(actor_roles, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_actor_genre(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        actor = actor_analysis.get_actor_by_name(movies_df, actors_df, self.selected_actor.get())
        actor_roles = actor['movie_roles']
        role_genres = actor_analysis.get_role_genres(movies_df, actor_roles)

        new_window = tk.Toplevel(self)
        new_window.title("Actor Genre Distribution")

        figure = plot_actor_genre_distribution(role_genres, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_actor_activity(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        actor = actor_analysis.get_actor_by_name(movies_df, actors_df, self.selected_actor.get())
        actor_roles = actor['movie_roles']

        new_window = tk.Toplevel(self)
        new_window.title("Actor Activity")

        figure = plot_actor_activity(actor_roles, return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def generate_summary(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        log_buffer = io.StringIO()
        actors_general(movies_df, actors_df, logger=log_buffer)

        summary_info = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(summary_info)

        IMDBMsg.show_imdb_msg(self, "Actor Summary", summary_info)

    def generate_actor_summary(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors
        actor_name = self.selected_actor.get()
        actor = actor_analysis.get_actor_by_name(movies_df, actors_df, actor_name)

        log_buffer = io.StringIO()
        actors_specific(movies_df, actors_df, actor['id'], logger=log_buffer)

        actor_info = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(actor_info)

        IMDBMsg.show_imdb_msg(self, f"Actor {actor_name} Summary", actor_info)

    def show_actor_roles(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors
        actor_name = self.selected_actor.get()
        actor = actor_analysis.get_actor_by_name(movies_df, actors_df, actor_name)
        actor_roles = actor['movie_roles']

        log_buffer = io.StringIO()
        actor_analysis.print_actor_roles(actor_roles, logger=log_buffer)

        actor_roles = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(actor_roles)

        IMDBMsg.show_imdb_msg(self, f"Actor {actor_name} Roles", actor_roles)
