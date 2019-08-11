from os import path
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pd_doc2vec import doc2vec


def url(counter):
    url = "https://en.wikiquote.org/wiki/King_of_the_Hill"
    url += "_(season_" + str(counter) + ")"
    return url


def name_cleaner(name):
    name = str(name)
    try:
        return str(name.split()[0]).lower()
    except IndexError:
        return name


def koth_df():
    quotes = []
    for season in range(1, 13 + 1):
        response = requests.get(url(season))
        soup = BeautifulSoup(response.text, 'lxml')
        text = soup.find('div', {'class': 'mw-parser-output'})
        quotes += [i.split(":", 1) for i in text.text.split("\n") if ":" in i]

    df = pd.DataFrame(quotes, columns=["Character", "Quote"])
    return df


def droprows(filtered, bad_bois):
    for cond in bad_bois:
        filtered = filtered[filtered.Character != cond]
    return filtered


def build_model():

    file = "faked_koth_quotes.csv"
    #file = "koth_quotes.csv"


    if path.exists(file):
        df = pd.read_csv(file)
    else:
        df = koth_df()  # Scraping
        df.to_csv(file, index=False)

    # Analysis
    # df.Character.value_counts()

    # Cleaning
    df.Character = df.Character.apply(name_cleaner)
    filtered = df.drop_duplicates()
    filtered = df.groupby('Character').filter(lambda x: len(x) >= 100)
    filtered = droprows(filtered, ["wikipedia", "seasons"])
    filtered.Quote = filtered['Quote'].str.replace(r"\(.*\)", "")
    filtered.Quote = filtered['Quote'].str.replace(r"\[.*\]", "")
    filtered = filtered.dropna()
    filtered = filtered.applymap(str)

    model = doc2vec(filtered, "Quote", ['Character'], iterations=10, vector_size=7, window_size=31, min_count=2,
                    negative_size=2, train_epoch=66, build=True)
    return model
