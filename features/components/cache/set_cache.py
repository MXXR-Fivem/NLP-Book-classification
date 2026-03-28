import json
from pathlib import Path

import pandas as pd


def set_cache(
    book_id: int,
    feature_name: str,
    feature_value: str | dict,
    csv_path: str = 'alice_assets/cache/alice_cache.csv'
) -> str | dict | None:
    """
    Store a feature value for a book id and return the stored value.

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
    if not isinstance(feature_value, (str, list, dict)):
        raise TypeError('feature_value must be str, list or dict')
    if not isinstance(csv_path, str):
        raise TypeError('csv_path must be str')
    if book_id < 0:
        raise ValueError('book_id must be positive')

    csv_file = Path(csv_path)
    if not csv_file.exists():
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        df_cache = pd.DataFrame(columns=['id', feature_name])
        df_cache.to_csv(csv_file, index=False)

    try:
        df_cache = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        df_cache = pd.DataFrame(columns=['id', feature_name])

    columns_changed = False
    if 'id' not in df_cache.columns:
        df_cache['id'] = pd.NA
        columns_changed = True
    if feature_name not in df_cache.columns:
        df_cache[feature_name] = pd.Series([pd.NA] * len(df_cache), dtype='object')
        columns_changed = True
    elif df_cache[feature_name].dtype != 'object':
        df_cache[feature_name] = df_cache[feature_name].astype('object')
        columns_changed = True

    if columns_changed:
        df_cache.to_csv(csv_file, index=False)

    if isinstance(feature_value, list):
        feature_value = str(feature_value)

    value_to_store = (
        json.dumps(feature_value, ensure_ascii=True, separators=(',', ':'))
        if isinstance(feature_value, dict)
        else feature_value
    )

    book_rows = df_cache.loc[df_cache['id'] == book_id]
    if book_rows.empty:
        df_cache = pd.concat(
            [df_cache, pd.DataFrame([{'id': book_id, feature_name: value_to_store}])],
            ignore_index=True
        )
    else:
        df_cache.loc[df_cache['id'] == book_id, feature_name] = value_to_store

    df_cache.to_csv(csv_file, index=False)
    return feature_value
