import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
import cv2

def load_and_scale_data(file_path, column_names=None):
    """
    Ładuje dane z pliku i skaluje cechy.

    Args:
        file_path: ścieżka do pliku z danymi
        column_names: opcjonalna lista nazw kolumn

    Returns:
        X_scaled: przeskalowane cechy
        y: etykiety
    """
    data = pd.read_csv(file_path, sep=r'\s+', names=column_names)
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y


def evaluate_classifiers(X, y, dataset_name):
    """
    Trenuje i ocenia różne klasyfikatory na danych.

    Args:
        X: cechy
        y: etykiety
        dataset_name: nazwa zbioru danych
    """
    # Podział na zbiory treningowe i testowe
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    classifiers = {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "SVM": SVC(kernel='linear', random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=3),
        "Naive Bayes": GaussianNB()
    }

    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        print(f"\n{dataset_name} - {name} Classification Report:")
        print(classification_report(y_test, y_pred))


def visualize_data(X, y, dataset_name):
    """
    Wizualizuje dane w 2D.

    Args:
        X: cechy
        y: etykiety
        dataset_name: nazwa zbioru danych
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', alpha=0.7)
    plt.title(f"{dataset_name} Visualization")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.colorbar(label="Class")
    plt.show()


def predict_with_classifiers(X_example, classifiers, X_train, y_train):
    """
    Wyświetla predykcje dla różnych klasyfikatorów.

    Args:
        X_example: przykładowe dane wejściowe
        classifiers: słownik klasyfikatorów
        X_train: dane treningowe
        y_train: etykiety treningowe
    """
    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        prediction = clf.predict(X_example)
        print(f"Prediction for {name}: {prediction}")


def load_images_from_folder(folder_path, label):
    """
    Ładuje obrazy z folderu i przekształca je do odcieni szarości oraz zmienia rozmiar.

    Args:
        folder_path: ścieżka do folderu z obrazami
        label: etykieta klasy (0 lub 1)

    Returns:
        images: lista obrazów w formie znormalizowanych wektorów
        labels: lista etykiet odpowiadających obrazom
    """
    images = []
    labels = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Wczytaj obraz w odcieniach szarości
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if image is not None:
                # Zmień rozmiar obrazu na 64x64 pikseli
                image = cv2.resize(image, (64, 64))
                # Znormalizuj wartości pikseli
                image = image / 255.0
                # Spłaszcz obraz do wektora
                images.append(image.flatten())
                labels.append(label)
    return images, labels


def load_brain_tumor_data(base_path):
    """
    Ładuje obrazy z danych Brain Tumor.

    Args:
        base_path: ścieżka do folderu z danymi `brain_tumor_dataset`

    Returns:
        X: znormalizowane obrazy w postaci wektorów
        y: etykiety obrazów
    """
    X, y = [], []
    yes_path = os.path.join(base_path, "yes")
    no_path = os.path.join(base_path, "no")

    yes_images, yes_labels = load_images_from_folder(yes_path, label=1)
    no_images, no_labels = load_images_from_folder(no_path, label=0)

    X.extend(yes_images)
    y.extend(yes_labels)

    X.extend(no_images)
    y.extend(no_labels)

    return np.array(X), np.array(y)


if __name__ == "__main__":
    seeds_file_path = "seeds_dataset.txt"
    seeds_column_names = ["Area", "Perimeter", "Compactness", "Length", "Width", "Asymmetry", "GrooveLength", "Class"]

    X_seeds, y_seeds = load_and_scale_data(seeds_file_path, seeds_column_names)
    evaluate_classifiers(X_seeds, y_seeds, "Seeds Dataset")
    visualize_data(X_seeds, y_seeds, "Seeds Dataset")

    base_path = "brain_tumor_data/brain_tumor_dataset"
    X_brain_mri, y_brain_mri = load_brain_tumor_data(base_path)

    print(f"\nNumber of samples: {len(X_brain_mri)}")
    print(f"Positive samples (tumor): {sum(y_brain_mri)}")
    print(f"Negative samples (no tumor): {len(y_brain_mri) - sum(y_brain_mri)}")

    evaluate_classifiers(X_brain_mri, y_brain_mri, "Brain MRI Dataset")
