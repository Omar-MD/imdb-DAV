from collections import Counter

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt, ticker
from matplotlib.lines import Line2D


"""
    General
"""


def plot_movie_count_vs_year(df, return_figure=False):
    """Plot a bar chart for the movie count vs. release year."""

    plt.figure(figsize=(10, 6))
    ax = plt.subplot(111)

    df.drop_duplicates(subset=['movie_id'], inplace=True)
    movie_count_by_year = df.groupby('movie_year').agg({'movie_id': 'count'}).reset_index()
    movie_count_by_year.sort_values('movie_year', ascending=True, inplace=True)
    movie_count_by_year.rename(columns={'movie_id': 'movie_count'}, inplace=True)

    # Movie Count vs Year
    ax.bar(movie_count_by_year['movie_year'], movie_count_by_year['movie_count'])
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))

    ax.set_xlabel("Release Year")
    ax.set_ylabel("Movie Count")
    ax.set_title("Movie Count vs. Release year")

    plt.tight_layout()

    if return_figure:
        return plt.gcf()  # Return the Matplotlib Figure object
    else:
        plt.show()


def plot_genre_distribution(df, return_figure=False):
    """Plot a bar chart of the movie count for each genre."""
    plt.figure(figsize=(12, 6))
    ax = plt.subplot(111)

    genre_counts = df.groupby('movie_genre').agg({'movie_id': 'count'}).reset_index()
    genre_counts.rename(columns={'movie_id': 'movie_count'}, inplace=True)
    genre_counts.sort_values(by='movie_count', inplace=True)

    ax.bar(genre_counts['movie_genre'], genre_counts['movie_count'])
    ax.set_xticks(range(len(genre_counts)))
    ax.set_xticklabels(genre_counts['movie_genre'], rotation=90)
    ax.set_xlabel('Genre')
    ax.set_ylabel('Movie count')
    ax.set_title("Genre Distribution")
    plt.tight_layout()

    if return_figure:
        return plt.gcf()  # Return the Matplotlib Figure object
    else:
        plt.show()


def plot_gender_distribution(df, return_figure=False):
    """Plot a pie chart for the actor gendre distribution"""
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111)

    # Assuming 'gender' is the column containing gender information
    gender_count = df['gender(act)'].value_counts()

    if len(gender_count) > 0:
        labels = gender_count.index.tolist()
        ax.pie(gender_count, labels=labels, autopct='%1.1f%%')
        ax.set_title("Gender distribution for all actors", fontsize=16)
        plt.tight_layout()

        if return_figure:
            return plt.gcf()  # Return the Matplotlib Figure object
        else:
            plt.show()
    else:
        return "No gender information available for actors."


"""
    Movie
"""


def plot_movie_rank_binning(movies_df, bin_size, title, movie_rank=None, return_figure=False):
    """Plot a histogram of average movie ratings with specified bin size."""

    movies_df = movies_df.drop_duplicates(subset=['movie_id']).copy()
    plt.figure(figsize=(10, 6))
    ax = plt.subplot(111)


    # Calculate average ratings per movie
    avg_ratings = movies_df.groupby('movie_id')['movie_rank'].mean()

    # Plot histogram
    ax.hist(avg_ratings, bins=np.arange(0.5, 10, bin_size), edgecolor='black', alpha=0.7, color='lightblue')
    ax.set_xticks(np.arange(1, 11))
    ax.set_xlabel("Average Movie Rank")
    ax.set_ylabel("Frequency")
    ax.set_title(title)

    # Add median and standard deviation to the plot
    median_value = avg_ratings.median()
    std_dev_value = avg_ratings.std()

    ax.annotate(f'Median: {median_value:.2f}', xy=(median_value, 0),
                xytext=(median_value, max(ax.get_ylim()) * 1),  # Adjusted position
                ha='center', color='red', fontsize=10,
                arrowprops=dict(facecolor='red', arrowstyle='->', linestyle='dashed', lw=0.5, shrinkA=0.05),
                label='Median Rank')

    # Annotation for standard deviation to the right
    ax.annotate(f'+1 Std Dev: {median_value + std_dev_value:.2f}', xy=(median_value + std_dev_value, 0),
                xytext=(median_value + std_dev_value, max(ax.get_ylim()) * 0.95),  # Adjusted position
                ha='center', color='blue', fontsize=10,
                arrowprops=dict(facecolor='blue', arrowstyle='->', linestyle='dashed', lw=0.5, shrinkA=0.05),
                label='Std Dev Right')

    # Annotation for standard deviation to the left
    ax.annotate(f'-1 Std Dev: {median_value - std_dev_value:.2f}', xy=(median_value - std_dev_value, 0),
                xytext=(median_value - std_dev_value, max(ax.get_ylim()) * 0.95),  # Adjusted position
                ha='center', color='blue', fontsize=10,
                arrowprops=dict(facecolor='blue', arrowstyle='->', linestyle='dashed', lw=0.5, shrinkA=0.05),
                label='Std Dev Left')

    # Manually create legend
    handles = [Line2D([0], [0], color='red', linestyle='dashed', lw=0.5),
               Line2D([0], [0], color='blue', linestyle='dashed', lw=0.5)]
    labels = ['Median Rank', 'Std Dev']

    # Optional annotation for the movie's rank
    if movie_rank is not None:
        ax.annotate(f'Movie Rank: {movie_rank:.2f}', xy=(movie_rank, 0),
                    xytext=(movie_rank, max(ax.get_ylim()) * 1.05),  # Adjusted position
                    ha='center', color='green', fontsize=10,
                    arrowprops=dict(facecolor='green', arrowstyle='->', linestyle='dashed', lw=0.5, shrinkA=0.05),
                    label='Movie Rank')
        handles.append(Line2D([0], [0], color='green', linestyle='dashed', lw=0.5))
        labels.append('Movie Rank')

    ax.set_ylim(bottom=0, top=max(ax.get_ylim()) * 1.1)
    ax.legend(handles=handles, labels=labels, loc='upper left', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    if return_figure:
        return plt.gcf()  # Return the Matplotlib Figure object
    else:
        plt.show()


"""
    Actor
"""


def plot_actor_count_over_years(merged_df, return_figure=False):
    # Actor count vs Year
    actors_by_year = merged_df.groupby(['movie_year']).agg({'actor_id': 'nunique'}).reset_index()

    # Plotting actor count vs year
    plt.figure(figsize=(12, 6))
    ax = plt.subplot(111)

    ax.plot(actors_by_year['movie_year'], actors_by_year['actor_id'], marker='o', color='blue')
    ax.set_title('Actor Count Over Years')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Unique Actors')
    plt.tight_layout()

    if return_figure:
        return plt.gcf()
    else:
        plt.show()


def plot_actor_occurrences(actor_occurrences, return_figure=False):
    """Visualization of the distribution with an improved boxplot"""
    plt.figure(figsize=(14, 6))
    ax = plt.subplot(111)

    # Boxplot with custom color and additional elements
    boxplot = ax.boxplot(actor_occurrences, vert=False, widths=0.7, patch_artist=True,
                         medianprops=dict(color='black', linewidth=2),
                         meanprops=dict(marker='o', markeredgecolor='black', markerfacecolor='red', markersize=8),
                         showmeans=True)

    # Customizing box colors
    for box in boxplot['boxes']:
        box.set(facecolor='lightblue', linewidth=2)

    ax.set_xlabel('Number of Movies Acted In')
    ax.set_title('Distribution of Actor Occurrences')
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Adding legend for mean and median
    ax.legend([boxplot["medians"][0], boxplot["means"][0]],
              ['Median', 'Mean'],
              loc='upper right')
    plt.tight_layout()

    if return_figure:
        return plt.gcf()
    else:
        plt.show()


def plot_actor_by_genre(merged_df, return_figure=False):
    # Actor count vs Genre
    actors_by_genre = merged_df.groupby(['movie_genre']).agg({'actor_id': 'count'}).reset_index()
    actors_by_genre.rename(columns={'actor_id': 'actor_count'}, inplace=True)
    actors_by_genre.sort_values(by='actor_count', ascending=True, inplace=True)

    # Plotting actor count vs genre
    plt.figure(figsize=(12, 6))
    ax = plt.subplot(111)

    x_positions = range(len(actors_by_genre))
    ax.bar(x_positions, actors_by_genre['actor_count'], color='blue')

    # Set custom tick positions and labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(actors_by_genre['movie_genre'], rotation=45, ha='right')

    ax.set_title('Actor Count vs Genre')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Actor Count')

    plt.tight_layout()
    if return_figure:
        return plt.gcf()
    else:
        plt.show()


def plot_actor_activity(roles_list, return_figure=False):
    years = [role[0] for role in roles_list]
    year_counts = Counter(years)

    sorted_years, counts = zip(*sorted(year_counts.items()))
    smooth_counts = np.interp(sorted_years, sorted_years, counts)

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(sorted_years, smooth_counts, marker='o', color='blue', linestyle='-', linewidth=2, markersize=8)
    plt.fill_between(sorted_years, 0, smooth_counts, color='lightblue', alpha=0.3)

    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.title('Actor Activity over Years')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Set y-axis ticks to display only integer values
    plt.yticks(np.arange(0, max(smooth_counts) + 2, 1))

    plt.tight_layout()
    if return_figure:
        return plt.gcf()
    else:
        plt.show()


def plot_actor_genre_distribution(role_genres, return_figure=False):
    all_genres = [genre for genres in role_genres for genre in genres]
    genre_counts = Counter(all_genres)
    sorted_genres, counts = zip(*sorted(genre_counts.items(), key=lambda x: x[1]))

    # Plotting
    plt.figure(figsize=(12, 6))
    ax = plt.subplot(111)

    ax.bar(sorted_genres, counts, color='blue')

    # Set custom tick positions and labels
    x_positions = range(len(sorted_genres))
    ax.set_xticks(x_positions)
    ax.set_xticklabels(sorted_genres, rotation=45, ha='right')

    ax.set_xlabel('Genre')
    ax.set_ylabel('Number of Movies')
    ax.set_title('Actor Genre Distribution')

    plt.tight_layout()
    if return_figure:
        return plt.gcf()
    else:
        plt.show()


def plot_actor_performance(roles_list, return_figure=False):
    # Calculate average movie rank for each year
    years = [role[0] for role in roles_list]
    ranks = [role[4] for role in roles_list]

    year_stats = {}
    for year, rank in zip(years, ranks):
        if year not in year_stats:
            year_stats[year] = {'sum': 0, 'count': 0}
        year_stats[year]['sum'] += rank
        year_stats[year]['count'] += 1

    # Calculate average ranks for each year
    avg_ranks = {year: stats['sum'] / stats['count'] for year, stats in year_stats.items()}

    # Sort years
    sorted_years, avg_counts = zip(*sorted(avg_ranks.items()))

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(sorted_years, avg_counts, marker='o', color='blue', linestyle='-', linewidth=2, markersize=8)
    plt.fill_between(sorted_years, 0, avg_counts, color='lightblue', alpha=0.3)

    plt.xlabel('Year')
    plt.ylabel('Average Movie Rank')
    plt.title('Actor Performance over Years')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    if return_figure:
        return plt.gcf()
    else:
        plt.show()


"""
    Genre
"""


def plot_genre_count_vs_year(movies_df, genre, return_figure=False):
    genre_years = (movies_df.groupby(['movie_year', 'movie_genre'])
                   .agg({'movie_id': 'count', 'movie_rank': 'mean'})
                   .reset_index())
    genre_years.rename(columns={'movie_id': 'movie_count', 'movie_rank': 'avg_movie_rank'}, inplace=True)
    genre_data = genre_years[genre_years['movie_genre'] == genre]

    # Movie Count Over the years
    plt.figure(figsize=(12, 6))
    ax = plt.subplot(111)

    # Use Seaborn for improved styling
    sns.lineplot(x='movie_year', y='movie_count', data=genre_data, label=genre, marker='o', ax=ax)

    ax.set_title(f'Movie Count Over Years for Genre: {genre}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Movie Count')
    ax.legend()
    plt.tight_layout()

    if return_figure:
        return plt.gcf()
    else:
        plt.show()


def plot_genre_avg_vs_year(movies_df, genre, return_figure=False):
    genre_years = (movies_df.groupby(['movie_year', 'movie_genre'])
                   .agg({'movie_id': 'count', 'movie_rank': 'mean'})
                   .reset_index())
    genre_years.rename(columns={'movie_id': 'movie_count', 'movie_rank': 'avg_movie_rank'}, inplace=True)
    genre_data = genre_years[genre_years['movie_genre'] == genre]

    # Average Movie Rank Over the Years (Line plot)
    plt.figure(figsize=(12, 6))
    ax = plt.subplot(111)

    # Use Seaborn for improved styling
    sns.lineplot(x='movie_year', y='avg_movie_rank', data=genre_data, marker='o', ax=ax)

    ax.set_title(f'Average movie rank by year: {genre}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Movie Rank')
    plt.tight_layout()

    if return_figure:
        return plt.gcf()
    else:
        plt.show()


"""
    Correlation
"""


def plot_corr_heatmap(corr_matrix, rank_type='All', return_figure=False):
    plt.figure(figsize=(10, 8))
    sns.heatmap(data=corr_matrix, cmap='Blues', vmin=-1.0, vmax=1.0, annot=True, fmt=".2f")
    plt.title(f'IMDB Heatmap Correlation ({rank_type})')
    plt.tight_layout()

    if return_figure:
        return plt.gcf()
    else:
        plt.show()


def plot_correlation(corr_df, rank_type, rank, return_figure=False):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 8))

    # Correlation
    sns.scatterplot(data=corr_df, x=rank_type, y='movie_rank')
    plt.title(f'{rank} vs. Movie Rank')
    plt.xlabel(rank)
    plt.ylabel('Movie Rank')
    plt.tight_layout()

    if return_figure:
        return plt.gcf()
    else:
        plt.show()


def plot_linear_regression(corr_df, rank_type, rank, return_figure=False):
    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 8))
    sns.lmplot(data=corr_df, x=rank_type, y='movie_rank', ci=None, line_kws={'color': 'red'})
    plt.title(f'Linear regression {rank} vs. Movie Rank')
    plt.xlabel(rank)
    plt.ylabel('Movie Rank')
    plt.tight_layout()

    if return_figure:
        return plt.gcf()
    else:
        plt.show()
