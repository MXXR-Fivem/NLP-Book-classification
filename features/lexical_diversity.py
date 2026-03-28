import math
from collections import Counter

from .components.get_book_content import get_book_content
from .components.tokenize import tokenize


def lexical_diversity(book_id: int, book_content: str | None = None) -> dict[str, int | float]:
    """
    Get lexical informations about a book based on tokenization

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **book_content**: Book content

    ## Returns
        Dictionnary with lexical diversity metrics :

        "tok":int, # total number of word tokens
        "typ":int, # number of unique word tokens
        "hap":int, # number of word tokens occurring only once
        "ttr":float, # number of unique words tokens divided by number of word tokens
        "mwl":float, # mean number of characters per word token
        "mwf":float # number of word token divided by number of unique word tokens
    """

    if book_content is not None and not isinstance(book_content, str):
        raise TypeError('book_content must be str')
    elif not isinstance(book_id, int):
        raise TypeError('book_id mut be an int')
    elif book_content is not None and not book_content:
        raise ValueError('book_content need to be fill')
    elif book_id < 0:
        raise ValueError('book_id must be positive')

    if book_content is None:
        book_content = get_book_content(book_id)

    tokens = tokenize(text=book_content)
    tok = len(tokens)

    if tok == 0:
        return {
            'tok': 0,
            'typ': 0,
            'hap': 0,
            'ttr': 0.0,
            'mwl': 0.0,
            'mwf': 0.0,
            'guiraud': 0.0,
            'herdan_c': 0.0,
            'yules_k': 0.0,
            'yules_i': 0.0,
        }

    counts = Counter(tokens)

    typ = len(counts)
    hap = sum(1 for count in counts.values() if count == 1)
    ttr = typ / tok
    mwl = sum(len(word) for word in tokens) / tok
    mwf = tok / typ
    guiraud = typ / (tok**0.5)
    herdan_c = math.log(typ) / math.log(tok)
    yules_k = 10000 * (sum(freq**2 for freq in counts.values()) - tok) / (tok**2)
    yules_i = 1 / yules_k * 10000

    result = {
        'tok': tok,  # total number of word tokens
        'typ': typ,  # number of unique word tokens
        'hap': hap,  # number of word tokens occurring only once
        'ttr': ttr,  # number of unique words tokens divided by number of word tokens
        'mwl': mwl,  # mean number of characters per word token
        'mwf': mwf,  # number of word token divided by number of unique word tokens
        'guiraud': guiraud,  # lexical richness
        'herdan_c': herdan_c,  # lexical diversity (better for large texts)
        'yules_k': yules_k,  # It quantifies how varied the vocabulary is, with higher values indicating lower diversity
        'yules_i': yules_i,  # The reciprocal of Yule's K, higher score -> higher diversity
    }

    return result
