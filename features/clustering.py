from pathlib import Path

from .components.get_info import get_info

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer


def clustering(
    books_dir: str = 'alice_assets/books',
    output_path: str = 'alice_assets/plots/clustering.png',
    n_clusters: int = 3,
    max_features: int = 1000
) -> dict[str, list | str]:
    """
    Cluster books with TF-IDF + KMeans and save a plot.

    ## Parameters
        **books_dir**: folder containing .txt books
        **output_path**: output image path
        **n_clusters**: number of clusters
        **max_features**: TF-IDF max features

    ## Returns
        Dictionnary with labels, titles, and output path
    """

    if not isinstance(books_dir, str):
        raise TypeError('books_dir must be str')
    if not isinstance(output_path, str):
        raise TypeError('output_path must be str')
    if not isinstance(n_clusters, int):
        raise TypeError('n_clusters must be int')
    if not isinstance(max_features, int):
        raise TypeError('max_features must be int')
    if n_clusters <= 0:
        raise ValueError('n_clusters must be positive')
    if max_features <= 0:
        raise ValueError('max_features must be positive')

    books_path = Path(books_dir)
    if not books_path.exists():
        raise ValueError('books_dir does not exist')

    book_files = sorted(p for p in books_path.iterdir() if p.suffix == '.txt')
    if not book_files:
        raise ValueError('no .txt books found')

    def resolve_title(book_file: Path) -> str:
        stem = book_file.stem
        digits = ''.join(ch for ch in stem if ch.isdigit())
        if not digits:
            return book_file.name
        try:
            info = get_info(int(digits))
            title = info.get('title') if isinstance(info, dict) else None
            return title or book_file.name
        except Exception:
            return book_file.name

    texts = []
    titles = []
    for book_file in book_files:
        with open(book_file, encoding='utf-8', errors='ignore') as file:
            texts.append(file.read())
            titles.append(resolve_title(book_file))

    vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
    X = vectorizer.fit_transform(texts)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(X)

    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X.toarray())

    plt.figure(figsize=(10, 6))
    cmap = plt.cm.get_cmap('tab10', n_clusters)

    for i, (title, label) in enumerate(zip(titles, labels, strict=False)):
        plt.scatter(X_2d[i, 0], X_2d[i, 1], color=cmap(label), s=100)
        plt.annotate(title, (X_2d[i, 0], X_2d[i, 1]), fontsize=8)

    plt.title('Clustering off downloaded books')
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file)
    plt.close()

    return {
        'labels': labels.tolist(),
        'titles': titles,
        'output_path': str(output_file)
    }
