from features.book_card import make_book_card
from features.book_summarization import summarize_book
from features.components.arguments.arguments_events import arguments_events
from features.components.arguments.arguments_initialisation import arguments_initialisation
from features.components.fetch_cover import fetch_cover
from features.components.get_info import get_info
from features.download_all_books import download_all_books
from features.lexical_diversity import lexical_diversity
from features.named_entities_recognition import named_entities
from features.similar_book import similar_books
from features.topic_modeling import topic_modeling
from features.clustering import clustering

args_action = {
    'lexdiv': {
        'action': lambda book_id: lexical_diversity(book_id),
        'sub_args': ['book_id'],
        'use_cache': True,
    },
    'clustering': {
        'action': lambda: clustering(),
    },
    'topics': {
        'action': lambda book_id: topic_modeling(book_id),
        'sub_args': ['book_id'],
        'use_cache': True,
    },
    'info': {
        'action': lambda book_id: get_info(book_id),
        'sub_args': ['book_id'],
        'use_cache': True,
    },
    'entities': {
        'action': lambda book_id: named_entities(book_id),
        'sub_args': ['book_id'],
        'use_cache': True,
    },
    'summarize': {
        'action': lambda book_id: summarize_book(book_id),
        'sub_args': ['book_id'],
        'use_cache': True,
    },
    'card': {
        'action': lambda book_id: make_book_card(book_id),
        'sub_args': ['book_id'],
        'use_cache': True,
    },
    'cover': {
        'action': lambda book_id: fetch_cover(book_id, True),
        'sub_args': ['book_id'],
        'use_cache': True,
    },
    'similar': {
        'action': lambda book_id: similar_books(book_id),
        'sub_args': ['book_id'],
        'use_cache': True,
    },
    'download': {
        'action': lambda author, category: (
            download_all_books(author, None)
            if author is not None
            else download_all_books(None, category)
        ),
        'sub_args': [
            'author',
            'category'
        ],
        'optional_args': [
            ('--author', str),
            ('--category', str)
        ],
    },
}

if __name__ == '__main__':
    args = arguments_initialisation(args_action)
    arguments_events(args, args_action)
