import pandas as pd

def add_dt_column(df: pd.DataFrame, dt_part: str = 'year', column: str = 'date'):
    """Extracts a datetime component from a column and creates a new column in the dataframe for that data.

    Args:
        df (pd.DataFrame): the supplied dataframe
        dt_part (str, optional): the datetime part to add. Defaults to 'year'.
        column (str, optional): the name of the column containing the date values. Defaults to 'date'.

    Raises:
        ValueError: raised if the column cannot be found in the dataframe

    Returns:
        pandas.DataFrame: a new dataframe with the added data
    """
    new_df = df.copy()
    if not (column in df.columns):
        raise ValueError(f'No column named {column} found in dataframe')
    if df[column].dtype != '<M8[ns]':
        dates = pd.to_datetime(df[column])
    else:
        dates = df[column]
    new_df[dt_part] = getattr(dates.dt, dt_part)
    return new_df