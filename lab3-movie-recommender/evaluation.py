from sklearn.metrics import silhouette_score, davies_bouldin_score
import pandas as pd

def evaluate_clustering(matrix, labels):
    """
    Ocena jakości klasteryzacji za pomocą Silhouette Score i Davies-Bouldin Index.

    :param matrix: Macierz użytkownik-film.
    :param labels: Etykiety klastrów.
    :return: Silhouette Score i Davies-Bouldin Index.
    """
    if len(set(labels)) > 1:
        silhouette = silhouette_score(matrix, labels)
        davies_bouldin = davies_bouldin_score(matrix, labels)
    else:
        silhouette = -1
        davies_bouldin = -1
    return silhouette, davies_bouldin


def compare_algorithms(matrix, clustering_results):
    """
    Porównuje różne algorytmy klasteryzacji na podstawie metryk Silhouette Score i Davies-Bouldin Index.

    :param matrix: Macierz użytkownik-film.
    :param clustering_results: Lista krotek zawierających nazwę algorytmu, Silhouette Score i Davies-Bouldin Index.
    """
    comparison_df = pd.DataFrame(clustering_results, columns=['Algorithm', 'Silhouette Score', 'Davies-Bouldin Index'])
    print("\n=== Porównanie Algorytmów Klasteryzacji ===")
    print(comparison_df)
