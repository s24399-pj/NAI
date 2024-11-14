import json
import pandas as pd

def load_data(filepath):
    """
    Ładuje dane z pliku JSON, obsługuje duplikaty filmów dla danego użytkownika poprzez
    obliczenie średniej oceny.

    :param filepath: Ścieżka do pliku JSON.
    :return: Pandas DataFrame z danymi filmów i ocenami.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    records = []
    for osoba in data['Osoby']:
        nazwa = osoba['nazwa']

        for film in osoba.get('filmy', []):
            records.append({
                'Użytkownik': nazwa,
                'Film': film['film'],
                'Ocena': film['ocena']
            })
    df = pd.DataFrame(records)

    print("=== DataFrame po załadowaniu danych ===")
    print(df.head())
    print(f"Liczba rekordów: {len(df)}\n")

    df = df.groupby(['Użytkownik', 'Film'], as_index=False).mean()

    print("=== DataFrame po grupowaniu (średnie oceny) ===")
    print(df.head())
    print(f"Liczba rekordów po grupowaniu: {len(df)}\n")

    return df


def create_user_item_matrix(df):
    """
    Tworzy macierz użytkownik-film z ocenami.

    :param df: DataFrame z danymi.
    :return: Macierz użytkownik-film.
    """
    matrix = df.pivot_table(index='Użytkownik', columns='Film', values='Ocena').fillna(0)

    print("=== Macierz użytkownik-film ===")
    print(matrix.head())
    print(f"Rozmiar macierzy: {matrix.shape}\n")
    return matrix
