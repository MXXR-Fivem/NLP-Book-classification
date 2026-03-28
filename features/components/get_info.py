import pandas as pd

from .get_offline_catalog import get_offline_catalogue


def get_info(book_id: int) -> dict[str, str]:
    """
    Get main informations about a book

    ## Parameters
        **book_id**: Gutenberg project unique identifier

    ## Returns
        Dictionnary of book informations
    """

    if not isinstance(book_id, int):
        raise TypeError('book_id must be int')
    elif book_id < 0:
        raise ValueError

    df = pd.read_csv(get_offline_catalogue())
    mask = df['Text#'].astype(int) == book_id
    filtered = df.loc[mask]

    if filtered.empty:
        raise ValueError(f'No entry found for id {book_id}')

    df_book = filtered.iloc[0]

    result = {
        'id': book_id,
        'title': df_book.get('Title'),
        'authors': df_book.get('Authors'),
        'bookshelves': df_book.get('Bookshelves'),
    }

    return result
