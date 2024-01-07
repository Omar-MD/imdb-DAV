from IMDB.analysis import movie_analysis
from IMDB.visualisation.df_visuals import printDF


def print_movie_actors(actors_list, logger=None):
    logger.write("\nActors:")
    actor_headers = ["ID", "Name", "Role", "Gender"]
    printDF(actors_list, headers=actor_headers, logger=logger)


def print_actor_roles(roles_list, logger=None):
    logger.write("\nRoles:")
    roles_headers = ["Year", "Movie Name", "Director Name", "Actor Role", "Movie Rank"]
    printDF(roles_list, headers=roles_headers, logger=logger)


def print_roles_summary(movie_df, roles_list, logger=None):
    num_movies = len(roles_list)
    num_directors_worked_with = len(set(role[2] for role in roles_list))

    year_first_movie = min(role[0] for role in roles_list)
    year_latest_movie = max(role[0] for role in roles_list)

    role_genres = get_role_genres(movie_df, roles_list)
    genres_acted_in = set(genre for genres in role_genres for genre in genres)

    top_movie_rank = max(role[4] for role in roles_list)
    avg_movie_rank = sum(role[4] for role in roles_list) / num_movies if num_movies > 0 else 0
    worst_movie_rank = min(role[4] for role in roles_list)

    logger.write("\nRoles Summary:\n")
    logger.write(f"Number of Movies Acted In: {num_movies}\n")
    logger.write(f"Number of Directors Worked With: {num_directors_worked_with}\n")
    logger.write(f"Year of First Movie: {year_first_movie}\n")
    logger.write(f"Year of Latest Movie: {year_latest_movie}\n")
    logger.write(f"Career longevity: {year_latest_movie-year_first_movie}\n")
    logger.write(f"\nGenres Acted In:\n{', '.join(genres_acted_in)}\n")
    logger.write(f"\nTop Movie Rank:\t{top_movie_rank}\n")
    logger.write(f"Avg Movie Rank:\t{avg_movie_rank:.2f}\n")
    logger.write(f"Worst Movie Rank:\t{worst_movie_rank}\n")


"""
    Getters
"""


def get_actors(actors_df):
    return sorted(list(actors_df['full_name(act)'].unique()))


def get_actor_list(actor_df):
    return list(actor_df[['actor_id', 'full_name(act)', 'role(act)', 'gender(act)']]
                .itertuples(index=False, name=None))


def get_actor_by_name(movie_df, actor_df, actor_name):
    actor = actor_df[actor_df['full_name(act)'] == actor_name]
    return get_actor_info(movie_df, actor)


def get_actor_by_id(movie_df, actor_df, actor_id):
    actor = actor_df[actor_df['actor_id'] == actor_id]
    return get_actor_info(movie_df, actor)


def get_actor_roles(movie_df, actor_df):
    roles = actor_df['role(act)'].tolist()
    movie_ids = actor_df['movie_id'].tolist()
    movie_roles = []

    for idx, (role, movie_id) in enumerate(zip(roles, movie_ids), start=1):
        movie = movie_analysis.get_movie_by_id(movie_df, movie_id)
        if movie is not None:
            movie_roles.append(
                [movie['year'], movie['name'], movie['director'][1], role, movie['rank']]
            )
    # Sort movie_roles based on year
    movie_roles = sorted(movie_roles, key=lambda x: x[0])
    return movie_roles


def get_actor_info(movie_df, actor_df):
    return {
        'id': actor_df['actor_id'].iloc[0],
        'name': actor_df['full_name(act)'].iloc[0],
        'gender': actor_df['gender(act)'].iloc[0],
        'movie_roles': get_actor_roles(movie_df, actor_df)
    }


def get_role_genres(movie_df, roles_list):
    return [movie_analysis.get_movie_genres(movie_df, movie_name=role[1]) for role in roles_list]
