import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utilities.processes import all_pet_data
from utilities.config import products
from pathlib import Path

def _save_figure(title: str, location: str|Path = products.images, set_bbox_inches: bool = True, figtype: str = 'jpg'):
    """Saves the currently active figure with the supplied title and location

    Args:
        title (str): the name of the figure
        location (str | Path, optional): the folder to save the figure to. Must exist before calling. Defaults to products.images.
        set_bbox_inches (bool, optional): Whether to trim whitespace in the margins when saving the figure: ensures the entire figure is saved. Defaults to True.
        figtype (str, optional): the file type to save as. Defaults to 'jpg'.
    """
    if isinstance(location, str):
        location = Path(location)
    plt.savefig(location / f'{title}.{figtype}', bbox_inches='tight' if set_bbox_inches else None)

def activities_countplots(data: pd.DataFrame, save: bool = False, palette: str|None = None, return_df: bool = False):
    """Creates a barplot of the record counts for each activity that is not a health activity.

    Args:
        data (pd.DataFrame): A copy of the cleaned dataframe
        save (bool, optional): whether to save the figure produced to `products/images` as a JPG. Defaults to False.
        palette (str | None, optional): a Seaborn palette to set, if any. Defaults to None.
    """
    if palette:
        sns.set_palette(palette)
    a_df = data.loc[-(data.activity_type == 'Health')].copy()
    a_df.activity_type = a_df.activity_type.cat.remove_unused_categories()
    ax = sns.countplot(a_df, x='activity_type', dodge=False, hue='activity_type')
    ax.set_xlabel('')
    ax.set_ylabel('')
    title = 'Activity counts (non-health)'
    plt.suptitle(title)
    if save:
        _save_figure(title)
    plt.show()

    if return_df:
        return a_df

def activities_boxplots(data: pd.DataFrame, by_type: bool = False, save: bool = False, palette: str|None = None, reset_palette: bool = True, return_df: bool = False):
    """Creates boxplots of non-health activity counts per month.

    Args:
        data (pd.DataFrame): the cleaned dataframe
        by_type (bool, optional): whether to visualize counts by pet type. Defaults to False.
        save (bool, optional): whether to save the figure created to the images directory. Defaults to False.
        palette (str | None, optional): a Seaborn palette to set, if any. Defaults to None.
        reset_palette (bool, optional): Whether to reset the palette after the visualization is complete. Defaults to True.
        return_df (bool, optional): whether to return the dataframe created to make the visual. Defaults to False.

    Returns:
        None | pandas.DataFrame: either None or the dataframe created to produce the visual
    """
    if palette:
        if reset_palette:
            orig_palette = sns.color_palette()
        sns.set_palette(palette)
    # Copy the data, removing health records and "Health" activity category
    a_df = data.loc[data.activity_type != 'Health'].copy()
    a_df.activity_type = a_df.activity_type.cat.remove_unused_categories()

    # Group data and count number of each activity per month
    a_df['month'] = a_df.date.dt.month
    a_df['year'] = a_df.date.dt.year
    
    # Visualize
    if by_type:
        title = 'Distribution of activity counts per month by pet type'
        g_df = a_df.groupby(['year', 'month', 'pet_type'], observed=True).activity_type.value_counts().reset_index(name='counts')
        g_df = g_df.loc[(g_df.year == 2023) | (g_df.month > 3)].reset_index(drop=True)
        g = sns.FacetGrid(g_df, col='pet_type', hue='activity_type')
        g.map(sns.boxplot, 'activity_type', 'counts', order=sorted(g_df.activity_type.unique()), width=0.7)
        g.set_axis_labels(x_var='', y_var='')
        g.add_legend(title='Activity type')
        g.tight_layout()
        g.set_titles("{col_name}")
        g.figure.subplots_adjust(top=0.8)  # makes room for title
        g.figure.suptitle(title)
    else:
        title = 'Distribution of activity counts per month'
        g_df = a_df.groupby(['year', 'month']).activity_type.value_counts().reset_index(name='counts')
        g_df = g_df.loc[(g_df.year == 2023) | (g_df.month > 3)].reset_index(drop=True)
        ax = sns.boxplot(g_df, x='activity_type', y='counts', hue='activity_type')
        ax.set_xlabel('')
        ax.set_ylabel('')
        plt.suptitle(title)

    if save:
        _save_figure(title)
    plt.show()

    if palette and reset_palette:
        sns.set_palette(orig_palette)

    if return_df:
        return g_df


def health_activities_boxplots(data: pd.DataFrame, by_type: bool = False, save: bool = False, palette: str|None = None, return_df: bool = False):
    """Creates boxplots of the health visits for each health activity.
    Can optionally calculate and visualize for each pet type.

    Args:
        data (pd.DataFrame): The cleaned dataframe
        by_type (bool, optional): Whether to group the results by pet type. Defaults to False.
        save (bool, optional): whether to save the figure produced to `products/images` as a JPG. Defaults to True.
        palette (str | None, optional): a Seaborn palette to set, if any. Defaults to None.
    """
    if palette:
            sns.set_palette(palette)
    hda_df = data.loc[(data.activity_type == 'Health'), ['date', 'issue', 'resolution', 'pet_type']]
    hda_df['month'] = hda_df.date.dt.month
    hda_df['year'] = hda_df.date.dt.year

    if not by_type:
        issue_counts = hda_df.groupby(['year', 'month']).issue.value_counts().reset_index(name='counts')
        ax = sns.boxplot(issue_counts, x='issue', y='counts', hue='issue')
        ax.set_xlabel('')
        ax.set_ylabel('')
        title = 'Distibution of health visits for all pet types'
        plt.suptitle(title)
    else:
        issue_counts = hda_df.groupby(['year', 'month', 'pet_type'], observed=True).issue.value_counts().reset_index(name='counts')
        g = sns.FacetGrid(issue_counts, col='pet_type', hue='issue')
        g.map(sns.boxplot, 'issue', 'counts', order=sorted(hda_df.issue.unique()), width=0.6)
        g.set_axis_labels(x_var='', y_var='')
        g.set
        g.set_xticklabels(['' for x in range(len(hda_df.issue.unique()))])
        g.set_titles('{col_name}')
        g.add_legend()
        g.tight_layout()
        g.set(xticks=[])
        g.figure.subplots_adjust(top=0.8)  # makes room for title
        title = 'Distibution of health visits by pet type'
        g.figure.suptitle(title)
    if save:
        _save_figure(title)
    plt.show()

    if return_df:
        return issue_counts

def pet_counts(data: pd.DataFrame, save: bool = False, palette: str|None = None, return_df: bool = False):
    if palette:
        sns.set_palette(palette)
    pet_counts = data.groupby('pet_type', observed=True).pet_id.nunique().reset_index(name='counts')
    ax = sns.barplot(pet_counts, x='pet_type', y='counts', hue='pet_type')
    ax.set_xlabel('')
    ax.set_ylabel('')
    title = 'Unique pet counts'
    ax.set_title(title)
    if save:
        _save_figure(title)
    plt.show()

    if return_df:
        return pet_counts

def pet_counts_by_owner_age(data: pd.DataFrame, proportions: bool = False, save: bool = False, palette: str|None = None, return_df: bool = False):
    """_summary_

    Args:
        data (pd.DataFrame): _description_
        proportions (bool, optional): _description_. Defaults to False.
        save (bool, optional): _description_. Defaults to False.
        palette (str | None, optional): a Seaborn palette to set, if any. Defaults to None.
    """
    if palette:
        sns.set_palette(palette)
    u_df = data.drop_duplicates(subset=['pet_id', 'owner_id'])[['owner_age_group', 'pet_type']]  # unique pet_id and owner id
    pet_types = sorted(list(u_df.pet_type.unique()))
    age_groups = sorted(list(u_df.owner_age_group.unique()))
    if proportions:
        normalize = True
        name = 'prop'
        title = 'Pet proportions by owner age group'
    else:
        normalize = False
        name = 'counts'
        title = 'Pet counts by owner age group'
    counts_df = u_df.groupby('owner_age_group', observed=True).pet_type.value_counts(normalize=normalize).reset_index(name=name).sort_values(['pet_type', 'owner_age_group']).set_index(['pet_type', 'owner_age_group'], drop=True)
    totals = np.array([0.0 for x in range(len(age_groups))])
    for i, pet in enumerate(pet_types):
        new = counts_df.loc[pet][name].values
        plt.bar(age_groups, new, label=pet, color=sns.color_palette()[i], bottom=totals)
        totals += new
    plt.legend(loc='best', bbox_to_anchor=(1, 0.7), reverse=True)
    plt.suptitle(title)
    if save:
        _save_figure(title)
    plt.show()

    if return_df:
        return counts_df