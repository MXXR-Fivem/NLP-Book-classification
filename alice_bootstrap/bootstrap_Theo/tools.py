import argparse
import os
import string
import sys

import nltk
import pandas as pd
import requests
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

os.system('clear')

stop_words = set(stopwords.words('english'))


def init_args() -> None:
    """
    Initialisation of arguments and flags.

    # Parameters
        None

    # Returns
        None
    """

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--info', action='store_true')
    group.add_argument('--download', action='store_true')

    group.add_argument('--clean', action='store_true')
    parser.add_argument('--lower', action='store_true')

    group.add_argument('--tokenize', action='store_true')
    parser.add_argument('--sent', action='store_true')
    parser.add_argument('--stop', action='store_true')
    parser.add_argument('--punct', action='store_true')

    group.add_argument('--postag', action='store_true')

    group.add_argument('--normalize', action='store_true')
    parser.add_argument('--stem', action='store_true')

    parser.add_argument('value', nargs='?')

    global args
    args = parser.parse_args()

    return None


if __name__ == '__main__':
    init_args()


def download_book(book_id: int) -> str:
    """
    Download the book.

    # Parameters
        **book_id**: Gutenberg project unique identifier

    # Returns
        The file name of the book.
    """

    link = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'
    response = requests.get(link)

    if response.status_code != 200:
        return 'Invalid book id'

    with open(f'pgbook_{book_id}.txt', 'w+') as f:
        f.write(response.text)

    return f'pgbook_{book_id}.txt'


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'a'
    elif tag.startswith('V'):
        return 'v'
    elif tag.startswith('R'):
        return 'r'
    else:
        return 'n'


if args.info:
    if not args.value:
        print('Missing id for --info', file=sys.stderr)
        sys.exit(1)
    try:
        book_id = int(args.value[0])
    except ValueError, TypeError:
        print(f'Invalid id: {args.value[0]}', file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv('pg_catalog.csv')
    mask = df['Text#'].astype(int) == book_id
    filtered = df.loc[mask]

    if filtered.empty:
        print(f'No entry found for Text# {book_id}', file=sys.stderr)
        sys.exit(1)

    df_book = filtered.iloc[0]
    print(
        {
            'id': book_id,
            'title': df_book.get('Title'),
            'authors': df_book.get('Authors'),
            'bookshelves': df_book.get('Bookshelves'),
        }
    )
elif args.download:
    if not args.value:
        print('Missing id for --download', file=sys.stderr)
        sys.exit(1)
    try:
        title = download_book(int(args.value[0]))
    except ValueError, TypeError:
        print(f'Invalid id: {args.value[0]}', file=sys.stderr)
        sys.exit(1)
    print(title)
elif args.clean:
    text_input = args.value[0] if args.value else sys.stdin.read()

    cleaned_text = ' '.join(text_input.split())

    end_index = cleaned_text.find('*** END OF THE PROJECT GUTENBERG EBOOK')
    if end_index == -1:
        end_index = len(cleaned_text)

    start_index = cleaned_text.find('***', cleaned_text.find('***') + 3) + 3
    if start_index == -1 or start_index > end_index:
        start_index = 0

    cleaned_text = cleaned_text[start_index:end_index]
    print(cleaned_text.lower() if args.lower else cleaned_text)
elif args.tokenize:
    tokenized = sent_tokenize(args.value) if args.sent else args.value.split()

    if args.stop:
        tokenized = [word for word in tokenized if word not in stop_words]
        for i, _word in enumerate(tokenized):
            for character in string.punctuation:
                tokenized[i] = tokenized[i].replace(character, '')
    print(tokenized)
elif args.postag:
    tokens = word_tokenize(args.value)
    clean_tokens = [token for token in tokens if token not in string.punctuation]
    print(pos_tag(clean_tokens))
elif args.normalize:
    tokens = word_tokenize(args.value)
    if args.stem:
        ps = PorterStemmer()
        steammed_words = [ps.stem(word) for word in tokens]

        print(f'Original Text: {args.value}')
        print(f'Lemmatized Words: {steammed_words}')
    else:
        lemmatizer = WordNetLemmatizer()
        tagged_tokens = pos_tag(tokens)
        lemmatized_words = [
            lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in tagged_tokens
        ]

        print(f'Original Text: {args.value}')
        print(f'Lemmatized Words: {lemmatized_words}')
