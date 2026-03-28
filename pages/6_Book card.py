from pathlib import Path

import streamlit as st

from shared import get_book_id, make_book_card, page_header, run_cached, setup_page

setup_page('Book Card', '📔')
page_header('Book Card', 'Full analysis card | PDF export')

book_id = get_book_id()
if book_id and st.button('Generate card'):
    result = run_cached('card', make_book_card, book_id)
    st.divider()

    info = result.get('info', {})
    st.markdown(f'**{info.get("title", "—")}** — {info.get("author", "—")}')

    lexdiv = result.get('lexdiv', {})
    c1, c2, c3 = st.columns(3)
    c1.metric('TTR', f'{lexdiv.get("ttr", 0):.4f}')
    c2.metric('Unique types', f'{lexdiv.get("typ", 0):,}')
    c3.metric('Total tokens', f'{lexdiv.get("tok", 0):,}')

    st.markdown('**Summary**')
    st.write(result.get('summary', '—'))

    similar = result.get('similar', [])
    if similar:
        st.markdown('**Similar books**')
        for title in similar:
            st.write(f'- {title}')

    entities = result.get('entities', {})
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('**Characters**')
        for name in sorted(entities.get('characters', [])):
            st.write(f'- {name}')
    with col2:
        st.markdown('**Locations**')
        for place in sorted(entities.get('locations', [])):
            st.write(f'- {place}')

    st.success('PDF card saved to alice_assets/book_cards/')

    pdf_path = Path(f'alice_assets/book_cards/card_{book_id}.pdf')

    if pdf_path.exists():
        with open(pdf_path, 'rb') as f:
            st.download_button(
                label='Download PDF card',
                data=f,
                file_name=f'card_{book_id}.pdf',
                mime='application/pdf',
            )
