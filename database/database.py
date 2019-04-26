import pandas as pd


class Database:

    @staticmethod
    def get_urls():
        df = pd.read_csv('data/properties.csv')
        return set(df['URL'])