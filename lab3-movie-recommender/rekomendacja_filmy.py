import json
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler


def load_data(filepath):
    """
    Ładuje dane z pliku JSON.

    :param filepath: Ścieżka do pliku JSON.
    :return: Pandas DataFrame z danymi filmów i ocenami.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    records = []
    for osoba in data['Osoby']:
        nazwa = osoba['nazwa']
        kod = osoba.get('kod', None)
        for film in osoba['filmy']:
            records.append({
                'Użytkownik': nazwa,
                'Kod': kod,
                'Film': film['film'],
                'Ocena': film['ocena']
            })
    df = pd.DataFrame(records)
    return df


def create_user_item_matrix(df):
    """
    Tworzy macierz użytkownik-film z ocenami.

    :param df: DataFrame z danymi.
    :return: Macierz użytkownik-film.
    """
    matrix = df.pivot_table(index='Użytkownik', columns='Film', values='Ocena').fillna(0)
    return matrix


def perform_clustering(matrix, n_clusters=3, algorithm='kmeans', distance_metric='euclidean'):
    """
    Wykonuje klasteryzację na macierzy użytkownik-film.

    :param matrix: Macierz użytkownik-film.
    :param n_clusters: Liczba klastrów.
    :param algorithm: Algorytm klasteryzacji ('kmeans' lub 'agglomerative').
    :param distance_metric: Metryka odległości ('euclidean' lub 'cosine').
    :return: Model klasteryzacji oraz etykiety klastrów.
    """
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(matrix)

    if algorithm == 'kmeans':
        if distance_metric != 'euclidean':
            print("KMeans obsługuje tylko metrykę euklidesową. Użyję euklidesowej.")
        model = KMeans(n_clusters=n_clusters, random_state=42)
    elif algorithm == 'agglomerative':
        model = AgglomerativeClustering(n_clusters=n_clusters, metric=distance_metric, linkage='average')
    else:
        raise ValueError("Nieznany algorytm klasteryzacji.")

    if algorithm == 'kmeans':
        model.fit(scaled_matrix)
        labels = model.labels_
    else:
        labels = model.fit_predict(scaled_matrix)

    return model, labels


def recommend_films(user, matrix, labels, algorithm='kmeans', top_n=5):
    """
    Rekomenduje filmy dla użytkownika na podstawie jego klastra.

    :param user: Nazwa użytkownika.
    :param matrix: Macierz użytkownik-film.
    :param labels: Etykiety klastrów.
    :param algorithm: Algorytm klasteryzacji użyty do etykiet.
    :param top_n: Liczba rekomendacji.
    :return: Lista rekomendowanych filmów.
    """
    user_cluster = labels[matrix.index.get_loc(user)]
    cluster_members = matrix.index[labels == user_cluster]

    # Średnie oceny w klastrze
    cluster_mean = matrix.loc[cluster_members].mean()

    # Filmy, które użytkownik nie oglądał
    watched = matrix.loc[user]
    recommendations = cluster_mean[watched == 0].sort_values(ascending=False).head(top_n).index.tolist()
    return recommendations


def anti_recommend_films(user, matrix, labels, algorithm='kmeans', top_n=5):
    """
    Rekomenduje filmy, których użytkownik nie powinien oglądać.

    :param user: Nazwa użytkownika.
    :param matrix: Macierz użytkownik-film.
    :param labels: Etykiety klastrów.
    :param algorithm: Algorytm klasteryzacji użyty do etykiet.
    :param top_n: Liczba antyrekomendacji.
    :return: Lista antyrekomendowanych filmów.
    """
    user_cluster = labels[matrix.index.get_loc(user)]
    cluster_members = matrix.index[labels == user_cluster]

    # Średnie oceny w klastrze
    cluster_mean = matrix.loc[cluster_members].mean()

    # Filmy, które użytkownik nie oglądał
    watched = matrix.loc[user]
    anti_recommendations = cluster_mean[watched == 0].sort_values(ascending=True).head(top_n).index.tolist()
    return anti_recommendations


def display_recommendations(user, recommendations, distance_metric, algorithm):
    """
    Wyświetla rekomendacje.

    :param user: Nazwa użytkownika.
    :param recommendations: Lista rekomendowanych filmów.
    :param distance_metric: Metryka odległości użyta do klasteryzacji.
    :param algorithm: Algorytm klasteryzacji użyty do klasteryzacji.
    """
    print(f"\nRekomendacje dla {user} ({algorithm.capitalize()}, {distance_metric}):")
    for film in recommendations:
        print(f"- {film}")


def display_anti_recommendations(user, anti_recommendations, distance_metric, algorithm):
    """
    Wyświetla antyrekomendacje.

    :param user: Nazwa użytkownika.
    :param anti_recommendations: Lista antyrekomendowanych filmów.
    :param distance_metric: Metryka odległości użyta do klasteryzacji.
    :param algorithm: Algorytm klasteryzacji użyty do klasteryzacji.
    """
    print(f"\nAntyrekomendacje dla {user} ({algorithm.capitalize()}, {distance_metric}):")
    for film in anti_recommendations:
        print(f"- {film}")


def main():
    # Ścieżka do pliku z danymi
    filepath = 'dane_filmy.json'

    # Ładowanie danych
    df = load_data(filepath)
    matrix = create_user_item_matrix(df)

    # Klasteryzacja KMeans z metryką euklidesową
    kmeans_model, kmeans_labels = perform_clustering(matrix, n_clusters=3, algorithm='kmeans',
                                                     distance_metric='euclidean')

    # Klasteryzacja Agglomerative z metryką kosinusową
    agglomerative_model, agglomerative_labels = perform_clustering(matrix, n_clusters=3, algorithm='agglomerative',
                                                                   distance_metric='cosine')

    # Wybór użytkownika
    users = matrix.index.tolist()
    print("Dostępni użytkownicy:")
    for idx, user in enumerate(users, 1):
        print(f"{idx}. {user}")

    try:
        choice = int(input("Wybierz użytkownika (numer): "))
        if choice < 1 or choice > len(users):
            print("Nieprawidłowy wybór.")
            return
    except ValueError:
        print("Nieprawidłowy wybór.")
        return

    selected_user = users[choice - 1]

    # Rekomendacje i antyrekomendacje dla KMeans
    recommendations_kmeans = recommend_films(selected_user, matrix, kmeans_labels, algorithm='kmeans', top_n=5)
    anti_recommend_kmeans = anti_recommend_films(selected_user, matrix, kmeans_labels, algorithm='kmeans', top_n=5)

    # Rekomendacje i antyrekomendacje dla Agglomerative
    recommendations_agglomerative = recommend_films(selected_user, matrix, agglomerative_labels,
                                                    algorithm='agglomerative', top_n=5)
    anti_recommend_agglomerative = anti_recommend_films(selected_user, matrix, agglomerative_labels,
                                                        algorithm='agglomerative', top_n=5)

    # Wyświetlanie wyników
    display_recommendations(selected_user, recommendations_kmeans, 'euclidean', 'kmeans')
    display_anti_recommendations(selected_user, anti_recommend_kmeans, 'euclidean', 'kmeans')

    display_recommendations(selected_user, recommendations_agglomerative, 'cosine', 'agglomerative')
    display_anti_recommendations(selected_user, anti_recommend_agglomerative, 'cosine', 'agglomerative')


if __name__ == "__main__":
    main()
