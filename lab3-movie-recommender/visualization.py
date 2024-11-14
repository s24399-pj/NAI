from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_clusters(matrix, labels, algorithm, distance_metric):
    """
    Wizualizuje klastry użytkowników za pomocą PCA.

    :param matrix: Macierz użytkownik-film.
    :param labels: Etykiety klastrów.
    :param algorithm: Algorytm klasteryzacji.
    :param distance_metric: Metryka odległości użyta do klasteryzacji.
    """
    pca = PCA(n_components=2)
    components = pca.fit_transform(matrix)

    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=components[:, 0], y=components[:, 1], hue=labels, palette='viridis', s=100)
    plt.title(f'Klasteryzacja użytkowników ({algorithm.capitalize()}, {distance_metric})')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.legend(title='Klaster')
    plt.show()
