import streamlit as st

from shared import fetch_cover, get_book_id, page_header, setup_page

setup_page('Cover', '🔬')
page_header('Cover', 'Book cover image | Gutenberg')

book_id = get_book_id()
if book_id and st.button('Fetch cover'):
    st.divider()
    try:
        response = fetch_cover(book_id, save_cover=False)
        st.image(response.content, caption=f'Cover — book {book_id}')
    except ValueError as e:
        st.error(str(e))
