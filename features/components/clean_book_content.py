def clean_book_content(book_content: str) -> str:
    """
    Clean the book content

    ## Parameters
        **book_content**: The book text

    ## Returns
        Cleaned book content
    """

    if not isinstance(book_content, str):
        raise TypeError('book_content must be a str')
    if not book_content.strip():
        raise ValueError('book_content must not be empty')

    content = book_content.replace('\r\n', '\n').replace('\r', '\n').replace('__', '')
    lines = [line.strip() for line in content.split('\n')]

    cleaned_lines = []
    previous_empty = False

    for line in lines:
        is_empty = line == ''

        if is_empty:
            if not previous_empty:
                cleaned_lines.append('')
            previous_empty = True
        else:
            cleaned_lines.append(line)
            previous_empty = False

    return '\n'.join(cleaned_lines).strip()
