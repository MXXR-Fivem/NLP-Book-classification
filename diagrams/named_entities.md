## Named Entities Recognition

This feature identifies characters and locations mentioned in a book.

### Approaches Tested

#### Version 1 — NLTK (no model)

A first version was developed using `nltk` only, without any heavy model:

```python
from nltk import ne_chunk, pos_tag, word_tokenize
tree = ne_chunk(pos_tag(word_tokenize(chunk)))
```
**Result**: less accurate — many false positives such as `'Fury'`, `'Soup'`, `'Mystery'` detected as characters. Abandoned in favor of spaCy.

#### Version 2 — spaCy `en_core_web_md` (final version)

More accurate and still considered a lightweight model.
---

### Line-by-line Reasoning

#### 1. Model loading

```python
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")
```
We attempt to load the spaCy model. If it is not installed on the machine (`OSError`), it is downloaded automatically before being reloaded. This ensures the program runs **on any machine** without manual configuration.

#### 2. Retrieving the book content

```python
book_content = book_content or get_book_content(book_id)
```
If the book content is already provided, it is used directly. Otherwise, it is fetched via `get_book_content`. This avoids downloading the book multiple times when chaining several features.

#### 3. Splitting into chunks

```python
chunk_size = 10000
chunks = [book_content[i:i+chunk_size] for i in range(0, len(book_content), chunk_size)]
```
A full book can exceed 150,000 characters. Passing the entire text to spaCy at once would be slow and memory-intensive. It is therefore split into 10,000-character chunks processed one at a time.

#### 4. Using `set()` instead of `list()`

```python
characters = set()
locations = set()
```
A `set` cannot contain duplicates — `Alice` appears hundreds of times in the book but will only be added once. More efficient than filtering duplicates after the fact with `list(set(...))`.

#### 5. Entity filtering

```python
for ent in doc.ents:
    if ent.label_ == "PERSON" and "\n" not in ent.text and not ent.text.startswith("CHAPTER"):
        characters.add(ent.text)
    elif ent.label_ in ["GPE", "LOC"] and "\n" not in ent.text:
        locations.add(ent.text)
```
- `ent.label_ == "PERSON"` → filters characters
- `"\n" not in ent.text` → removes chapter titles incorrectly detected as entities, e.g. `"CHAPTER I.\nDown"`
- `not ent.text.startswith("CHAPTER")` → additional filter for chapter headings
- `ent.label_ in ["GPE", "LOC"]` → `GPE` = geopolitical locations (countries, cities), `LOC` = physical locations

#### 6. Returning the dictionary

```python
return {
    "characters": list(characters),
    "locations": list(locations)
}
```
The `set` objects are converted to `list` since the expected return format is a list of strings.
---

### Pipeline

```
Raw text → Chunk splitting → spaCy NER → Label filtering → Dictionary
```

### Returns

```python
{
    "characters": ["Alice", "Queen", ...],
    "locations": ["London", "Wonderland", ...]
}
```