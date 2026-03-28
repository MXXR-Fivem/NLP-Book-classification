from .components.build_summary import build_summary
from .components.clean_book_content import clean_book_content
from .components.get_book_content import get_book_content
from .components.score_sentences import score_sentences
from .components.segmentation import segmentation


def summarize_book(
    book_id: int,
    book_content: str | None = None,
    max_sentences: int = 10,
    min_words: int = 17,
    max_words: int = 40,
    min_useful_words: int = 8,
    min_word_length: int = 3,
    exclude_dialogue: bool = True,
    normalize_by_length: bool = True,
    skip_first_sentences: int = 12,
    min_score: float = 0.0,
) -> str:
    """
    Summarize book

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **book_content**: Book content
        **max_sentences**: number of sentences kept
        **min_words**: reject very short sentences
        **max_words**: reject very long sentences
        **min_useful_words**: reject sentences who has more or less useful words
        **min_word_length**: ignore very short tokens
        **exclude_dialogue**: reject sentences containing quotes
        **normalize_by_length**: divide score by useful word count
        **skip_first_sentences**: skip first n sentences
        **min_score**: ignore sentences with score <= min_score

    ## Returns
        The summarized book
    """

    if book_content is not None and not isinstance(book_content, str):
        raise TypeError('book_content must be a str or None')
    if not isinstance(book_id, int):
        raise TypeError('book_id must be an int')
    if book_content is not None and not book_content.strip():
        raise ValueError('book_content must not be empty')
    if book_id < 0:
        raise ValueError('book_id must be positive')

    if book_content is None:
        book_content = get_book_content(book_id)

    cleaned_content = clean_book_content(book_content)
    sentences = segmentation(cleaned_content)

    scored_sentences = score_sentences(
        sentences,
        min_words=min_words,
        max_words=max_words,
        min_useful_words=min_useful_words,
        min_word_length=min_word_length,
        exclude_dialogue=exclude_dialogue,
        normalize_by_length=normalize_by_length,
        skip_first_sentences=skip_first_sentences,
    )

    summary = build_summary(
        scored_sentences,
        max_sentences=max_sentences,
        min_score=min_score,
    )

    return summary
