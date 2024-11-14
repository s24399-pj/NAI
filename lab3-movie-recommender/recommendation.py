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
    cluster_mean = matrix.loc[cluster_members].mean()
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
    cluster_mean = matrix.loc[cluster_members].mean()
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
