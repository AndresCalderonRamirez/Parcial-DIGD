import pandas as pd

genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

def get_genre_columns(df : pd.DataFrame) -> pd.DataFrame:
    if 'genres' in df.columns:
        df_copy = df.copy()
        df_copy[genres] = df_copy['genres'].str.get_dummies(sep='|')[genres]
        df_copy['None'] = (df_copy[genres].sum(axis=1) == 0).astype(int)
        df_copy = df_copy.drop(columns=['genres'])
        df = df_copy.copy()
    return df
