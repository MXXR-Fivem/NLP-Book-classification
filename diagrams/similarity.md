## Similar Books

This feature identifies books from a collection that are most similar to a given target book, using TF-IDF vectorization and cosine similarity.

---

### Line-by-line Reasoning

#### 1. Constants and collection

```python
N_SIMILAR = 5
BOOK_COLLECTION = {
    11: "Alice's Adventures in Wonderland",
    ...
    345: "Dracula",
}
```

`N_SIMILAR` controls how many recommendations are returned. `BOOK_COLLECTION` is a fixed set of 20 books used as the reference for similarity comparisons.

#### 2. Build stopwords

```python
def build_stopwords():
    nltk.download('stopwords', quiet=True)
    base = set(stopwords.words('english'))
    return list(base | LITERARY_STOPWORDS)
```

Combines NLTK's standard English stopwords with an additionnal stopword list to reduce noise during vectorization.

#### 3. Load all books

```python
def load_all_books(book_ids: list):
    ids = []
    texts = []
    for book_id in book_ids:
        content = get_book_content(book_id)
        if content:
            ids.append(book_id)
            texts.append(content)
    return ids, texts
```

Downloads each book in the collection from Project Gutenberg. Books that fail to load are skipped so that a single unavailable title does not interrupt the process.

#### 4. Vectorize books

```python
def vectorize_books(texts: list):
    vectorizer = TfidfVectorizer(
        stop_words=build_stopwords(),
        max_df=0.85,
        min_df=1,
        ngram_range=(1, 2),
        max_features=5000,
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer
```

Transforms the collection into a matrix. High-frequency terms are filtered out, and the fitted vectorizer is returned so that external books can later be projected into the same vector space.

#### 5. Handle internal vs external books

```python
if book_id in loaded_ids:
    target_index = loaded_ids.index(book_id)
    target_vector = tfidf_matrix[target_index]
else:
    target_text = book_content or get_book_content(book_id)
    target_vector = vectorizer.transform([target_text])
```

If the target book belongs to the collection, its row is reused directly. If it is an external book, its text is downloaded and projected with `transform()` (not `fit_transform()`) to preserve the collection's vocabulary and IDF weights.

#### 6. Compute cosine similarity and rank results

```python
scores = cosine_similarity(target_vector, tfidf_matrix).flatten()
ranked = []
for idx, score in enumerate(scores):
    if book_id in loaded_ids and idx == loaded_ids.index(book_id):
        continue
    ranked.append((idx, score))
ranked.sort(key=lambda pair: pair[1], reverse=True)
```

Cosine similarity is computed between the target vector and every book in the collection matrix. The target book itself is excluded from results if it belongs to the collection. Results are sorted by decreasing similarity score.

#### 7. Return top similar titles

```python
for idx, _score in ranked[:n_similar]:
    similar_book_id = loaded_ids[idx]
    similar_titles.append(BOOK_COLLECTION[similar_book_id])
return similar_titles
```

The top `n_similar` book titles are extracted from the ranked list and returned as a formatted list of strings.

---

### Pipeline

```
Book IDs -> Download texts -> TF-IDF vectorization -> Cosine similarity -> Ranking -> Title list
```

### Returns

```python
[
    "The Adventures of Sherlock Holmes",
    "The Memoirs of Sherlock Holmes",
    "The Return of Sherlock Holmes",
    "Poirot Investigates",
    "The Mysterious Affair at Styles",
]
```