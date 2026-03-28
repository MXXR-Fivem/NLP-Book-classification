import streamlit as st

from shared import get_book_id, named_entities, page_header, run_cached, setup_page

setup_page('Entities', '📄')
page_header('Named Entities', 'Character & location recognition | spaCy')

book_id = get_book_id()
if book_id and st.button('Recognize entities'):
    result = run_cached('entities', named_entities, book_id)
    st.divider()

    characters = result.get('characters', [])
    locations = result.get('locations', [])

    c1, c2 = st.columns(2)
    c1.metric('Characters', len(characters))
    c2.metric('Locations', len(locations))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('**Characters**')
        for name in sorted(characters):
            st.write(f'- {name}')
    with col2:
        st.markdown('**Locations**')
        for place in sorted(locations):
            st.write(f'- {place}')
