from IMDB.analysis import actor_analysis
from IMDB.visualisation.df_visuals import printTitle
from IMDB.visualisation.imdb_visuals import plot_movie_rank_binning


def movie_overall_binning(movie_df, fine=False, movie_rank=None):
    movie_rank_binning(movie_df, "Overall", fine, movie_rank)


def movie_year_binning(movie_df, year, fine=False, movie_rank=None):
    year_df = movie_df[movie_df['movie_year'] == year]
    movie_rank_binning(year_df, f"Year:{year}", fine, movie_rank)


def movie_genre_binning(movie_df, genre, fine=False, movie_rank=None):
    genre_df = movie_df[movie_df['movie_genre'] == genre]
    movie_rank_binning(genre_df, f"Genre:{genre}", fine, movie_rank)


def movie_genre_year_binning(movie_df, genre, year, fine=False, movie_rank=None):
    genre_year_df = movie_df[(movie_df['movie_genre'] == genre) & (movie_df['movie_year'] == year)]
    movie_rank_binning(genre_year_df, f"Year:{year}-Genre:{genre}", fine, movie_rank)


def movie_rank_binning(movies_df, title, fine=False, movie_rank=None, return_figure=False):
    """Perform movie binning analysis Broad/Fine."""
    if fine:
        # Low-level Overview  (Fine binning)
        bin_size_small = 0.25
        return plot_movie_rank_binning(movies_df, bin_size_small, f"{title} - Fine Binning", movie_rank, return_figure)
    else:
        # High-level Overview (Broad binning)
        bin_size_large = 1.0
        return plot_movie_rank_binning(movies_df, bin_size_large, f"{title} - Broad Binning", movie_rank, return_figure)


def movie_summary(movies_df, movie_name, logger=None):
    printTitle(f"Movie summary", logger=logger)

    movie = get_movie_by_name(movies_df, movie_name)
    movie_df = movies_df[movies_df['movie_id'] == movie['id']]

    if movie_df.empty:
        logger.write(f"No Movie information found for movie ID: {movie['id']}\n")
    else:
        print_movie_summary(movies_df, movie['id'], movie['name'], movie['rank'],
                            movie['year'], movie['genres'], movie['director'],
                            logger=logger)


def print_movie_summary(movie_df, movie_id, name, rank, year, genres, director, logger=None):
    logger.write(f"\nSummary, for movie id:{movie_id} released {year}:\n")
    logger.write(f"Name:       {name}\n")
    logger.write(f"Rank:       {rank}\n")
    logger.write(f"Genres:     {genres}\n")
    logger.write(f"Director:\n  -ID:{director[0]},\tName:{director[1]}\n")

    avg_rank_all_movies = movie_df['movie_rank'].mean()
    logger.write(f"\nAverage Rank of All Movies: {avg_rank_all_movies:.2f}\n")
    logger.write(f"Comparison with Average Rank: {compare_rank(rank, avg_rank_all_movies)}\n")

    avg_rank_year = movie_df[movie_df['movie_year'] == year]['movie_rank'].mean()
    logger.write(f"\nAverage Rank of {year}: {avg_rank_year:.2f}\n")
    logger.write(f"Comparison with {year}'s Average: {compare_rank(rank, avg_rank_year)}\n")

    for genre in genres:
        avg_rank_genre = movie_df[movie_df['movie_genre'] == genre]['movie_rank'].mean()
        logger.write(f"\nAverage Rank of {genre}: {avg_rank_genre:.2f}\n")
        logger.write(f"Comparison with {genre} Average: {compare_rank(rank, avg_rank_genre)}\n")

        avg_rank_genre_year = movie_df[(movie_df['movie_year'] == year) &
                                       (movie_df['movie_genre'] == genre)]['movie_rank'].mean()
        logger.write(f"\nAverage Rank of {year}'s {genre}: {avg_rank_genre_year:.2f}\n")
        logger.write(
            f"Comparison with Average of {year}'s {genre}: {compare_rank(rank, avg_rank_genre_year)}\n"
        )


def compare_rank(movie_rank, avg_rank):
    if movie_rank > avg_rank:
        return "Higher rank than the average."
    elif movie_rank < avg_rank:
        return "Lower rank than the average."
    else:
        return "Same rank as the average."


'''
    Getters
'''


def get_movie_actors(movies_df, actors_df, movie_name, logger=None):
    printTitle(f"Movie Actors", logger=logger)

    movie = get_movie_by_name(movies_df, movie_name)
    actor_df = actors_df[actors_df['movie_id'] == movie['id']]

    if actor_df.empty:
        logger.write(f"\nNo Actor information found for movie ID: {movie['id']}\n")
    else:
        actors_list = actor_analysis.get_actor_list(actor_df)
        actor_analysis.print_movie_actors(actors_list, logger=logger)


def get_movies(movies_df):
    return sorted(list(movies_df['movie_name'].unique()))


def get_genres_list(movies_df):
    return sorted(list(movies_df['movie_genre'].unique()))


def get_movie_by_name(movie_df, movie_name):
    movie = movie_df[movie_df['movie_name'] == movie_name]
    if movie.empty:
        return
    return get_movie_info(movie)


def get_movie_by_id(movie_df, movie_id):
    movie = movie_df[movie_df['movie_id'] == movie_id]
    if movie.empty:
        return
    return get_movie_info(movie)


def get_movie_info(movie_df):
    return {
        'id': movie_df['movie_id'].iloc[0],
        'name': movie_df['movie_name'].iloc[0],
        'rank': movie_df['movie_rank'].iloc[0],
        'year': movie_df['movie_year'].iloc[0],
        'genres': movie_df['movie_genre'].unique(),
        'director': (movie_df['director_id'].iloc[0], movie_df['full_name(dir)'].iloc[0])
    }


def get_movie_genres(movie_df, movie_id=None, movie_name=None):
    if movie_id is not None:
        movie = get_movie_by_id(movie_df, movie_id)
    else:
        movie = get_movie_by_name(movie_df, movie_name)

    if movie is None:
        return
    else:
        return movie['genres'].tolist()


def get_movie_years(movie_df):
    return sorted(list(movie_df['movie_year'].unique()))
