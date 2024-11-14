from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


def perform_kmeans_clustering(matrix, n_clusters=3):
    """
    Wykonuje klasteryzację za pomocą K-Means.

    :param matrix: Macierz użytkownik-film.
    :param n_clusters: Liczba klastrów.
    :return: Model K-Means oraz etykiety klastrów.
    """
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(matrix)

    print("=== Skalowana macierz dla K-Means ===")
    print(scaled_matrix[:5])
    print(f"Rozmiar skalowanej macierzy: {scaled_matrix.shape}\n")

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(scaled_matrix)
    labels = kmeans.labels_

    return kmeans, labels


def perform_agglomerative_clustering(matrix, n_clusters=3, distance_metric='cosine'):
    """
    Wykonuje klasteryzację za pomocą Hierarchical (Agglomerative) Clustering.

    :param matrix: Macierz użytkownik-film.
    :param n_clusters: Liczba klastrów.
    :param distance_metric: Metryka odległości ('euclidean' lub 'cosine').
    :return: Model Agglomerative Clustering oraz etykiety klastrów.
    """
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(matrix)

    print("=== Skalowana macierz dla Agglomerative Clustering ===")
    print(scaled_matrix[:5])
    print(f"Rozmiar skalowanej macierzy: {scaled_matrix.shape}\n")

    agglomerative = AgglomerativeClustering(n_clusters=n_clusters, metric=distance_metric, linkage='average')
    labels = agglomerative.fit_predict(scaled_matrix)

    return agglomerative, labels


def perform_gmm_clustering(matrix, n_clusters=3, covariance_type='full'):
    """
    Wykonuje klasteryzację za pomocą Gaussian Mixture Models (EM).

    :param matrix: Macierz użytkownik-film.
    :param n_clusters: Liczba klastrów.
    :param covariance_type: Typ macierzy kowariancji ('full', 'tied', 'diag', 'spherical').
    :return: Model GMM oraz etykiety klastrów.
    """
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(matrix)

    print("=== Skalowana macierz dla GMM ===")
    print(scaled_matrix[:5])
    print(f"Rozmiar skalowanej macierzy: {scaled_matrix.shape}\n")

    gmm = GaussianMixture(n_components=n_clusters, covariance_type=covariance_type, random_state=42)
    gmm.fit(scaled_matrix)
    labels = gmm.predict(scaled_matrix)

    return gmm, labels
