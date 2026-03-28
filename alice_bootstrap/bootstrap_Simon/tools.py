import argparse
import re
import string

import nltk
import pandas as pd
import requests
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('stopwords')
nltk.download('wordnet')


def get_pos(tag):
    if tag.startswith('V'):
        return 'v'
    elif tag.startswith('J'):
        return 'a'
    elif tag.startswith('R'):
        return 'r'
    else:
        return 'n'


mots_vides = set(stopwords.words('english'))
parser = argparse.ArgumentParser()
parser.add_argument('--info', type=int)
parser.add_argument('--download')
parser.add_argument('--lower', action='store_true')
parser.add_argument('--clean')
parser.add_argument('--tokenize')
parser.add_argument('--sent', action='store_true')
parser.add_argument('--stop', action='store_true')
parser.add_argument('--punct', action='store_true')
parser.add_argument('--postag', nargs='+')
parser.add_argument('--normalize', nargs='+')
parser.add_argument('--stem', action='store_true')

args = parser.parse_args()

df = pd.read_csv('pg_catalog.csv', sep=',')

if args.info:
    ligne = df[df['Text#'] == args.info]
    liste = ligne[['Title', 'Authors', 'Bookshelves']].to_dict(orient='records')

    result = {
        'id': args.info,
        'title': liste[0]['Title'],
        'authors': liste[0]['Authors'],
        'bookshelves': liste[0]['Bookshelves'],
    }
    print(result)
elif args.download:
    ID = args.download
    url = f'https://www.gutenberg.org/files/{ID}/{ID}-0.txt'
    response = requests.get(f'{url}')
    with open(f'{ID}.txt', 'w') as f:
        f.write(response.text)
elif args.clean:
    cleaned_text = re.sub(r'\s+', ' ', f'{args.clean}')
    if args.lower:
        cleaned_text = cleaned_text.lower()
    print(cleaned_text)
elif args.tokenize:
    token = sent_tokenize(args.tokenize) if args.sent else word_tokenize(args.tokenize)
    if args.stop:
        token = [mot for mot in token if mot not in mots_vides]
    if args.punct:
        token = [mot for mot in token if mot not in string.punctuation]
    print(token)
elif args.postag:
    result = nltk.pos_tag(args.postag)
    print(result)
elif args.normalize:
    if args.stem:
        ps = PorterStemmer()
        token = [ps.stem(mot) for mot in args.normalize]
        print(token)
    else:
        lemmatizer = WordNetLemmatizer()
        tagged = nltk.pos_tag(args.normalize)
        token = [lemmatizer.lemmatize(mot, pos=get_pos(tag)) for mot, tag in tagged]
        print(token)
