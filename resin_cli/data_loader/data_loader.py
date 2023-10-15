import os
import glob
import pandas as pd

from pydantic import ValidationError

from resin.knoweldge_base import KnowledgeBase


class IndexNotUniqueError(ValueError):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DataframeValidationError(ValueError):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def _validate_dataframe(df: pd.DataFrame):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Dataframe must be a pandas DataFrame")
    if "id" not in df.columns:
        raise DataframeValidationError("Dataframe must have an 'id' column")
    if df.id.nunique() != df.shape[0]:
        raise IndexNotUniqueError("Dataframe index must be unique")
    try:
        KnowledgeBase._df_to_documents(df)
    except ValidationError:
        return DataframeValidationError("Dataframe failed validation")
    except ValueError as e:
        raise DataframeValidationError(f"Unexpected error in validation: {e}")


def _load_single_file_by_suffix(f: str) -> pd.DataFrame:
    if f.endswith(".parquet"):
        df = pd.read_parquet(f)
    elif f.endswith(".jsonl"):
        df = pd.read_json(f, lines=True)
    else:
        raise ValueError("Only .parquet and .jsonl files are supported")

    return df


def load_dataframe_from_path(path: str) -> pd.DataFrame:
    if os.path.isdir(path):
        all_files = glob.glob(os.path.join(path, "*.jsonl")) + glob.glob(
            os.path.join(path, "*.parquet")
        )
        df = pd.concat(
            [_load_single_file_by_suffix(f) for f in all_files],
            axis=0,
            ignore_index=True,
        )
    else:
        df = _load_single_file_by_suffix(path)

    _validate_dataframe(df)

    return df