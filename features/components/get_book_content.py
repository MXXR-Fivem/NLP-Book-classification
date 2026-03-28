import requests

from .remove_gutenberg_tags import remove_gutenberg_tags


def get_book_content(book_id: int) -> str:
    """
    Get the book content.

    ## Parameters
        **book_id**: Gutenberg project unique identifier

    ## Returns
        The book content.
    """

    if not isinstance(book_id, int):
        raise TypeError('book_id must be int')
    elif book_id < 0:
        raise ValueError

    link = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'
    response = requests.get(link)

    if response.status_code != 200:
        raise ValueError('Invalid book id')

    book_content = remove_gutenberg_tags(response.text)

    return book_content
