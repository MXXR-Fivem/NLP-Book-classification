import streamlit as st

from shared import CSS, _render_sidebar

st.set_page_config(
    page_title='Alice in Wonderlands Dashboard',
    page_icon='📚',
    layout='wide',
)
st.markdown(CSS, unsafe_allow_html=True)
_render_sidebar()

st.markdown(
    """
		<div style='padding:3rem 0 1rem;'>
		<div style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.14em;color:#b5a07a;margin-bottom:0.5rem;'>
			Project Gutenberg | Analyse
		</div>
		<div style='font-family:"Fraunces",serif;font-size:2.6rem;font-weight:300;color:#f0ede6;line-height:1.2;'>
			Gutenberg Explorer
		</div>
		<p style='color:#555;margin-top:1rem;max-width:500px;'>
			Select a Book ID in the sidebar, then select a functionality in the menu.
		</p>
		</div>
	""",
    unsafe_allow_html=True,
)

st.divider()

FEATURES = [
    ('Info', 'Métadonnées du livre'),
    ('Résumé', 'Résumé généré par IA'),
    ('Div. lexicale', 'Statistiques de vocabulaire'),
    ('Topics', 'Modélisation thématique LDA'),
    ('Entités', "Reconnaissance d'entités nommées"),
    ('Fiche livre', 'Carte récapitulative'),
    ('Couverture', 'Image de couverture'),
    ('Similaires', 'Livres proches par embeddings'),
    ('Télécharger', 'Téléchargement par lot'),
]

cols = st.columns(2)
for i, (name, desc) in enumerate(FEATURES):
    with cols[i % 2]:
        st.markdown(
            f"""
				<div class='result-card' style='padding:14px 16px;margin-bottom:8px;'>
				<div style='margin-bottom:4px;'>
					<span style='font-family:"Fraunces",serif;font-weight:300;color:#f0ede6;font-size:1rem;'>{name}</span>
				</div>
					<div style='font-size:0.73rem;color:#555;'>{desc}</div>
				</div>
			""",
            unsafe_allow_html=True,
        )
