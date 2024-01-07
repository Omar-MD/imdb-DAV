import io
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from IMDB.gui.IMDB_Msg_Obj import IMDBMsg
from IMDB.analysis.summary_analsis import prep_corr_df, show_corr_matrix
from IMDB.visualisation.imdb_visuals import plot_corr_heatmap, plot_correlation, plot_linear_regression

CORR_COLUMNS_DICT = {
    'Director Movie Count': 'director_movie_count',
    'Director Avg Movie Ranking': 'director_avg_rank',
    'Actor Movie Count': 'actor_movie_count',
    'Actor Avg Movie Ranking': 'actor_avg_rank',
    'Cast (Actors in Movie) Size': 'cast_size',
    'Cast Avg Movie Ranking': 'cast_avg_rank',
    'Crew (Cast & Director) Avg Movie Ranking': 'crew_avg_rank',
    'Movie Release Year': 'movie_year',
    'Movie Rank': 'movie_rank'
}

CORR_COLUMNS = ['Actor Movie Count', 'Actor Avg Movie Ranking', 'Cast (Actors in Movie) Size',
                'Cast Avg Movie Ranking', 'Crew (Cast & Director) Avg Movie Ranking',
                'Director Movie Count', 'Director Avg Movie Ranking', 'Movie Release Year', 'Movie Rank']


class IMDBCorrTab(ttk.Frame):
    def __init__(self, parent, logger, imdb_data):
        ttk.Frame.__init__(self, parent)
        self.title = "IMDB Actor Analysis"
        self.logger = logger
        self.imdb_data = imdb_data

        self.corr_df = None
        self.selected_column = None

    def create_widgets(self):
        self.corr_df = prep_corr_df(self.imdb_data.merged_movies, self.imdb_data.merged_actors, logger=self.logger)

        label_corr_heading = ttk.Label(self, text="IMDB Correlation Analysis")
        label_corr_heading.grid(row=0, column=0, columnspan=2, rowspan=1, sticky="nswe", padx=5, pady=5)

        # Column Name Label & Combobox
        label_column_name = ttk.Label(self, text="Select Column:")
        self.selected_column = tk.StringVar()
        column_names = sorted(CORR_COLUMNS)
        combo_column = ttk.Combobox(self, textvariable=self.selected_column, values=column_names, state='readonly')
        combo_column.set(CORR_COLUMNS[0])
        label_column_name.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        combo_column.grid(row=1, column=1, pady=5, padx=5, sticky="nswe")

        prepare_corr_button = tk.Button(self, text="Prepare Correlation DF", command=self.generate_corr_df)
        prepare_corr_button.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky="nswe")

        # Actors Summary
        label_summary = ttk.Label(self, text="Summary:")
        summary_corr_matrix_button = tk.Button(self, text="Correlation Matrix",
                                               command=self.generate_corr_matrix)

        summary_corr_heatmap = tk.Button(self, text="Correlation Heatmap", command=self.show_corr_heatmap)
        label_summary.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        summary_corr_matrix_button.grid(row=4, column=0, pady=5, padx=5, sticky="nswe")
        summary_corr_heatmap.grid(row=4, column=1, pady=5, padx=5, sticky="nswe")

        # Actors Summary
        label_column = ttk.Label(self, text="Column:")
        corr_matrix_button = tk.Button(self, text="Correlation Matrix", command=self.generate_filtered_corr_matrix)
        corr_heatmap_button = tk.Button(self, text="Correlation Heatmap", command=self.show_filtered_corr_heatmap)
        corr_button = tk.Button(self, text="Correlation Column vs Movie Rank", command=self.show_corr)
        linear_regression_button = tk.Button(self, text="Linear regression Column vs Movie Rank",
                                             command=self.show_linear_regression)

        label_column.grid(row=5, column=0, pady=5, padx=5, sticky="w")
        corr_matrix_button.grid(row=6, column=0, pady=5, padx=5, sticky="nswe")
        corr_heatmap_button.grid(row=6, column=1, pady=5, padx=5, sticky="nswe")
        corr_button.grid(row=7, column=0, pady=5, padx=5, sticky="nswe")
        linear_regression_button.grid(row=7, column=1, pady=5, padx=5, sticky="nswe")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)


    def show_linear_regression(self):
        new_window = tk.Toplevel(self)
        new_window.title(f"Linear regression ({self.selected_column.get()}) vs Movie Rank")
        rank_type = CORR_COLUMNS_DICT[self.selected_column.get()]

        figure = plot_linear_regression(self.corr_df, rank_type, self.selected_column.get(), return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()


    def show_corr(self):
        new_window = tk.Toplevel(self)
        new_window.title(f"Correlation ({self.selected_column.get()}) vs Movie Rank")
        rank_type = CORR_COLUMNS_DICT[self.selected_column.get()]

        figure = plot_correlation(self.corr_df, rank_type, self.selected_column.get(), return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def show_filtered_corr_heatmap(self):
        new_window = tk.Toplevel(self)
        new_window.title(f"Correlation Heatmap ({self.selected_column.get()})")
        rank_type = CORR_COLUMNS_DICT[self.selected_column.get()]
        corr_matrix = self.corr_df.corr()
        rank_corr = round(corr_matrix[[rank_type]].sort_values(by=rank_type, ascending=False), 3)

        figure = plot_corr_heatmap(rank_corr, self.selected_column.get(), return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def generate_filtered_corr_matrix(self):
        rank_type = CORR_COLUMNS_DICT[self.selected_column.get()]
        corr_matrix = self.corr_df.corr()
        rank_corr = round(corr_matrix[[rank_type]].sort_values(by=rank_type, ascending=False), 3)

        log_buffer = io.StringIO()
        show_corr_matrix(rank_corr, self.selected_column.get(), logger=log_buffer)

        corr_matrix = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(corr_matrix)
        IMDBMsg.show_imdb_msg(self, f"Correlation Matrix ({self.selected_column.get()})", corr_matrix)

    def show_corr_heatmap(self):
        new_window = tk.Toplevel(self)
        new_window.title("Correlation Heatmap")

        figure = plot_corr_heatmap(round(self.corr_df.corr(), 3), return_figure=True)

        canvas = FigureCanvasTkAgg(figure, master=new_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def generate_corr_matrix(self):
        log_buffer = io.StringIO()

        show_corr_matrix(round(self.corr_df.corr(), 3), logger=log_buffer)

        corr_matrix = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(corr_matrix)
        IMDBMsg.show_imdb_msg(self, "Correlation Matrix", corr_matrix)

    def generate_corr_df(self):
        movies_df = self.imdb_data.merged_movies
        actors_df = self.imdb_data.merged_actors

        log_buffer = io.StringIO()
        self.corr_df = prep_corr_df(movies_df, actors_df, logger=log_buffer)

        corr_info = log_buffer.getvalue()
        log_buffer.close()
        self.logger.write(corr_info)

        IMDBMsg.show_imdb_msg(self, "Correlation Info", corr_info)
