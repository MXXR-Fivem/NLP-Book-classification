import streamlit as st

from features.components.get_book_content import get_book_content
from features.components.wordcloud import create_wordcloud
from shared import get_book_id, get_info, page_header, run_cached, setup_page

setup_page('Info', '📄')
page_header('📄', 'Book Info', 'Metadata · Gutenberg')

book_id = get_book_id()

if book_id and st.button('Fetch info'):
    result = run_cached('info', get_info, book_id)

    st.markdown(f'**Title** — {result.get("title")}')
    st.markdown(f'**Author** — {result.get("authors")}')
    st.markdown(f'**Bookshelves** — {result.get("bookshelves")}')

    text_content = get_book_content(book_id)

    if text_content:
        with st.spinner('Génération du WordCloud...'):
            path_to_cloud = create_wordcloud(book_id, text_content)
            st.image(f'{path_to_cloud}.png', caption=f'WordCloud du livre {book_id}')
    else:
        st.warning("Le contenu du texte n'est pas disponible pour générer le WordCloud.")
