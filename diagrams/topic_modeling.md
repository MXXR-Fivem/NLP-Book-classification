## Topic Modeling

This feature extracts the dominants topics from each section of a book using Latent Dirichlet Allocation (LDA).

---

### Line-by-line Reasoning

#### 1. Constants and patterns

```python
Word_Per_Chunk = 1000
N_Topics = 8
N_Words = 9
CHAPTER_PATTERN = re.compile(
    r'(?<!\w)(CHAPTER|CHAP)\s+([IVXLCDM]+|[0-9]+)\.?',
    flags=re.IGNORECASE,
)
```

Default values control chunking and model output size. The regex detects chapter markers such as `CHAPTER IV` or `CHAP 3` in raw text.

#### 2. Build stopwords

```python
def build_stopwords():
    nltk.download('stopwords', quiet=True)
    base = set(stopwords.words('english'))
    return list(base | LITERARY_STOPWORDS)
```

Combines NLTK's standard English stopwords with a set of words to reduce noise in topic extraction.

#### 3. Split into chunks

```python
def split_into_chunks(text: str, words_per_chunk: int = Word_Per_Chunk):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), words_per_chunk):
        chunk = ' '.join(tokens[i : i + words_per_chunk])
        chunks.append(chunk)
    return chunks
```

Fallback segmentation when no chapter markers are found. The text is divided into fixed-size of chunks of words.

#### 4. Split book into chapters

```python
def split_book(text: str):
    ...
    all_boundaries = [m.start() for m in CHAPTER_PATTERN.finditer(text)]
    boundaries = []
    for pos in all_boundaries:
        if not boundaries or pos - boundaries[-1] > 500:
            boundaries.append(pos)
    if len(boundaries) <= 1:
        return split_into_chunks(text)
    ...
```

Detects chapter boundaries using the regex pattern. A minimum distance of 500 characters between boundaries avoids false positives. If fewer than two chapters are found, chunk splitting is used instead.

#### 5. Vectorize chapters

```python
vectorizer = CountVectorizer(
    stop_words=build_stopwords(),
    max_df=0.85,
    min_df=1,
    ngram_range=(1, 2),
    max_features=5000,
)
document_term_matrix = vectorizer.fit_transform(chapters)
```

Transforms each chapter into a cluster of words. Very frequent terms (`max_df=0.85`) are discarded to prevent dominant words from meddling with the model.

#### 6. Train LDA model

```python
actual_n_topics = min(n_topics, len(chapters))
lda = LatentDirichletAllocation(
    n_components=actual_n_topics,
    random_state=42,
    learning_method='batch',
    doc_topic_prior=0.1,
    topic_word_prior=0.01,
)
lda.fit(document_term_matrix)
```

Trains LDA on the document-term matrix. The number of topics is capped to the number of chapters to avoid empty topics. Low priors encourage focused topic distributions.

#### 7. Extract top words per topic

```python
def get_top_words(model, feature_names: list, n_words: int):
    topics = []
    for topic in model.components_:
        top_indices = topic.argsort()[-n_words:][::-1]
        words = [feature_names[i] for i in top_indices]
        topics.append(words)
    return topics
```

For each topic, the words with the highest weights in the topic-word distribution are extracted and returned as an ordered list.

#### 8. Assign dominant topic per section

```python
section_topic_matrix = lda.transform(document_term_matrix)
for i in range(len(chapters)):
    topic_index = section_topic_matrix[i].argmax()
    results[i + 1] = lda_topics[topic_index]
```

Each chapter is projected into the topic space. The topic with the highest probability is assigned as the dominant one for that section.

---

### Pipeline

```
Raw text -> Chapter splitting -> Stopword filtering -> CountVectorizer -> LDA training -> Topic assignment -> Dictionary
```

### Returns

```python
{
    1: ['sea', 'captain', 'ship', 'voyage', 'island', 'men', 'long john', 'treasure', 'crew'],
    2: ['doctor', 'livesey', 'map', 'squire', 'trelawney', 'chest', 'old', 'silver', 'pirates'],
    ...
}
```