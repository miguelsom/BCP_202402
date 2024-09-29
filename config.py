import os

# Folder paths
SOURCE_FOLDER = os.path.join("Daily Prices", "Source")
DATASET_FOLDER = os.path.join("Daily Prices")
PLOT_FOLDER = os.path.join("Daily Prices", "Plots")

# Business day configuration
BUSINESS_DAYS_COUNT = 5

# Excel file column names
COLUMNS = [
    'Código', 'Nome', 'Repac./ Venc.', 'Índice/ Correção', 'Taxa de Compra',
    'Taxa de Venda', 'Taxa Indicativa', 'Desvio Padrão', 'Intervalo Indicativo Min.',
    'Intervalo Indicativo Máx.', 'PU', '% Pu Par', 'Duration', '% Reune', 'Referência NTN-B'
]

# URL configuration
BASE_URL = "https://www.anbima.com.br/informacoes/merc-sec-debentures/arqs/"

# Mapping of English month abbreviations to Portuguese
MONTHS_PT_BR = {
    "JAN": "jan",
    "FEB": "fev",
    "MAR": "mar",
    "APR": "abr",
    "MAY": "mai",
    "JUN": "jun",
    "JUL": "jul",
    "AUG": "ago",
    "SEP": "set",
    "OCT": "out",
    "NOV": "nov",
    "DEC": "dez"
}

# File names for dataset preparation
RAW_DATA_FILE = "dataset_source_combined.csv"
CLEANED_DATA_FILE = "cleaned_dataset.csv"

# Column names used in dataset cleaning
DATASET_COLUMNS_TO_SELECT = ['Código', 'Nome', 'PU', 'Taxa Indicativa', 'sheet_name', 'data']
DATASET_FINAL_COLUMNS = ['Código', 'Nome', 'PU', 'Taxa Indicativa', 'data', 'Indexer']