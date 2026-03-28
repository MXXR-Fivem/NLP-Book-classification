from .book_summarization import summarize_book
from .components.get_book_content import get_book_content
from .components.get_info import get_info
from .components.make_pdf_card import make_pdf_card
from .components.wordcloud import create_wordcloud
from .lexical_diversity import lexical_diversity
from .named_entities_recognition import named_entities
from .similar_book import similar_books
from .topic_modeling import topic_modeling


def make_book_card(book_id: int) -> dict[str, dict | list | str]:
    """
    Make book card summary

    ## Parameters
        **book_id**: Gutenberg project unique identifier

    ## Returns
        Book card dictionnary
    """

    if not isinstance(book_id, int):
        raise TypeError('book_id must be int')
    elif book_id < 0:
        raise ValueError

    book_content = get_book_content(book_id)

    book_card = {
        'info': get_info(book_id),
        'lexdiv': lexical_diversity(book_id, book_content),
        'topics': topic_modeling(book_id, book_content),
        'entities': named_entities(book_id, book_content),
        'summary': summarize_book(book_id, book_content),
        'similar': similar_books(book_id, book_content),
    }

    create_wordcloud(
        book_id,
        book_content,
    )

    make_pdf_card(book_card)

    return book_card
