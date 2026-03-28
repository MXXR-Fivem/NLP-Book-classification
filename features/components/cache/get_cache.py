import json
from pathlib import Path

import pandas as pd


def get_cache(
    book_id: int,
    feature_name: str,
    csv_path: str = 'alice_assets/cache/alice_cache.csv'
) -> str | dict | None:
    """
    Return cached feature for a book id, or None if unavailable.

    ## Parameters
        **book_id**: Gutenberg project unique identifier
        **feature_name**: Feature name
        **csv_path**: CSV file path

    ## Returns
        Feature data
    """

    if not isinstance(book_id, int):
        raise TypeError('book_id must be an int')
    if not isinstance(feature_name, str):
        raise TypeError('feature_name must be str')
    if not isinstance(csv_path, str):
        raise TypeError('csv_path must be str')
    if book_id < 0:
        raise ValueError('book_id must be positive')

    csv_file = Path(csv_path)
    if not csv_file.exists():
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        df_cache = pd.DataFrame(columns=['id', feature_name])
        df_cache.to_csv(csv_file, index=False)
        return None

    try:
        df_cache = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        return None

    if 'id' not in df_cache.columns or feature_name not in df_cache.columns:
        return None

    book_rows = df_cache.loc[df_cache['id'] == book_id]
    if book_rows.empty:
        return None

    feature_value = book_rows.iloc[0][feature_name]
    if pd.isna(feature_value):
        return None

    if isinstance(feature_value, str):
        try:
            return json.loads(feature_value)
        except json.JSONDecodeError:
            return feature_value

    return feature_value
