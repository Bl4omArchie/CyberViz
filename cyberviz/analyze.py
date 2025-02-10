import pandas as pd


def analyze_csv(csv_dataset: object):
    df = pd.read_csv(csv_dataset.path_dataset)
    
    columns = df.columns.tolist()
    file_size = df.memory_usage(deep=True).sum()
    num_rows, num_columns = df.shape
    
    stats = df.describe(include='all').to_dict()
    missing_values = df.isnull().sum().to_dict()
    
    return {
        'file_size': file_size,
        'num_rows': num_rows,
        'num_columns': num_columns,
    }