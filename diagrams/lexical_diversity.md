## Lexical Diversity

This feature computes lexical richness metrics from a book's tokenized text.
---

### Line-by-line Reasoning

#### 1. Input validation
```python
if book_content is not None and not isinstance(book_content, str):
	raise TypeError('book_content must be str')
elif not isinstance(book_id, int):
	raise TypeError('book_id mut be an int')
elif book_content is not None and not book_content:
	raise ValueError('book_content need to be fill')
elif book_id < 0:
	raise ValueError('book_id must be positive')
```
The function validates types and basic constraints to remove silent errors (ex: negative IDs or empty content).

#### 2. Retrieve content if missing

```python
if book_content is None:
	book_content = get_book_content(book_id)
```
If no content is provided, the book is fetched using the Gutenberg project unique identifier.

#### 3. Tokenize the content

```python
tokens = tokenize(text=book_content)
tok = len(tokens)
```
Tokenization transforms raw text into a list of word tokens used by all metrics.

#### 4. Empty-book short circuit

```python
if tok == 0:
	return {
		'tok': 0,
		'typ': 0,
		'hap': 0,
		'ttr': 0.0,
		'mwl': 0.0,
		'mwf': 0.0,
		'guiraud': 0.0,
		'herdan_c': 0.0,
		'yules_k': 0.0,
		'yules_i': 0.0,
	}
```
If no tokens exist, all metrics are returned as 0 to prevent division errors.

#### 5. Build frequency dictionary

```python
counts = Counter(tokens)
```
The `Counter` function create a dictionnary with token as key and token's frequency as value.

#### 6. Compute metrics

```python
typ = len(counts)
hap = sum(1 for count in counts.values() if count == 1)
ttr = typ / tok
mwl = sum(len(word) for word in tokens) / tok
mwf = tok / typ
guiraud = typ / (tok**0.5)
herdan_c = math.log(typ) / math.log(tok)
yules_k = 10000 * (sum(freq**2 for freq in counts.values()) - tok) / (tok**2)
yules_i = 1 / yules_k * 10000
```
- `tok`: number of tokens
- `typ`: number of unique tokens
- `hap`: number of tokens appearing once
- `ttr`: type-token ratio
- `mwl`: mean word length
- `mwf`: mean word frequency
- `guiraud`, `herdan_c`, `yules_k`, `yules_i`: standard richness metrics

#### 7. Return results

```python
return {
	'tok': tok,
	'typ': typ,
	'hap': hap,
	'ttr': ttr,
	'mwl': mwl,
	'mwf': mwf,
	'guiraud': guiraud,
	'herdan_c': herdan_c,
	'yules_k': yules_k,
	'yules_i': yules_i,
}
```
All metrics are returned in a single dictionary.

---
### Pipeline

```
Raw text -> Tokenize -> Frequency counting -> Metric computation -> Dictionary
```

### Returns

```python
{
	"tok": 12034,
	"typ": 2451,
	"hap": 1020,
	"ttr": 0.2037,
	"mwl": 4.12,
	"mwf": 4.91,
	"guiraud": 22.34,
	"herdan_c": 0.78,
	"yules_k": 87.1,
	"yules_i": 114.8,
}
```