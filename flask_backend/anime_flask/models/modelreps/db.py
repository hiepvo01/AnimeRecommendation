import pandas as pd
import os

first_filtered = {'type': {'Unknown': 0, 'Music': 1, 'ONA': 2, 'Special': 3, 'Movie': 4, 'OVA': 5, 'TV': 6}, 'source': {'Radio': 0, 'Digital manga': 1, 'Card game': 2, 'Book': 3, 'Picture book': 4, 'Web manga': 5, '4-koma manga': 6, 'Music': 7, 'Novel': 8, 'Other': 9, 'Light novel': 10, 'Game': 11, 'Visual novel': 12, 'Manga': 13, 'Original': 14, 'Unknown': 15}, 'status': {'Not yet aired': 0, 'Currently Airing': 1, 'Finished Airing': 2}, 'airing': {True: 0, False: 1}, 'rating': {'None': 0, 'R+ - Mild Nudity': 1, 'R - 17+ (violence & profanity)': 2, 'Rx - Hentai': 3, 'PG - Children': 4, 'G - All Ages': 5, 'PG-13 - Teens 13 or older': 6}}

genres = ['0', 'Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life', 'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri']

user_default = {'type': 'TV', 'source': 'Visual novel', 'episodes': 11.667909932311092, 'status': 'Finished Airing', 'airing': False, 'duration': 26.237322491727163, 'rating': 'PG-13 - Teens 13 or older', 'scored_by': 11460.02527973477, 'rank': 5739.031634203619, 'popularity': 7220.259566238431, 'members': 22966.402679928167, 'favorites': 311.6496062992126, 'licensor': 0.6075424782428512, 'genre': ', Military, School', 'year': 2017}

response_default = [6, 12, 11.667909932311092, 2, 1, 26.237322491727163, 6, 11460.02527973477, 5739.031634203619, 7220.259566238431, 22966.402679928167, 311.6496062992126, 0.6075424782428512, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2017]

use_cols = ['type', 'source', 'episodes', 'status', 'airing', 'duration', 'rating', 'scored_by', 'rank', 'popularity', 'members', 'favorites', 'licensor', '0', 'Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life', 'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri', 'year']

basedir =  os.path.abspath(os.path.dirname(__file__))
basedir = basedir[:-16] + "Data\excel\model_data.csv"
df_model = pd.read_csv(basedir)