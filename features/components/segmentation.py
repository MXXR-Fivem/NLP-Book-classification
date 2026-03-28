import re


def segmentation(book_content: str) -> list[str]:
    """
    Split cleaned book content into sentences

    ## Parameters
        **book_content**: Book cleaned and normalized content

    ## Returns
        List of sentences made with the book content
    """

    if not isinstance(book_content, str):
        raise TypeError('book_content must be a str')
    if not book_content.strip():
        raise ValueError('book_content must not be empty')

    content = re.sub(r'\s+', ' ', book_content).strip()

    sentences = re.split(r'(?<=[.!?])\s', content)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    return sentences
