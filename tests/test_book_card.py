import unittest
from unittest import mock

from features.book_card import make_book_card


class TestBookCard(unittest.TestCase):
    def test_invalid_inputs(self):
        with self.assertRaises(TypeError):
            make_book_card('1')
        with self.assertRaises(ValueError):
            make_book_card(-1)

    def test_returns_card_and_calls_wordcloud(self):
        with (
            mock.patch(
                'features.book_card.get_book_content', return_value='content'
            ) as get_content,
            mock.patch('features.book_card.get_info', return_value={'id': 11, 'title': 'Alice'}),
            mock.patch('features.book_card.lexical_diversity', return_value={'tok': 1}),
            mock.patch('features.book_card.topic_modeling', return_value='topics'),
            mock.patch(
                'features.book_card.named_entities',
                return_value={'characters': [], 'locations': []},
            ),
            mock.patch('features.book_card.summarize_book', return_value='summary'),
            mock.patch('features.book_card.similar_books', return_value=['id2']),
            mock.patch('features.book_card.create_wordcloud') as create_wordcloud,
        ):
            result = make_book_card(12)

        get_content.assert_called_once_with(12)
        create_wordcloud.assert_called_once_with(12, 'content')
        self.assertEqual(result['info'], {'id': 11, 'title': 'Alice'})
        self.assertEqual(result['lexdiv'], {'tok': 1})
        self.assertEqual(result['topics'], 'topics')
        self.assertEqual(result['entities'], {'characters': [], 'locations': []})
        self.assertEqual(result['summary'], 'summary')
        self.assertEqual(result['similar'], ['id2'])


if __name__ == '__main__':
    unittest.main()
