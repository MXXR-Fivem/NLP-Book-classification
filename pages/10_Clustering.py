import streamlit as st
from pathlib import Path
from features.clustering import clustering

from shared import setup_page, page_header

setup_page("Clustering", "📊")
page_header("Book Clustering", "Cluster downloaded books with TF-IDF & KMeans")

st.write("""
This page allows you to cluster books you have downloaded. 
Provide the folder containing the `.txt` books and choose the number of clusters.
""")

# Inputs
books_dir = st.text_input("Books directory", value="alice_assets/books")
output_path = st.text_input("Output image path", value="alice_assets/plots/clustering.png")
n_clusters = st.number_input("Number of clusters", min_value=1, max_value=20, value=3, step=1)
max_features = st.number_input("TF-IDF max features", min_value=100, max_value=5000, value=1000, step=100)

if st.button("Run Clustering"):
    with st.spinner("Clustering books…"):
        try:
            result = clustering(
                books_dir=books_dir,
                output_path=output_path,
                n_clusters=n_clusters,
                max_features=max_features
            )
            st.success(f"Clustering finished! Output saved at: {result['output_path']}")
            st.image(result['output_path'])
            
            st.write("Cluster labels and titles:")
            for label, title in zip(result['labels'], result['titles']):
                st.write(f"Cluster {label}: {title}")

        except Exception as e:
            st.error(f"Error: {str(e)}")