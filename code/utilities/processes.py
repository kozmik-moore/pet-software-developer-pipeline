import pandas as pd
import numpy as np
from pathlib import Path

def load_dbs(*filenames: str|Path):
    """Takes supplied filenames and returns a list of dataframes \
    
    The list order is 'activities', 'health', 'users'

    Returns:
        list: a list of dataframes
    """
    def get_filename(f: str|Path):
        return f.name if isinstance(f, Path) else f

    names = ['activities', 'health', 'users']
    dataframes = []
    for name in names:
        result = list(filter(lambda x: name in get_filename(x), filenames))
        if not result:
            raise ValueError(f'None of the supplied filenames contains "{name}"')
        if len(result) > 1:
            raise ValueError(f'More than one filename returned containing "{name}"')
        dataframes.append(pd.read_csv(result[0]))
    return dataframes


def merge_dbs(*dfs: pd.DataFrame):
    """Merges the supplied databases \
    
    Expects databases to be two or more of "pet activities", "pet health", and "users"

    Args:
        method (str, optional): The method to use for joining any database to "users". Defaults to 'inner'.

    Raises:
        ValueError: Raised if fewer than 2 valid dataframes are supplied

    Returns:
        pandas.DataFrame: the resulting merged dataframe
    """

    # Identify dataframes
    activities = list(filter(lambda x: 'activity_type' in x.columns, dfs))
    health = list(filter(lambda x: 'issue' in x.columns, dfs))
    users = list(filter(lambda x: 'owner_id' in x.columns, dfs))

    # Check for at least two valid databases
    if sum([bool(x) for x in [activities, health, users]]) < 2:
        raise ValueError('Must supply at least two valid dataframes')

    # Rename columns to simplify merge
    if health:
        health[0].rename(columns={'visit_date': 'date'}, inplace=True)

    # Merge dataframes
    if activities and health:
        activities = pd.concat([activities[0], health[0]], ignore_index=True)
    elif health:
        activities = health[0]
    else:
        activities = activities[0]
    if users:
        merged_df = pd.merge(activities, users[0], on='pet_id')
    else:
        merged_df = activities
    return merged_df


def clean_data(df: pd.DataFrame):
    """Checks for specific columns in the dataframe and cleans them

    Args:
        df (pandas.DataFrame): the dataframe to be cleaned

    Returns:
        pandas.DataFrame: the cleaned dataframe
    """
    tdf = df.copy()

    # Drop records missing "pet_id", "owner_id", or "date"

    tdf.dropna(subset=['pet_id', 'date', 'owner_id'], inplace=True)

    # Strip leading and trailing whitespace from columns with strings
    for column in ['activity_type', 'issue', 'resolution', 'owner_age_group', 'pet_type']:
        if column in tdf.columns:
            tdf[column] = tdf[column].str.strip()
    
    # Change "date" datatype
    if 'date' in tdf.columns:
        tdf.date = pd.to_datetime(tdf.date, errors='coerce')

    # Assign "Health" to health activities
    if 'issue' in tdf.columns:
        tdf.loc[~df.issue.isna(), 'activity_type'] = 'Health'  

    # Clean values for 'activity_type': "Playing", "Walking", "Resting"
    if 'activity_type' in tdf.columns:
        for activity in ['Play', 'Walk', 'Rest']:
            tdf.activity_type = tdf.activity_type.str.replace(fr'^{activity}$', f'{activity}ing', regex=True)
        tdf.activity_type = tdf.activity_type.astype('category')  

    # Assign 0 to "duration_minutes" for health records and convert datatype
    if 'duration_minutes' in tdf.columns:
        tdf.loc[tdf.activity_type == 'Health', 'duration_minutes'] = 0
        tdf.loc[tdf.duration_minutes == '-', 'duration_minutes'] = np.nan
        tdf.duration_minutes = tdf.duration_minutes.astype('float')

    # Assign NaN for "issue", if missing, and change datatype to "category"
    if 'issue' in tdf.columns:
        tdf.loc[tdf.issue.isna(), 'issue'] = np.nan
        tdf.issue = tdf.issue.astype('category')

    # Assign NaN for "resolution", if missing, and change datatype to "category"
    if 'resolution' in tdf.columns:
        tdf.loc[tdf.resolution.isna(), 'resolution'] = np.nan
        tdf.resolution = tdf.resolution.astype('category')

    # Change "owner_age_group" datatype to "category" and assign NaN, if missing
    if 'owner_age_group' in tdf.columns:
        tdf.loc[tdf.owner_age_group.isna(), 'owner_age_group'] = np.nan
        # tdf.owner_age_group = tdf.owner_age_group.astype('category')

    # Change "pet_type" datatype to "category" and assign NaN, if missing
    if 'pet_type' in tdf.columns:
        tdf.loc[tdf.pet_type.isna(), 'pet_type'] = np.nan
        tdf.pet_type = tdf.pet_type.astype('category')

    return tdf


def sort_data(df: pd.DataFrame):
    """Orders the columns of the data and sorts the records
     Records are sorted by `pet_id`, `date`, `owner_id`, and `activity_type`

    Args:
        df (pd.DataFrame): the dataframe to be sorted

    Returns:
        pandas.DataFrame: a dataframe that has been ordered
    """
    cols_sort_by = ['pet_id', 'date', 'owner_id', 'activity_type']
    cols_order = [
        'pet_id', 
        'date', 
        'activity_type', 
        'duration_minutes', 
        'issue', 'resolution',	
        'owner_id',	
        'owner_age_group', 
        'pet_type',
        ]
    cols_available = [x for x in cols_order if x in df.columns]
    cols_available_sort = [x for x in cols_sort_by if x in cols_available]
    sorted_df = df.loc[:, cols_available].sort_values(cols_available_sort).reset_index(drop=True)
    return sorted_df


def all_pet_data(activities: str|Path, health: str|Path, users: str|Path, sort: bool = False):
    """Merges and cleans data from the "pet activities", "pet health", and "users" databases

    Args:
        activities (str): the "activities" CSV file
        health (str): the "health" CSV file
        users (str): the "users" CSV file
        merge (str): the type of merge to be performed between any database and "users". Defaults to 'left'.
        sort (bool): whether to sort rows and columns of the resulting dataframe. Defaults to False.

    Returns:
        pandas.DataFrame: a DataFrame of cleaned and merged databases
    """
    df_list = load_dbs(activities, health, users)   # Load
    merge_df = merge_dbs(*df_list)                  # Merge
    clean_df = clean_data(merge_df)                 # Clean
    if sort:                                        # Sort
        return sort_data(clean_df)
    return clean_df

# Test function courtesy of `u/AvailableMarzipan285` on Reddit

def test_function(activities: str, health: str, users: str):

    with open (activities, 'r') as file:
        pa_df=pd.read_csv(file, parse_dates=['date'])

    with open (health, 'r') as file:
        ph_df=pd.read_csv(file, parse_dates=['visit_date'])

    with open (users, 'r') as file:
        u_df=pd.read_csv(file)

    pa_df = pa_df.dropna(subset=['pet_id', 'date'])
    pa_df['activity_type'] = pa_df['activity_type'].str.strip()
    pa_df['activity_type'] = pa_df['activity_type'].replace({"Play":"Playing", "Walk":"Walking", "Rest":"Resting"})
    pa_df['issue'] = pa_df['issue'] = np.nan
    pa_df['resolution'] = np.nan

    ph_df = ph_df.rename(columns={'visit_date':'date'})
    ph_df = ph_df.dropna(subset=['pet_id', 'date'])
    ph_df['issue'] = ph_df['issue'].str.strip()
    ph_df['resolution'] = ph_df['resolution'].str.strip()
    ph_df['activity_type'] = 'Health'
    ph_df['duration_minutes'] = 0

    u_df = u_df.dropna(subset=['owner_id'])
    u_df['owner_age_group'] = u_df['owner_age_group'].str.strip()
    u_df['pet_type'] = u_df['pet_type'].str.strip()

    pa_ph_df = pd.concat([pa_df,ph_df], axis=0, ignore_index=True)

    final_df = pa_ph_df.merge(u_df, on='pet_id', how='left')

    final_df['duration_minutes'] = final_df['duration_minutes'].replace('-', np.nan)

    #final_df['activity_type'] = final_df['activity_type'].astype('category')
    final_df['duration_minutes'] = final_df['duration_minutes'].astype(float)
    #final_df['issue'] = final_df['issue'].astype('category')
    #final_df['resolution'] = final_df['resolution'].astype('category')
    #final_df['owner_age_group'] = final_df['owner_age_group'].astype('category')
    #final_df['pet_type'] = final_df['pet_type'].astype('category')

    #final_df.info()

    return final_df