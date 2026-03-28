import re


def tokenize(text: str) -> list[(str, str)]:
    """
    Tokenize a text

    ## Parameters
        **text**: The text that will be tokenized
        **remove_punct**: Toggle suppression of punctuation in the tokens

    ## Returns
        The list of the generated tokens
    """

    if not isinstance(text, str):
        raise TypeError
    elif not text:
        raise ValueError

    return re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
