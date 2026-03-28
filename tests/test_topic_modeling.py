import unittest
from unittest import mock

from features.topic_modeling import topic_modeling


class TestTopicModeling(unittest.TestCase):
    def test_formats_topics(self):
        with mock.patch(
            'features.topic_modeling.extract_topics_from_book',
            return_value={1: ['tea', 'rabbit'], 2: ['queen']},
        ):
            result = topic_modeling(1, 'content')

        self.assertIn('=== Section 1 ===', result)
        self.assertIn('tea, rabbit', result)
        self.assertIn('=== Section 2 ===', result)
        self.assertIn('queen', result)


if __name__ == '__main__':
    unittest.main()
