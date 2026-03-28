import re

import nltk
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from .components.get_book_content import get_book_content

Word_Per_Chunk = 1000
N_Topics = 8
N_Words = 9

CHAPTER_PATTERN = re.compile(
    r'(?<!\w)(CHAPTER|CHAP)\s+([IVXLCDM]+|[0-9]+)\.?',
    flags=re.IGNORECASE,
)

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

    It combines the default NLTK English stopwords with stopwords defined in the project.

    ## Parameters
        None

    ## Returns
        A list containing all stopwords used for text preprocessing
    """
    nltk.download('stopwords', quiet=True)
    base = set(stopwords.words('english'))
    return list(base | LITERARY_STOPWORDS)


def split_into_chunks(text: str, words_per_chunk: int = Word_Per_Chunk):
    """
    Split a text into fixed-size chunks based on a number of words.

    This function is used in case no chapter markers
    are detected in the book.

    ## Parameters
        **text**: the full book text
        **words_per_chunk**: maximum number of words per chunk

    ## Returns
        A list of text chunks
    """

    tokens = text.split()
    chunks = []

    for i in range(0, len(tokens), words_per_chunk):
        chunk = ' '.join(tokens[i : i + words_per_chunk])
        chunks.append(chunk)

    return chunks


def split_book(text: str):
    """
    Split a book into chapters based on chapter markers.

    The function detects chapter titles such as "CHAPTER I" or
    "CHAP 1" using a regular expression. If no chapters are found,
    the book is split into fixed-size chunks.

    ## Parameters
        **text**: the full book text

    ## Returns
        A list of chapters or text chunks
    """
    text = text.replace('\r\n', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    all_boundaries = [m.start() for m in CHAPTER_PATTERN.finditer(text)]

    boundaries = []
    for pos in all_boundaries:
        if not boundaries or pos - boundaries[-1] > 500:
            boundaries.append(pos)

    if len(boundaries) <= 1:
        return split_into_chunks(text)

    chapters = []
    for idx, start in enumerate(boundaries):
        end = boundaries[idx + 1] if idx + 1 < len(boundaries) else len(text)
        chapter_text = text[start:end].strip()
        if chapter_text:
            chapters.append(chapter_text)

    return chapters


def get_top_words(model, feature_names: list, n_words: int):
    """
    Extract the most important words for each topic in the LDA model.

    For each topic, the function selects the words with the highest
    weights in the topic-word distribution.

    ## Parameters
        **model**: trained LDA model
        **feature_names**: vocabulary used by the vectorizer
        **n_words**: number of top words returned per topic

    ## Returns
        A list of topics containing their most important words
    """

    topics = []
    for topic in model.components_:
        top_indices = topic.argsort()[-n_words:][::-1]
        words = []

        for i in top_indices:
            words.append(feature_names[i])

        topics.append(words)

    return topics


def extract_topics_from_book(book_id: int, book_content: str | None = None, n_topics: int = N_Topics, n_words: int = N_Words):
    """
    Extract the main topic for each section of a book.

    The book is first downloaded from Project Gutenberg, then split
    into chapters or chunks. An LDA model is trained on these sections
    to determine the dominant topic for each one.

    ## Parameters
        **book_id**: Project Gutenberg book identifier
        **n_topics**: number of topics used by the LDA model
        **n_words**: number of representative words returned per topic

    ## Returns
        A dictionary mapping section numbers to their main topic words
    """
    text = book_content or get_book_content(book_id)

    chapters = split_book(text)

    vectorizer = CountVectorizer(
        stop_words=build_stopwords(),
        max_df=0.85,
        min_df=1,
        ngram_range=(1, 2),
        max_features=5000,
    )
    document_term_matrix = vectorizer.fit_transform(chapters)

    actual_n_topics = min(n_topics, len(chapters))

    lda = LatentDirichletAllocation(
        n_components=actual_n_topics,
        random_state=42,
        learning_method='batch',
        doc_topic_prior=0.1,
        topic_word_prior=0.01,
    )
    lda.fit(document_term_matrix)

    feature_names = vectorizer.get_feature_names_out()
    lda_topics = get_top_words(lda, feature_names, n_words)

    section_topic_matrix = lda.transform(document_term_matrix)

    results = {}
    for i in range(len(chapters)):
        topic_index = section_topic_matrix[i].argmax()
        results[i + 1] = lda_topics[topic_index]

    return results


def topic_modeling(book_id: int, book_content: str | None = None):
    """
    Entry point of the program.

    It parses command line arguments, extracts topics from the
    selected book, and prints the detected topics for each section.

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **book_content**: Book content

    ## Returns
        Main topics as string
    """

    topics = extract_topics_from_book(
        book_id=book_id,
        book_content=book_content
    )

    result = ''
    for section_num, words in topics.items():
        result += (f'\n=== Section {section_num} ===\n' + ', '.join(words) + '\n')

    return result
