import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .components.get_book_content import get_book_content

N_SIMILAR = 5

BOOK_COLLECTION = {
    11:    "Alice's Adventures in Wonderland",
    12:    "Through the Looking-Glass",
    16:    "Peter Pan",
    55:    "The Wonderful Wizard of Oz",
    113:   "The Secret Garden",
    120:   "Treasure Island",
    236:   "The Jungle Book",
    108:   "The Return of Sherlock Holmes",
    834:   "The Memoirs of Sherlock Holmes",
    863:   "The Mysterious Affair at Styles",
    1661:  "The Adventures of Sherlock Holmes",
    61262: "Poirot Investigates",
    69087: "The Murder of Roger Ackroyd",
    70114: "The Big Four",
    35:    "The Time Machine",
    36:    "The War of the Worlds",
    84:    "Frankenstein; Or, The Modern Prometheus",
    159:   "The Island of Doctor Moreau",
    164:   "Twenty Thousand Leagues under the Sea",
    345:   "Dracula",
}

LITERARY_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'of', 'to', 'in', 'on', 'at', 'for', 'with', 'by', 'is', 'are', 'was',
    'were', 'be', 'been', 'it', 'this', 'that', 'these', 'those', 'as', 'from', 'not', 'he', 'she', 'they', 'we',
    'you', 'i', 'his', 'her', 'their', 'our', 'my', 'your', 'him', 'them', 'me', 'us', 'do', 'did', 'does', 'have',
    'has', 'had', 'so', 'if', 'then', 'than', 'into', 'out', 'up', 'down', 'all', 'any', 'what', 'which', 'who', 'whom',
    'when', 'where', 'why', 'how', 'can', 'could', 'would', 'should', 'shall', 'will', 'may', 'might', 'must', 'there',
    'here', 'too', 'very', 'just', 'about', 'over', 'under', 'again', 'once',
}


def build_stopwords():
    """
    Build the list of stopwords used by the vectorizer.

    It combines the default NLTK English stopwords with stopwords
    defined in the project.

    ## Parameters
        None

    ## Returns
        A list containing all stopwords used for text preprocessing
    """
    nltk.download('stopwords', quiet=True)
    base = set(stopwords.words('english'))
    return list(base | LITERARY_STOPWORDS)


def load_all_books(book_ids: list):
    """
    Download and return the raw text for each book in the collection.

    Books that fail to download are silently skipped so that one
    unavailable title does not abort the whole process.

    ## Parameters
        **book_ids**: list of Project Gutenberg identifiers to fetch

    ## Returns
        A tuple (ids, texts) where ids is the filtered list of book
        identifiers that were successfully downloaded and texts is the
        corresponding list of raw book contents
    """
    ids = []
    texts = []

    for book_id in book_ids:
        content = get_book_content(book_id)
        if content:
            ids.append(book_id)
            texts.append(content)

    return ids, texts


def vectorize_books(texts: list):
    """
    Transform a list of book texts into a TF-IDF matrix.

    TfidfVectorizer combines CountVectorizer and TfidfTransformer into a
    single step.

    The fitted vectorizer is returned so that any new text can later be projected
    into the same vector space using transform() instead of fit_transform().

    ## Parameters
        **texts**: list of raw book contents

    ## Returns
        A tuple (tfidf_matrix, vectorizer) where tfidf_matrix is a
        matrix of shape (n_books, n_features) and vectorizer is the fitted TfidfVectorizer
    """
    vectorizer = TfidfVectorizer(
        stop_words=build_stopwords(),
        max_df=0.85,
        min_df=1,
        ngram_range=(1, 2),
        max_features=5000,
    )
    tfidf_matrix = vectorizer.fit_transform(texts)

    return tfidf_matrix, vectorizer

def find_similar_books(book_id: int, book_content: str | None = None, n_similar: int = N_SIMILAR):
    """
    Return a list of books most similar to the given book.

    The collection is used as training: the vectorizer
    and TF-IDF transformer are fitted on those 20 books so
    that the vocabulary and IDF weights are stable and consistent.

    If the requested book_id belongs to the collection it is projected
    using the computed matrix row. If it is an external book, the
    text is downloaded separately and placed into the same vector space
    using transform(), so that it is comparable to the collection vectors.

    ## Parameters
        **book_id**: Project Gutenberg identifier of the target book
        **n_similar**: number of similar books to return

    ## Returns
        A list of book titles from the collection sorted by decreasing
        similarity to the target book
    """
    collection_ids = list(BOOK_COLLECTION.keys())
    loaded_ids, texts = load_all_books(collection_ids)

    tfidf_matrix, vectorizer = vectorize_books(texts)

    if book_id in loaded_ids:
        target_index = loaded_ids.index(book_id)
        target_vector = tfidf_matrix[target_index]
    else:
        target_text = book_content or get_book_content(book_id)
        target_vector = vectorizer.transform([target_text])

    scores = cosine_similarity(target_vector, tfidf_matrix).flatten()

    ranked = []
    for idx, score in enumerate(scores):
        if book_id in loaded_ids and idx == loaded_ids.index(book_id):
            continue
        ranked.append((idx, score))

    ranked.sort(key=lambda pair: pair[1], reverse=True)

    similar_titles = []
    for idx, _score in ranked[:n_similar]:
        similar_book_id = loaded_ids[idx]
        similar_titles.append(BOOK_COLLECTION[similar_book_id])

    return similar_titles


def similar_books(book_id: int, book_content: str | None = None):
    """
    Entry point for the --similar option.

    It calls find_similar_books and formats the result as a printable
    list of titles sorted by decreasing similarity.

    ## Parameters
        **book_id**: Project Gutenberg identifier of the target book
        **book_content**: Book content

    ## Returns
        Similar book titles as a formatted string
    """
    titles = find_similar_books(book_id=book_id, book_content=book_content)

    return titles
