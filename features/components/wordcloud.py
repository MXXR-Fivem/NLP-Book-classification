import matplotlib.pyplot as plt
from wordcloud import WordCloud


def create_wordcloud(
    book_id: int, text: str, width: int = 400, height: int = 400, margin: int = 0
) -> str:
    """
    Create wordcloud to represent most frequent words in a list of words.

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **text**: Book content
        **width** : Width of the word cloud figure
        **height** : Height of the word cloud figure
        **margin** : Margin of the word cloud figure

    ## Returns
        Wordcloud file path
    """

    if (
        not isinstance(book_id, int)
        or not isinstance(text, str)
        or not isinstance(width, int)
        or not isinstance(height, int)
        or not isinstance(margin, int)
    ):
        raise TypeError
    elif not text or height <= 0 or width <= 0 or margin < 0:
        raise ValueError

    wordcloud_path = f'./alice_assets/plots/{book_id}'

    word_cloud = WordCloud(width=width, height=height, margin=margin).generate(text)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.savefig(wordcloud_path)

    return wordcloud_path
