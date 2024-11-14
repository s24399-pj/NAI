import sys
from data_loader import load_data, create_user_item_matrix
from clustering import perform_kmeans_clustering, perform_agglomerative_clustering, perform_gmm_clustering
from evaluation import evaluate_clustering, compare_algorithms
from recommendation import recommend_films, anti_recommend_films, display_recommendations, display_anti_recommendations
from visualization import visualize_clusters

# Made by s24399-pj

def main():
    filepath = 'dane_filmy.json'

    df = load_data(filepath)
    matrix = create_user_item_matrix(df)

    if matrix.empty:
        sys.exit(1)

    kmeans_model, kmeans_labels = perform_kmeans_clustering(matrix, n_clusters=3)

    agglomerative_model, agglomerative_labels = perform_agglomerative_clustering(matrix, n_clusters=3, distance_metric='cosine')

    gmm_model, gmm_labels = perform_gmm_clustering(matrix, n_clusters=3, covariance_type='full')

    visualize_clusters(matrix, kmeans_labels, 'KMeans', 'Euclidean')
    visualize_clusters(matrix, agglomerative_labels, 'Agglomerative', 'Cosine')
    visualize_clusters(matrix, gmm_labels, 'GMM', 'EM')

    silhouette_kmeans, db_kmeans = evaluate_clustering(matrix, kmeans_labels)
    silhouette_agglomerative, db_agglomerative = evaluate_clustering(matrix, agglomerative_labels)
    silhouette_gmm, db_gmm = evaluate_clustering(matrix, gmm_labels)

    clustering_results = [
        ('KMeans', silhouette_kmeans, db_kmeans),
        ('Agglomerative Clustering', silhouette_agglomerative, db_agglomerative),
        ('GMM', silhouette_gmm, db_gmm)
    ]

    compare_algorithms(matrix, clustering_results)

    users = matrix.index.tolist()
    print("\nDostępni użytkownicy:")
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

    # KMeans
    recommendations_kmeans = recommend_films(selected_user, matrix, kmeans_labels, algorithm='kmeans', top_n=5)
    anti_recommend_kmeans = anti_recommend_films(selected_user, matrix, kmeans_labels, algorithm='kmeans', top_n=5)

    # Agglomerative
    recommendations_agglomerative = recommend_films(selected_user, matrix, agglomerative_labels, algorithm='agglomerative', top_n=5)
    anti_recommend_agglomerative = anti_recommend_films(selected_user, matrix, agglomerative_labels, algorithm='agglomerative', top_n=5)

    # GMM
    recommendations_gmm = recommend_films(selected_user, matrix, gmm_labels, algorithm='GMM', top_n=5)
    anti_recommend_gmm = anti_recommend_films(selected_user, matrix, gmm_labels, algorithm='GMM', top_n=5)

    display_recommendations(selected_user, recommendations_kmeans, 'Euclidean', 'KMeans')
    display_anti_recommendations(selected_user, anti_recommend_kmeans, 'Euclidean', 'KMeans')
    display_recommendations(selected_user, recommendations_agglomerative, 'Cosine', 'Agglomerative')
    display_anti_recommendations(selected_user, anti_recommend_agglomerative, 'Cosine', 'Agglomerative')
    display_recommendations(selected_user, recommendations_gmm, 'EM', 'GMM')
    display_anti_recommendations(selected_user, anti_recommend_gmm, 'EM', 'GMM')


if __name__ == "__main__":
    main()
