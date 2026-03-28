import unittest
from unittest import mock

from features.lexical_diversity import lexical_diversity


class TestLexicalDiversity(unittest.TestCase):
    def test_metrics_for_simple_text(self):
        result = lexical_diversity(1, 'aa aa bb cc')

        self.assertEqual(result['tok'], 4)
        self.assertEqual(result['typ'], 3)
        self.assertEqual(result['hap'], 2)
        self.assertAlmostEqual(result['ttr'], 0.75)

    def test_empty_token_list_returns_zeros(self):
        result = lexical_diversity(1, 'a')

        self.assertEqual(result['tok'], 0)
        self.assertEqual(result['ttr'], 0.0)

    def test_invalid_inputs(self):
        with self.assertRaises(TypeError):
            lexical_diversity(1, 123)
        with self.assertRaises(TypeError):
            lexical_diversity('1', 'aa')
        with self.assertRaises(ValueError):
            lexical_diversity(1, '')
        with self.assertRaises(ValueError):
            lexical_diversity(-1, 'aa')

    def test_fetches_content_when_missing(self):
        with mock.patch(
            'features.lexical_diversity.get_book_content', return_value='aa aa'
        ) as get_content:
            result = lexical_diversity(42, None)

        get_content.assert_called_once_with(42)
        self.assertEqual(result['tok'], 2)
        self.assertEqual(result['typ'], 1)
        self.assertEqual(result['hap'], 0)


if __name__ == '__main__':
    unittest.main()
