import pandas as pd

from .components.download import download_book
from .components.get_offline_catalog import get_offline_catalogue


def download_all_books(author: str | None, category: str | None) -> list[str]:
    """
    Download all books [co-]written by a given author, or from a specific category

    ## Parameters
        **author**: Author name

    ## Returns
        The list of downloaded books path
    """

    if not (isinstance(author, str) or author is None) or not (
        isinstance(category, str) or category is None
    ):
        raise TypeError('Invalid type for author or category')
    elif not author and not category:
        raise ValueError('you must provide at least an author name or a category.')

    downloaded_files = []
    df_books = pd.read_csv(get_offline_catalogue())
    books_to_download = []

    if author is not None:
        author = ', '.join(author.split(' '))

    books_to_download = df_books[
        df_books[author and 'Authors' or 'Bookshelves'].str.contains(
            author or category, case=False, na=False
        )
    ]['Text#'].to_list()

    for book_id in books_to_download:
        book_path = download_book(book_id)

        if book_path is not None:
            downloaded_files.append(book_path)

    return downloaded_files
