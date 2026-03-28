def remove_gutenberg_tags(book_content: str) -> str:
    """
    Remove gutenberg header and footer

    ## Parameters
        **book_content**: Book content

    ## Returns
        Cleaned book content
    """

    if not isinstance(book_content, str):
        raise TypeError('book_content must be str')
    elif not book_content:
        raise ValueError

    cleaned_text = ' '.join(book_content.split())

    end_index = cleaned_text.find('*** END OF')
    if end_index == -1:
        end_index = len(cleaned_text)

    start_index = cleaned_text.find('***', cleaned_text.find('***') + 3) + 3
    if start_index == -1 or start_index > end_index:
        start_index = 0

    cleaned_text = cleaned_text[start_index:end_index]

    return cleaned_text
