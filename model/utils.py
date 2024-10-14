import numpy as np


def check_columns_with_nan_values(data=None):
    _column_numbers = []
    
    for column in data.columns:
        if (data[column].isna()).any().any():
            _column_numbers.append(column)
        else:
            pass
    return _column_numbers