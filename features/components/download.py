import requests


def download_book(book_id: int) -> str:
    """
    Download the book.

    ## Parameters
        **book_id**: Gutenberg project unique identifier

    ## Returns
        The file path of the book.
    """

    if not isinstance(book_id, int):
        raise TypeError('book_id must be int')
    elif book_id < 0:
        raise ValueError

    link = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'
    response = requests.get(link)

    if response.status_code != 200:
        print(f'Invalid book id : {book_id}')
        return

    with open(f'./alice_assets/books/pgbook_{book_id}.txt', 'w+') as file:
        file.write(response.text)

    return f'./alice_assets/books/pgbook_{book_id}.txt'
