import requests


def fetch_cover(book_id: int, save_cover: bool) -> requests.Response:
    """
    Fetch the cover of a specific book.

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **save_cover**: Indicate if you want to save the cover in png

    ## Returns
        Http response (containing the image in .content)
    """

    if not isinstance(book_id, int):
        raise TypeError('book_id must be an int')
    elif book_id < 0:
        raise ValueError('book_id must be positive')

    response = requests.get(
        f'https://www.gutenberg.org/cache/epub/{book_id}/images/cover.jpg', stream=True
    )

    if response.status_code != 200:
        raise ValueError('Invalid book id (not found)')

    if save_cover:
        with open(f'./alice_assets/covers/cover_{book_id}.png', 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

    return response
