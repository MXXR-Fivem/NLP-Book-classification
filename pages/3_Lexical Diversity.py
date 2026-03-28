import streamlit as st

from features.components.get_book_content import get_book_content
from shared import get_book_id, lexical_diversity, page_header, run_cached, setup_page

setup_page('Lexical Diversity', '📖')
page_header('Lexical Diversity', 'Vocabulary statistics | NLP')

book_id = get_book_id()
book_content = get_book_content(book_id)
if book_id and st.button('Analyze'):
    result = run_cached('lexdiv', lexical_diversity, book_id, book_content)
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Total tokens', f'{result.get("tok", 0):,}', help='Total number of word tokens')
    c2.metric('Unique types', f'{result.get("typ", 0):,}', help='Number of distinct word forms')
    c3.metric('Hapax', f'{result.get("hap", 0):,}', help='Words appearing only once')
    c4.metric(
        'Avg word length', f'{result.get("mwl", 0):.2f}', help='Mean number of characters per token'
    )

    c5, c6, c7, c8 = st.columns(4)
    c5.metric('TTR', f'{result.get("ttr", 0):.4f}', help='Type-Token Ratio — unique / total')
    c6.metric('Guiraud', f'{result.get("guiraud", 0):.3f}', help='Lexical richness — typ / √tok')
    c7.metric(
        'Herdan C',
        f'{result.get("herdan_c", 0):.4f}',
        help='Log typ / log tok — reliable on long texts',
    )
    c8.metric(
        "Yule's I", f'{result.get("yules_i", 0):.2f}', help="1 / Yule's K — higher = more diverse"
    )

    ttr = result.get('ttr', 0)
    label = (
        'Very rich vocabulary'
        if ttr > 0.15
        else 'Moderately varied vocabulary'
        if ttr > 0.08
        else 'Repetitive vocabulary / long text'
    )
    st.info(f'TTR interpretation: **{label}**')
