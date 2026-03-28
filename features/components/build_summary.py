def build_summary(
    scored_sentences: list[tuple[str, float]],
    max_sentences: int = 3,
    min_score: float = 0.0,
) -> str:
    """
    Build a summary from scored sentences.

    ## Parameters
        **scored_sentences**: List of tuples (sentence, score)
        **max_sentences**: number of sentences kept
        **min_score**: ignore sentences with score <= min_score

    ## Returns
        The summary
    """

    if not isinstance(scored_sentences, list):
        raise TypeError('scored_sentences must be a list')
    if not scored_sentences:
        raise ValueError('scored_sentences must not be empty')
    if not isinstance(max_sentences, int):
        raise TypeError('max_sentences must be an int')
    if max_sentences <= 0:
        raise ValueError('max_sentences must be positive')
    if not isinstance(min_score, (int, float)):
        raise TypeError('min_score must be numeric')

    indexed_sentences = [
        (index, sentence, score)
        for index, (sentence, score) in enumerate(scored_sentences)
        if isinstance(sentence, str) and isinstance(score, (int, float)) and score > min_score
    ]

    top_sentences = sorted(indexed_sentences, key=lambda item: item[2], reverse=True)

    selected = []
    seen = set()

    for index, sentence, score in top_sentences:
        normalized_sentence = sentence.strip().lower()

        if normalized_sentence in seen:
            continue

        selected.append((index, sentence, score))
        seen.add(normalized_sentence)

        if len(selected) >= max_sentences:
            break

    selected.sort(key=lambda item: item[0])

    summary = ' '.join(sentence.strip() for _, sentence, _ in selected).strip()

    return summary
