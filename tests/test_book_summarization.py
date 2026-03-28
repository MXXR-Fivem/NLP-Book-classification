import unittest
from unittest import mock

from features.book_summarization import summarize_book


class TestBookSummarization(unittest.TestCase):
    def test_pipeline_calls_and_return(self):
        with (
            mock.patch(
                'features.book_summarization.get_book_content', return_value='raw'
            ) as get_content,
            mock.patch(
                'features.book_summarization.clean_book_content', return_value='clean'
            ) as clean,
            mock.patch(
                'features.book_summarization.segmentation', return_value=['s1', 's2']
            ) as segment,
            mock.patch(
                'features.book_summarization.score_sentences',
                return_value=[('s1', 1.0)],
            ) as score,
            mock.patch(
                'features.book_summarization.build_summary', return_value='summary'
            ) as build,
        ):
            result = summarize_book(12, book_content=None, max_sentences=2, min_score=0.1)

        get_content.assert_called_once_with(12)
        clean.assert_called_once_with('raw')
        segment.assert_called_once_with('clean')
        score.assert_called_once()
        build.assert_called_once_with([('s1', 1.0)], max_sentences=2, min_score=0.1)
        self.assertEqual(result, 'summary')

    def test_invalid_inputs(self):
        with self.assertRaises(TypeError):
            summarize_book('1', book_content='raw')
        with self.assertRaises(TypeError):
            summarize_book(1, book_content=123)
        with self.assertRaises(ValueError):
            summarize_book(1, book_content='  ')
        with self.assertRaises(ValueError):
            summarize_book(-1, book_content='raw')


if __name__ == '__main__':
    unittest.main()
