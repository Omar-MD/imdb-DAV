import pandas as pd
import IMDB.analysis.actor_analysis as actor_analysis
from IMDB.visualisation.df_visuals import printTitle, printDF

''' 
    Summary Analysis
'''


def summary_statistics(movies_df, actors_df, year=None, logger=None):
    """Provide Overall summary statistics of the IMDB data"""

    if year is None:
        printTitle("Overall Summary statistics", logger=logger)
    else:
        movies_df = movies_df[movies_df['movie_year'] == year]
        printTitle(f"Summary statistics for year: {year}", logger=logger)

    merged_df = pd.merge(movies_df, actors_df, on='movie_id', how='inner')

    total_movies = merged_df['movie_id'].nunique()
    total_genres = merged_df['movie_genre'].nunique()
    total_directors = merged_df['director_id'].nunique()
    total_actors = merged_df['actor_id'].nunique()

    if year is None:
        min_year = merged_df['movie_year'].min()
        max_year = merged_df['movie_year'].max()
        logger.write(f"\nSummary, for movies released between {min_year}-{max_year}:\n")
    else:
        logger.write(f"\nSummary, for movies released in {year}:\n")

    logger.write(f"Movie count: {total_movies}\n")
    logger.write(f"Genres:      {total_genres}\n")
    logger.write(f"Directors:   {total_directors}\n")
    logger.write(f"Actors:      {total_actors}\n")
    logger.write("\nMovie rank numerical summary:\n")
    logger.write(movies_df['movie_rank'].describe().to_string())



''' 
    Actor Analysis
'''


def actors_general(movies_df, actors_df, logger=None):
    printTitle("Actors General Analysis", logger=logger)

    # remove duplicate movie_ids/genre
    movies_df = movies_df.drop_duplicates(subset=['movie_id'])
    merged_df = pd.merge(movies_df, actors_df, on='movie_id', how='inner')

    actor_occurrences = merged_df['actor_id'].value_counts()

    logger.write(f"Min number of movies acted in: {actor_occurrences.min()}\n")
    logger.write(f"Max number of movies acted in: {actor_occurrences.max()}\n")
    logger.write(f"Mean number of movies acted in: {actor_occurrences.mean():.2f}\n")
    logger.write(f"Median number of movies acted in: {actor_occurrences.median():.2f}\n")


def actors_specific(movies_df, actors_df, actor_id, logger=None):
    printTitle(f"Actors Analysis for actors with id {actor_id}", logger=logger)

    actor = actor_analysis.get_actor_by_id(movies_df, actors_df, actor_id)
    actor_roles = actor['movie_roles']

    logger.write(f"\nActor details for actor id:{actor_id}\n")
    logger.write(f"Name:       {actor['name']}\n")
    logger.write(f"Gender:     {actor['gender']}\n")
    actor_analysis.print_roles_summary(movies_df, actor_roles, logger=logger)




''' 
    Genre Analysis
'''


def genre_summary(movies_df, logger=None):
    printTitle("Genre summary", logger=logger)

    genre_counts = movies_df['movie_genre'].value_counts()
    total_genres = movies_df['movie_genre'].nunique()
    largest_genre = genre_counts.idxmax()
    smallest_genre = genre_counts.idxmin()
    total_movies = len(movies_df)

    logger.write(f"\nTotal Genres: {total_genres}\n")
    logger.write(f"Largest Genre: {largest_genre}  (Count: {genre_counts[largest_genre]})\n")
    logger.write(f"Smallest Genre: {smallest_genre}(Count: {genre_counts[smallest_genre]})\n")
    logger.write(f"Total Movies: {total_movies}\n")

    logger.write("\nMovie Rank Numerical summary for each genre:\n")
    summary = movies_df.groupby('movie_genre')['movie_rank'].describe()
    printDF(summary, showIndex=True, logger=logger)


def genre_specific(movies_df, actors_df, genre, logger=None):
    printTitle(f"Genre({genre}) summary", logger=logger)

    merged_movie_actor = pd.merge(movies_df, actors_df, on='movie_id', how='inner')
    summary = merged_movie_actor[merged_movie_actor['movie_genre'] == genre]

    total_movies_in_genre = summary['movie_id'].nunique()
    total_actors_in_genre = summary['actor_id'].nunique()
    total_directors_in_genre = summary['director_id'].nunique()
    min_year = summary['movie_year'].min()
    max_year = summary['movie_year'].max()

    logger.write(f"\nGenre({genre}) summary, for movies released between {min_year}-{max_year}:\n")
    logger.write(f"Total Movies in genre:      {total_movies_in_genre}\n")
    logger.write(f"Total Actors in genre:      {total_actors_in_genre}\n")
    logger.write(f"Total Directors in genre:   {total_directors_in_genre}\n")

    logger.write(f"\nMovie rank numerical summary for genre({genre}):")
    summary_df = summary['movie_rank'].describe().reset_index()
    summary_df = summary_df.round(3).values.tolist()
    printDF(summary_df, logger=logger)



'''
    Correlation Analysis
'''


def prep_corr_df(movies_df, actors_df, logger=None):
    printTitle(f"Prepare Correlation Columns", logger=logger)

    corr_df = pd.merge(movies_df, actors_df, on='movie_id', how='inner')

    corr_df['director_movie_count'] = corr_df.groupby('director_id')['movie_id'].transform('count')
    logger.write("[x] Count of movies directors column generated: 'director_movie_count'\n")

    corr_df['actor_movie_count'] = corr_df.groupby('actor_id')['movie_id'].transform('count')
    logger.write("[x] Count of movies Acted by actor column generated: 'actor_movie_count'\n")

    corr_df['cast_size'] = corr_df.groupby('movie_id')['actor_id'].transform('count')
    logger.write("[x] Cast size column generated: 'cast_size'\n")

    corr_df['director_avg_rank'] = corr_df.groupby('director_id')['movie_rank'].transform('mean')
    logger.write("[x] Average Movie ranking for director: 'director_avg_rank'\n")

    corr_df['actor_avg_rank'] = corr_df.groupby('actor_id')['movie_rank'].transform('mean')
    logger.write("[x] Average Movie ranking for actor: 'actor_avg_rank'\n")

    corr_df['cast_avg_rank'] = corr_df.groupby('movie_id')['actor_avg_rank'].transform('mean')
    logger.write("[x] Average Movie ranking for cast: 'cast_avg_rank'\n")

    corr_df['crew_avg_rank'] = (corr_df['director_avg_rank'] + corr_df['cast_avg_rank']) / 2
    logger.write("[x] Average Movie ranking for cast & director: 'crew_avg_rank'\n")

    # Remove duplicates movie_id
    corr_df.drop_duplicates(subset=['movie_id'], inplace=True)
    corr_df.sort_values(by='movie_rank', inplace=True, ascending=False)

    # Define the columns to be dropped
    columns_to_drop = ['movie_name', 'movie_genre', 'full_name(dir)', 'full_name(act)',
                       'gender(act)', 'role(act)', 'movie_id', 'director_id', 'actor_id']
    corr_df.drop(columns=columns_to_drop, inplace=True)
    logger.write("[x] Dropped non numerical columns and id columns\n")

    logger.write("Handling outliers...\n")
    corr_df = handle_actor_movie_count_outliers(corr_df)
    logger.write("[x] Dropped Actor movie count outliers \n")
    corr_df = handle_director_movie_count_outliers(corr_df)
    logger.write("[x] Dropped Director movie count outliers\n")
    corr_df = handle_cast_size_outliers(corr_df)
    logger.write("[x] Dropped Cast size outliers\n")

    return corr_df


def show_corr_matrix(corr_matrix, rank_type='All', logger=None):
    printTitle(f"Correlation Matrix ({rank_type})", logger=logger)
    printDF(corr_matrix.round(3), showIndex=True, logger=logger)


def handle_actor_movie_count_outliers(corr_df):
    return corr_df[corr_df['actor_movie_count'] < 100]


def handle_cast_size_outliers(corr_df):
    return corr_df[corr_df['cast_size'] < 400]


def handle_director_movie_count_outliers(corr_df):
    return corr_df[corr_df['director_movie_count'] < 3750]
