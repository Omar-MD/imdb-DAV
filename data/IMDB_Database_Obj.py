import os.path
import pandas as pd
import pkg_resources
from sqlalchemy import create_engine

from IMDB.visualisation.df_visuals import printTitle, dataframe_EDA, printDF


class IMDBConnection:
    TABLE_NAMES = ['actors', 'directors', 'directors_genres', 'movies', 'movies_directors',
                   'movies_genres', 'roles']

    def __init__(self, connect_info, client=None, logger=None):
        """
        Initializes the DBConnection object.

        Parameters:
        - connect_info (tuple): Information required to establish a database connection.
        """
        # DB connection
        self.host, self.user, self.password, self.port, self.database = connect_info
        self.imdb_con = None
        self.client = client
        self.logger = logger


        self.dataframes = {}
        self.merged_movies = pd.DataFrame()
        self.merged_actors = pd.DataFrame()

        self.csv_file_path_movies = pkg_resources.resource_filename(__name__, "merged/movies_df.csv")
        self.csv_file_path_actors = pkg_resources.resource_filename(__name__, "merged/actors_df.csv")
        self.csv_file_cleaned_movies = pkg_resources.resource_filename(__name__, "cleaned/cleaned_movies_df.csv")
        self.csv_file_cleaned_actors = pkg_resources.resource_filename(__name__, "cleaned/cleaned_actors_df.csv")

    '''
        Public functions
    '''

    def load_df(self):
        """
        Loads Cleaned Data Frames from the data folder if saved, else merges and cleans the data.
        :return: None
        """
        printTitle("Loading DataFrames", logger=self.logger)
        self.logger.write("DataFrames in the storage:")
        self.logger.write("- merged_movies")
        self.logger.write("- merged_actors")
        self.__load_or_merge_df()
        self.__load_or_clean_df()
        self.client.ready = True

    def fetch_df(self):
        """
        Connects to DB, fetchs tables, merges and cleans them.
        :return: None
        """
        self.connect_db()
        self.load_tables()
        self.table_EDA()
        self.merge_df()
        self.clean_df()
        self.close_con()
        self.client.ready = True

    def connect_db(self):
        """
        Establishs a connection to the IMDB database.
        :return: None
        """
        printTitle("DB connection", logger=self.logger)
        self.logger.write(
            f"Connecting to Database: IMDB" +
            f"\nHost:      {self.host}" +
            f"\nUser:      {self.user}" +
            f"\nPassword:  {self.password}" +
            f"\nPort:      {self.port}" +
            f"\nDatabase:  {self.database}"
        )
        try:
            self.imdb_con = create_engine(
                f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
        except Exception as error:
            self.logger.write("Error: Unable to connect to DB")
            self.logger.write(f"Error Details: {error}")

    def load_tables(self):
        """
        Loads tables from the data folder if saved, else fetches them through the connection.
        :return: None
        """
        printTitle("Loading Tables", logger=self.logger)
        self.logger.write("Tables in the database:")
        for table_name in self.TABLE_NAMES:
            self.logger.write(table_name)
            csv_file_path = pkg_resources.resource_filename(__name__, f"tables/{table_name}.csv")

            if os.path.isfile(csv_file_path):
                df = pd.read_csv(csv_file_path)
            else:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, self.imdb_con)
                df.to_csv(csv_file_path, index=False)

            self.dataframes[table_name] = df.copy()

    def table_EDA(self):
        """
        Perform Exploratory Data Analysis for all DB tables.
        :return: None
        """
        printTitle("Tables Exploratory Data Analysis", logger=self.logger)
        for table_name, dataframe in self.dataframes.items():
            dataframe_EDA(table_name, dataframe, logger=self.logger)

    def movies_EDA(self):
        """
        Perform Exploratory Data Analysis for Cleaned Merged Data frames.
        :return: None
        """
        dataframe_EDA("Merged Movies DF", self.merged_movies, logger=self.logger)

    def actors_EDA(self):
        """
        Perform Exploratory Data Analysis for Cleaned Merged Data frames.
        :return: None
        """
        dataframe_EDA("Merged Actors DF", self.merged_actors, logger=self.logger)

    def merge_df(self):
        """
         Function responsible for merging the tables.
         merged_movies = movies, movies_directors, movies_genre, directors, directors_genres
         merged_actors = actors, roles
         :return: None
         """
        printTitle("Merge tables", logger=self.logger)
        self.__load_or_merge_df()

        self.logger.write("\nMerged movies dataframe:")
        printDF(self.merged_movies.head(), logger=self.logger)

        self.logger.write("\nMerged actors dataframe:")
        printDF(self.merged_actors.head(), logger=self.logger)

    def clean_df(self):
        """
        Function responsible for all data cleaning. Performs the following:
        (1) Standardize data i.e., ensures columns are all in a consistent format
        (2) Create new column
        (3) Drop duplicate rows/columns
        (4) Fill in missing/incomplete data
        (5) Handle outliers
        (6) Reorder columns
        :return: None
        """
        printTitle("Cleaning Merged Tables", logger=self.logger)
        self.__load_or_clean_df()

        dataframe_EDA("Merged Movie DF", self.merged_movies, logger=self.logger)
        dataframe_EDA("Merged Actor DF", self.merged_actors, logger=self.logger)

    '''
        Private functions
    '''

    def __load_or_merge_df(self):
        if os.path.isfile(self.csv_file_path_movies):
            self.merged_movies = pd.read_csv(self.csv_file_path_movies)
        else:
            self.load_tables()
            self.__merge_movie_tables()
            self.merged_movies.to_csv(self.csv_file_path_movies, index=False)

        if os.path.isfile(self.csv_file_path_actors):
            self.merged_actors = pd.read_csv(self.csv_file_path_actors)
        else:
            self.load_tables()
            self.__merge_actor_tables()
            self.merged_actors.to_csv(self.csv_file_path_actors, index=False)

    def __merge_movie_tables(self):
        self.logger.write("1. Merging movies with directors, genre..")
        movies_director_id = pd.merge(self.dataframes['movies'], self.dataframes['movies_directors'],
                                      left_on='id', right_on='movie_id', how='inner')
        self.logger.write("[x] movies_director_id created")

        movies_with_director = pd.merge(movies_director_id, self.dataframes['directors'],
                                        left_on='director_id', right_on='id', how='inner')
        self.logger.write("[x] movies_with_director created")

        movies_with_director_genre = pd.merge(movies_with_director, self.dataframes['movies_genres'],
                                              on='movie_id', how='inner')
        self.logger.write("[x] movies_with_director_genre created")

        movies_with_director_genre.drop(columns=['id_x', 'id_y'], inplace=True)
        self.logger.write("[x] dropped duplicate columns")

        movies_with_director_genre.rename(columns={'name': 'movie_name', 'year': 'movie_year', 'rank': 'movie_rank',
                                                   'genre': 'movie_genre', 'first_name': 'first_name(dir)',
                                                   'last_name': 'last_name(dir)'}, inplace=True)
        self.logger.write("[x] renamed columns")

        # Store merged movies data
        self.merged_movies = movies_with_director_genre

    def __merge_actor_tables(self):
        self.logger.write("\n2. Merging actors with roles...")

        actor_roles = pd.merge(self.dataframes['actors'], self.dataframes['roles'],
                               left_on='id', right_on='actor_id', how='inner')
        self.logger.write("[x] actor_roles created")

        actor_roles.drop(columns=['id'], inplace=True)
        self.logger.write("[x] dropped duplicate columns")

        actor_roles.rename(columns={'first_name': 'first_name(act)', 'last_name': 'last_name(act)',
                                    'gender': 'gender(act)', 'role': 'role(act)'}, inplace=True)
        self.logger.write("[x] renamed columns")

        # Store merged actors data
        self.merged_actors = actor_roles

    def __load_or_clean_df(self):
        if os.path.isfile(self.csv_file_cleaned_movies):
            self.merged_movies = pd.read_csv(self.csv_file_cleaned_movies)
        else:
            self.__load_or_merge_df()
            self.__clean_movies_df()
            self.merged_movies.to_csv(self.csv_file_cleaned_movies, index=False)

        if os.path.isfile(self.csv_file_cleaned_actors):
            self.merged_actors = pd.read_csv(self.csv_file_cleaned_actors)
        else:
            self.__load_or_merge_df()
            self.__clean_actors_df()
            self.merged_actors.to_csv(self.csv_file_cleaned_actors, index=False)

    def __clean_movies_df(self):
        # TODO: Uncomment (4)
        self.logger.write("\nCleaning Merged Movies table...")

        # (1) Standardise data
        self.logger.write("\n1. Standardising data...")
        self.__standardise_movie_df()

        # (2) Create new columns
        self.logger.write("\n2. Create new columns...")
        self.merged_movies['full_name(dir)'] = (self.merged_movies['first_name(dir)']
                                                + " " + self.merged_movies['last_name(dir)'])
        self.logger.write("[x] created new column: full_name(dir)")

        # (3) Drop duplicate columns/rows
        self.logger.write("\n3. Dropping duplicate columns/rows...")
        self.merged_movies.drop(columns=['first_name(dir)', 'last_name(dir)'], inplace=True)
        self.logger.write("[x] dropped duplicate columns: first_name(dir), last_name(dir)")
        self.merged_movies.drop_duplicates(inplace=True)
        self.logger.write("[x] dropped duplicate rows")

        # (4) Fill in missing data
        self.logger.write("\n4. Fill missing data...")
        # self.__fill_missing_movie_df()

        # (5) Handle Outliers
        self.logger.write("\n5. Handle Outliers...")
        # drop rows with missing or out-of-range movie_rank
        query = "not (movie_rank.isna() or movie_rank < 0 or movie_rank > 10)"
        self.merged_movies.query(query, inplace=True)
        self.logger.write("[x] dropped out-of-range movie_rank rows")

        # (6) Reorder columns
        self.logger.write("\n6. Reorder columns...")
        new_order = ['movie_id', 'movie_rank', 'movie_name', 'movie_year', 'movie_genre', 'director_id',
                     'full_name(dir)']
        self.merged_movies = self.merged_movies[new_order]
        self.logger.write("[x] reordered columns")

    def __standardise_movie_df(self):
        int_columns = ['movie_id', 'movie_year', 'director_id']
        float_columns = ['movie_rank']
        str_columns = ['movie_name', 'movie_genre', 'first_name(dir)', 'last_name(dir)']

        self.merged_movies[int_columns] = self.merged_movies[int_columns].astype('int')
        self.logger.write("[x] convert ids and movie_year to int64")
        self.merged_movies[float_columns] = self.merged_movies[float_columns].astype('float')
        self.logger.write("[x] convert movie_rank to float64")

        self.merged_movies[str_columns] = self.merged_movies[str_columns].astype('string')
        for col in str_columns:
            self.merged_movies[col] = self.merged_movies[col].map(str.lower)
            self.merged_movies[col] = self.merged_movies[col].map(str.strip)
        self.logger.write("[x] convert strings to lowercase, and strip leading/trailing spaces")

    def __fill_missing_movie_df(self):
        self.logger.write("Number of missing values in each column:")
        self.logger.write(self.merged_movies.isnull().sum())

        movie_columns = ['movie_name', 'movie_rank', 'movie_genre', 'movie_year']
        director_columns = ['full_name(dir)']

        # movie columns
        self.merged_movies.sort_values(by=['movie_id', 'movie_rank'], inplace=True)
        fill_values = {col: self.merged_movies[col].ffill() for col in movie_columns}
        self.merged_movies[movie_columns] = self.merged_movies.groupby('movie_id')[movie_columns].fillna(
            value=fill_values)
        self.logger.write("\n[x] filled in missing movie name, rank, genre and year")

        # director columns
        self.merged_movies.sort_values(by='director_id', inplace=True)
        fill_values = {col: self.merged_movies[col].ffill() for col in director_columns}
        self.merged_movies[director_columns] = self.merged_movies.groupby('director_id')[director_columns].fillna(
            value=fill_values)
        self.logger.write("[x] filled in missing director first name, and last name")

        self.merged_movies.dropna(inplace=True)
        self.logger.write("[x] Dropped rows that still contain nan values")

        self.logger.write("\nNumber of missing values in each column:")
        self.logger.write(self.merged_movies.isnull().sum())

    def __clean_actors_df(self):
        # TODO: Uncomment (4)
        self.logger.write("\nCleaning Merged Actors table...")

        # (1) Standardise data
        self.logger.write("\n1. Standardising data...")
        self.__standardise_actor_df()

        # (2) Create new columns
        self.logger.write("\n2. Create new columns...")
        self.merged_actors['full_name(act)'] = self.merged_actors['first_name(act)'] + " " + self.merged_actors[
            'last_name(act)']
        self.logger.write("[x] created new column: full_name(act)")

        # (3) Drop duplicate columns/rows
        self.logger.write("\n3. Dropping duplicate columns/rows...")
        self.merged_actors.drop(columns=['first_name(act)', 'last_name(act)'], inplace=True)
        self.logger.write("[x] dropped duplicate columns: first_name(act), last_name(act)")
        self.merged_actors.drop_duplicates(inplace=True)
        self.logger.write("[x] dropped duplicate rows")

        # (4) Fill in missing data
        self.logger.write("\n4. Fill missing data...")
        # self.__fill_missing_actor_df()

        # (5) Reorder columns
        self.logger.write("\n5. Reorder Columns...")
        new_order = ['actor_id', 'full_name(act)', 'gender(act)', 'role(act)', 'movie_id']
        self.merged_actors = self.merged_actors[new_order]
        self.logger.write("[x] reordered columns")

    def __standardise_actor_df(self):
        int_columns = ['actor_id']
        str_columns = ['gender(act)', 'role(act)', 'first_name(act)', 'last_name(act)']

        self.merged_actors[int_columns] = self.merged_actors[int_columns].astype('int')
        self.logger.write("[x] convert id to int64")

        self.merged_actors[str_columns] = self.merged_actors[str_columns].astype('string')
        self.merged_actors[str_columns] = self.merged_actors[str_columns].fillna('')
        for col in str_columns:
            self.merged_actors[col] = self.merged_actors[col].map(str.lower)
            self.merged_actors[col] = self.merged_actors[col].map(str.strip)
        self.logger.write("[x] convert strings to lowercase, and strip leading/trailing spaces")

    def __fill_missing_actor_df(self):
        self.logger.write("\nNumber of missing values in each column:")
        self.logger.write(self.merged_actors.isnull().sum())

        actor_columns = ['full_name(act)', 'gender(act)', 'role(act)']

        # actor columns
        self.merged_actors.sort_values(by=['actors_id'], inplace=True)
        fill_values = {col: self.merged_actors[col].ffill() for col in actor_columns}
        self.merged_actors[actor_columns] = self.merged_actors.groupby('actor_id')[actor_columns].fillna(
            value=fill_values)
        self.logger.write("\n[x] filled in missing actor full name, gender and role")

        self.merged_actors.dropna(inplace=True)
        self.logger.write("[x] Dropped rows that still contain nan values")

        self.logger.write("\nNumber of missing values in each column:")
        self.logger.write(self.merged_actors.isnull().sum())

    def close_con(self):
        """
        Terminates connection to the DB:
        :return: None
        """
        self.imdb_con.dispose()
        self.logger.write("\nDB Connection closed!")
