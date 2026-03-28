import streamlit as st

from features.book_card import make_book_card
from features.book_summarization import summarize_book
from features.components.fetch_cover import fetch_cover
from features.components.get_info import get_info
from features.download_all_books import download_all_books
from features.lexical_diversity import lexical_diversity
from features.named_entities_recognition import named_entities
from features.similar_book import similar_books
from features.topic_modeling import topic_modeling

__all__ = [
    "setup_page", "page_header", "get_book_id", "run_cached", "CSS",
    "make_book_card", "summarize_book", "fetch_cover", "get_info",
    "download_all_books", "lexical_diversity", "named_entities",
    "similar_books", "topic_modeling",
]

CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Fraunces:ital,wght@0,300;0,600;1,300&display=swap');

  html, body, { font-family: 'DM Mono', monospace; }

  .stApp { background-color: #0e0f0f; }

  [data-testid="stSidebar"] {
    background-color: #141516 !important;
    border-right: 1px solid #2a2b2b;
  }
  [data-testid="stSidebar"] * { font-family: 'DM Mono', monospace !important; }

  .block-container { padding: 2rem 2.5rem !important; max-width: 900px; }

  h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    color: #f0ede6 !important;
    font-weight: 300 !important;
  }
  h1 { font-size: 2.2rem !important; letter-spacing: -0.02em; }
  h2 { font-size: 1.4rem !important; }

  .stTextInput input, div[data-baseweb="input"] input {
    background-color: #1a1b1b !important;
    border: 1px solid #2e2f2f !important;
    border-radius: 4px !important;
    color: #c8c3b8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
  }
  .stTextInput input:focus { border-color: #b5a07a !important; box-shadow: none !important; }

  .stButton > button {
    background-color: #b5a07a !important;
    color: #0e0f0f !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    padding: 0.5rem 1.2rem !important;
  }
  .stButton > button:hover { background-color: #cdb992 !important; }

  [data-testid="stMetricValue"] {
    font-family: 'Fraunces', serif !important;
    color: #b5a07a !important;
    font-size: 1.8rem !important;
  }
  [data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    color: #666 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  hr { border-color: #2a2b2b !important; margin: 1.5rem 0 !important; }

  label { color: #888 !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.08em; }

  .stSuccess { background-color: #0f1f14 !important; border-color: #1e4d2b !important; color: #6dbf8a !important; }
  .stError   { background-color: #1f0f0f !important; border-color: #4d1e1e !important; color: #bf6d6d !important; }
  .stInfo    { background-color: #0f1520 !important; border-color: #1e3050 !important; color: #6d9fbf !important; }
  .stWarning { background-color: #1f1a0f !important; border-color: #4d3d1e !important; color: #bfa06d !important; }

  .stSpinner > div { border-top-color: #b5a07a !important; }

  p, li { color: #c8c3b8; font-size: 0.85rem; line-height: 1.7; }
  code {
    background: #1a1b1b !important; color: #b5a07a !important;
    border-radius: 3px; padding: 1px 5px;
    font-family: 'DM Mono', monospace !important;
  }

  .tag-pill {
    display: inline-block;
    background: #1e1f1f; border: 1px solid #2e2f2f; border-radius: 2px;
    padding: 2px 8px; font-size: 0.75rem; color: #b5a07a;
    margin: 2px 3px; font-family: 'DM Mono', monospace;
  }

  .result-card {
    background: #141516; border: 1px solid #2a2b2b; border-radius: 6px;
    padding: 1.2rem 1.5rem; margin: 1rem 0;
    color: #c8c3b8; font-size: 0.85rem; line-height: 1.7;
  }

  .page-eyebrow {
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.14em;
    color: #b5a07a; font-family: 'DM Mono', monospace; margin-bottom: 0.3rem;
  }

    [data-testid="stSidebarCollapseButton"] { display: none !important; } 

</style>
"""


# Helpers

def setup_page(title: str, icon: str) -> None:
    """
    Configure the Streamlit page and inject global CSS and sidebar.

    ## Parameters
        **title**: Page title
        **icon**: Page icon (emoji)

    ## Returns
        None
    """
    st.set_page_config(page_title=f"{title} · Gutenberg", page_icon=icon, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    _render_sidebar()


def page_header(icon: str, title: str, subtitle = None) -> None:
    """
    Render the page header.

    ## Parameters
        **icon**: Emoji displayed before the title
        **title**: Page title
        **subtitle**: Optional subtitle displayed above the title

    ## Returns
        None
    """
    st.markdown(f"<div class='page-eyebrow'>{subtitle}</div>", unsafe_allow_html=True)
    st.markdown(f"## {icon}&nbsp;&nbsp;{title}")


def get_book_id() -> int | None:
    """
    Get the current book ID from the sidebar input.

    ## Returns
        The book ID as an integer if valid, otherwise None.

    Displays a warning or error message if the value is missing or invalid.
    """
    raw = st.session_state.get("book_id", "").strip()
    if not raw:
        st.warning("Enter a Book ID in the sidebar.")
        return None
    if not raw.isdigit():
        st.error(f"Invalid Book ID: '{raw}' — must be a positive integer.")
        return None
    return int(raw)


def run_cached(fn_key: str, fn, *args):
    """
    Execute a function and cache the result in Streamlit session state.

    ## Parameters
        **fn_key**: Identifier for the cached function
        **fn**: Function to execute
        **args**: Arguments passed to the function

    ## Returns
        Cached result of the function execution

    The cache key combines the function identifier and arguments,
    allowing different results for different book IDs.
    """
    if "cache" not in st.session_state:
        st.session_state.cache = {}
    cache_key = f"{fn_key}_{'_'.join(str(a) for a in args)}"
    if cache_key not in st.session_state.cache:
        with st.spinner("Loading…"):
            st.session_state.cache[cache_key] = fn(*args)
    return st.session_state.cache[cache_key]


# Sidebar

def _render_sidebar() -> None:
    """
    Render the application sidebar.

    Includes:
        - Application title
        - Book ID input field
        - Display of the current active ID

    ## Returns
        None
    """
    with st.sidebar:
        st.markdown("""
        <div style='padding:0.8rem 0.2rem 1rem;'>
          <div style='font-family:"Fraunces",serif;font-size:1.2rem;font-weight:300;color:#f0ede6;line-height:1.3;'>
            Gutenberg<br><span style='color:#b5a07a;'>Explorer</span>
          </div>
          <div style='font-size:0.65rem;color:#444;text-transform:uppercase;letter-spacing:0.1em;margin-top:4px;'>
            Project Gutenberg · Analysis
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        bid = st.text_input(
            "Book ID",
            value=st.session_state.get("book_id", ""),
            placeholder="ex: 1342",
            help="Numeric identifier of the book on gutenberg.org/ebooks/<id>",
        )
        if bid:
            st.session_state.book_id = bid.strip()

        st.divider()
        st.markdown(
            f"<div style='font-size:0.68rem;color:#444;'>"
            f"Active ID: <span style='color:#b5a07a;'>"
            f"{st.session_state.get('book_id') or '—'}</span></div>",
            unsafe_allow_html=True,
        )
