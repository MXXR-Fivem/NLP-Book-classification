from .contain_dialogue import contains_dialogue
from .tokenize import tokenize

DEFAULT_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'of', 'to', 'in', 'on', 'at', 'for', 'with', 'by', 'is', 'are', 'was',
    'were', 'be', 'been', 'it', 'this', 'that', 'these', 'those', 'as', 'from', 'not', 'he', 'she', 'they', 'we',
    'you', 'i', 'his', 'her', 'their', 'our', 'my', 'your', 'him', 'them', 'me', 'us', 'do', 'did', 'does', 'have',
    'has', 'had', 'so', 'if', 'then', 'than', 'into', 'out', 'up', 'down', 'all', 'any', 'what', 'which', 'who', 'whom',
    'when', 'where', 'why', 'how', 'can', 'could', 'would', 'should', 'shall', 'will', 'may', 'might', 'must', 'there',
    'here', 'too', 'very', 'just', 'about', 'over', 'under', 'again', 'once',
}


def score_sentences(
    sentences: list[str],
    min_words: int = 15,
    max_words: int = 40,
    min_useful_words: int = 7,
    min_word_length: int = 3,
    exclude_dialogue: bool = True,
    normalize_by_length: bool = True,
    skip_first_sentences: int = 12,
) -> list[tuple[str, float]]:
    """
    Score each sentence based on word frequency.

    ## Parameters
        **sentences**: List of sentences
        **min_words**: reject very short sentences
        **max_words**: reject very long sentences
        **min_useful_words**: reject sentences who has more or less useful words
        **min_word_length**: ignore very short tokens
        **exclude_dialogue**: reject sentences containing quotes
        **normalize_by_length**: divide score by useful word count
        **skip_first_sentences**: skip first n sentences

    ## Returns
        List of tuple (sentence, score)
    """

    if not isinstance(sentences, list):
        raise TypeError('sentences must be a list')
    elif not sentences:
        raise ValueError('sentences must not be empty')
    elif not all(isinstance(sentence, str) for sentence in sentences):
        raise TypeError('each sentence must be a str')
    elif not isinstance(min_words, int) or min_words <= 0:
        raise ValueError('min_words must be a positive int')
    elif not isinstance(max_words, int) or max_words <= 0:
        raise ValueError('max_words must be a positive int')
    elif min_words > max_words:
        raise ValueError('min_words must be lower than or equal to max_words')
    elif not isinstance(min_useful_words, int) or min_useful_words <= 0:
        raise ValueError('min_useful_words must be a positive int')
    elif not isinstance(min_word_length, int) or min_word_length <= 0:
        raise ValueError('min_word_length must be a positive int')
    elif not isinstance(exclude_dialogue, bool):
        raise TypeError('exclude_dialogue must be a bool')
    elif not isinstance(normalize_by_length, bool):
        raise TypeError('normalize_by_length must be a bool')
    elif not isinstance(skip_first_sentences, int):
        raise TypeError('skip_first_sentences must be an int')

    stopwords = DEFAULT_STOPWORDS

    word_frequencies: dict[str, int] = {}

    for sentence in sentences:
        if exclude_dialogue and contains_dialogue(sentence):
            continue

        words = tokenize(sentence)

        for word in words:
            if len(word) >= min_word_length and word not in stopwords:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1

    scored_sentences: list[tuple[str, float]] = []

    for index, sentence in enumerate(sentences):
        if index < skip_first_sentences:
            scored_sentences.append((sentence, 0.0))
            continue

        if exclude_dialogue and contains_dialogue(sentence):
            scored_sentences.append((sentence, 0.0))
            continue

        words = tokenize(sentence)
        useful_words = [
            word for word in words if len(word) >= min_word_length and word not in stopwords
        ]

        word_count = len(words)

        if word_count < min_words or word_count > max_words or len(useful_words) < min_useful_words:
            scored_sentences.append((sentence, 0.0))
            continue

        score = sum(word_frequencies.get(word, 0.0) for word in useful_words)

        if normalize_by_length:
            score = score / len(useful_words)

        scored_sentences.append((sentence, float(score)))

    return scored_sentences
