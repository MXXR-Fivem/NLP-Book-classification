import streamlit as st

from shared import get_book_id, page_header, run_cached, setup_page, topic_modeling

setup_page('Topics', '🤪')
page_header('Topic Modeling', 'LDA topic extraction | NLP')

book_id = get_book_id()
if book_id and st.button('Extract topics'):
    result = run_cached('topics', topic_modeling, book_id)
    st.divider()

    if isinstance(result, dict):
        for section_num in sorted(result):
            words = result.get(section_num, [])
            if isinstance(words, list):
                words_text = ', '.join(words)
            else:
                words_text = str(words)
            st.markdown(f'**Section {section_num}**')
            st.write(words_text)
    elif isinstance(result, str):
        for block in result.strip().split('\n\n'):
            lines = block.strip().splitlines()
            if not lines:
                continue
            header = lines[0].strip('= ').strip()
            words = lines[1] if len(lines) > 1 else ''
            st.markdown(f'**{header}**')
            st.write(words)
    else:
        st.error(f'Unexpected topic format: {type(result).__name__}')
