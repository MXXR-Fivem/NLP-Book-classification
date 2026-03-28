import streamlit as st

from shared import get_book_id, page_header, run_cached, setup_page, similar_books

setup_page('Similar', '🤔')
page_header('Similar Books', 'Cosine similarity | TF-IDF')

book_id = get_book_id()
if book_id and st.button('Find similar books'):
    titles = run_cached('similar', similar_books, book_id)
    st.divider()
    st.metric('Books found', len(titles))
    for i, title in enumerate(titles, 1):
        st.write(f'{i}. {title}')
