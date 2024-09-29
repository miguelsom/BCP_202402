import pandas as pd
import re

class DatasetValidator:
    """
    A static class that provides various validation methods for a dataset (pandas DataFrame).
    """

    @staticmethod
    def check_expected_columns(df: pd.DataFrame, expected_columns: list) -> None:
        """Check if all expected columns are present in the DataFrame."""
        for column in expected_columns:
            if column not in df.columns:
                raise ValueError(f"Missing expected column: {column}")
        print("✔ All expected columns are present.")

    @staticmethod
    def validate_date_column(df: pd.DataFrame, date_column: str) -> None:
        """Validate that the 'data' column matches the 'DD/MM/YYYY' format using regex."""
        date_pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'
        if not df[date_column].apply(lambda x: bool(re.match(date_pattern, str(x)))).all():
            raise TypeError(f"The '{date_column}' column should be in 'DD/MM/YYYY' format.")
        print(f"✔ '{date_column}' column is in 'DD/MM/YYYY' format.")

    @staticmethod
    def validate_numeric_columns(df: pd.DataFrame, columns: list) -> None:
        """Validate that the specified columns contain numeric values (integer or decimal)."""
        numeric_pattern = r'^\d+(\.\d{1,2})?$'
        for column in columns:
            if not df[column].apply(lambda x: bool(re.match(numeric_pattern, str(x)))).all():
                raise TypeError(f"The '{column}' column should contain numeric values in string format.")
        print(f"✔ {', '.join(columns)} columns contain valid numeric strings.")

    @staticmethod
    def check_for_missing_values(df: pd.DataFrame, key_columns: list) -> None:
        """Check for missing or null values in key columns."""
        if df[key_columns].isnull().any().any():
            raise ValueError(f"Missing or null values found in key columns: {', '.join(key_columns)}")
        print(f"✔ No missing or null values in key columns: {', '.join(key_columns)}")

    @staticmethod
    def check_for_duplicates(df: pd.DataFrame, subset_columns: list) -> None:
        """Check for duplicate rows based on a subset of columns."""
        if df.duplicated(subset=subset_columns).any():
            raise ValueError("Duplicate rows detected in the dataset.")
        print("✔ No duplicate rows detected.")

    @staticmethod
    def validate_alphanumeric_column(df: pd.DataFrame, column: str) -> None:
        """Validate that the specified column contains only alphanumeric values."""
        if not df[column].apply(lambda x: bool(re.match(r'^[A-Za-z0-9]+$', str(x)))).all():
            raise ValueError(f"Invalid values in '{column}': Must be alphanumeric.")
        print(f"✔ '{column}' column is alphanumeric.")

    @staticmethod
    def validate_string_column(df: pd.DataFrame, column: str) -> None:
        """Validate that the specified column contains non-empty strings."""
        if not df[column].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0).all():
            raise ValueError(f"Invalid values in '{column}': Must be a non-empty string.")
        print(f"✔ '{column}' column contains valid strings.")

    @staticmethod
    def validate_indexer_column(df: pd.DataFrame, column: str, valid_values: list) -> None:
        """Validate that the specified column contains only values from the valid_values list."""
        if not df[column].isin(valid_values).all():
            raise ValueError(f"Invalid values in '{column}'. Expected one of {valid_values}.")
        print(f"✔ '{column}' column contains valid values.")

    @staticmethod
    def validate_positive_values(df: pd.DataFrame, columns: list) -> None:
        """Validate that the specified columns contain values greater than 0."""
        for column in columns:
            if (df[column] <= 0).any():
                raise ValueError(f"Invalid values in '{column}': All values must be greater than 0.")
        print(f"✔ {', '.join(columns)} columns contain valid positive values.")

    @staticmethod
    def validate_dataset(df: pd.DataFrame) -> None:
        """
        Run a series of validation checks on the dataset to ensure it conforms to the expected structure.
        """
        expected_columns = ['Código', 'Nome', 'PU', 'Taxa Indicativa', 'data', 'Indexer']
        numeric_columns = ['Taxa Indicativa', 'PU']
        key_columns = ['Código', 'Nome', 'PU', 'Taxa Indicativa', 'data', 'Indexer']
        subset_columns = ['Código', 'Nome', 'PU', 'Taxa Indicativa', 'data', 'Indexer']
        valid_indexers = ['DI +', 'IPCA +', '% do DI']

        DatasetValidator.check_expected_columns(df, expected_columns)
        DatasetValidator.validate_date_column(df, 'data')
        DatasetValidator.validate_numeric_columns(df, numeric_columns)
        DatasetValidator.check_for_missing_values(df, key_columns)
        DatasetValidator.check_for_duplicates(df, subset_columns)
        DatasetValidator.validate_alphanumeric_column(df, 'Código')
        DatasetValidator.validate_string_column(df, 'Nome')
        DatasetValidator.validate_indexer_column(df, 'Indexer', valid_indexers)
        DatasetValidator.validate_positive_values(df, numeric_columns)

        print("✔ Dataset validation passed successfully.")
