import unittest
from unittest import mock

import pandas as pd

from features.download_all_books import download_all_books


class TestDownloadAllBooks(unittest.TestCase):
    def test_invalid_inputs(self):
        with self.assertRaises(TypeError):
            download_all_books(123, None)
        with self.assertRaises(TypeError):
            download_all_books(None, 123)
        with self.assertRaises(ValueError):
            download_all_books(None, None)

    def test_downloads_matching_books(self):
        df = pd.DataFrame(
            {
                'Authors': ['Lewis, Carroll', 'Other, Author'],
                'Bookshelves': ['Fantasy', 'History'],
                'Text#': [1, 2],
            }
        )

        with (
            mock.patch(
                'features.download_all_books.get_offline_catalogue', return_value='file.csv'
            ),
            mock.patch('features.download_all_books.pd.read_csv', return_value=df),
            mock.patch('features.download_all_books.download_book', return_value='book1.txt'),
        ):
            result = download_all_books('Lewis Carroll', None)

        self.assertEqual(result, ['book1.txt'])


if __name__ == '__main__':
    unittest.main()
