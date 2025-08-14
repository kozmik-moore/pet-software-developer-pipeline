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
    plt.savefig(location / f'{title}.{figtype}'.replace(': ', ' - '), bbox_inches='tight' if set_bbox_inches else None)

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
        title = 'Distribution of monthly health visits for all pet types'
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
        title = 'Distribution of monthly health visits by pet type'
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
    

def activities_heatmaps(
        data: pd.DataFrame, 
        category: str = 'owners', 
        save: bool = False, 
        palette: str|None = None, 
        reset_palette: bool = True, 
        return_df: bool = False):
    
    # Store palette and change to desired palette
    if palette:
        if reset_palette:
            orig_pal = sns.color_palette()
        sns.set_palette(palette)

    # Determine which category to analyze: pet types or owner ages
    c_type = {
        'owners': 'owner_age_group',
        'pets': 'pet_type'
    }[category]

    # Sort data by year and month
    a_df = data.loc[data.activity_type != 'Health', ['date', c_type, 'activity_type']].copy()
    a_df.activity_type = a_df.activity_type.cat.remove_unused_categories()
    a_df['month'] = a_df.date.dt.month
    a_df['year'] = a_df.date.dt.year

    # Get average monthly activity counts
    g_df = a_df.groupby(['year', 'month', c_type], observed=True).activity_type.value_counts().reset_index(name='counts')
    ag_df = g_df.loc[(g_df.year == 2023) | (g_df.month > 3)].groupby([c_type, 'activity_type'], observed=True).counts.agg('mean').reset_index(name='means')

    # Prepare for visualization and create heatmap
    title = f'Average monthly activity counts by {c_type.replace("_", " ")}'
    pag_df = ag_df.pivot(index=c_type, columns='activity_type', values='means')
    ax = sns.heatmap(pag_df);
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.suptitle(title)
    # plt.show()

    # Reset palette
    if palette and reset_palette:
        sns.set_palette(orig_pal)

    if save:
        _save_figure(title)
    
    if return_df:
        return ag_df
    

def activities_heatmaps_owners_pets(data: pd.DataFrame, save: bool = False, palette: str|None = None, reset_palette: bool = True, return_df: bool = False):
    if palette:
        if reset_palette:
            orig_pal = sns.color_palette()
        sns.set_palette(palette)
    a_df = data.loc[data.activity_type != 'Health', ['date', 'owner_age_group', 'pet_type', 'activity_type']].copy()
    a_df.activity_type = a_df.activity_type.cat.remove_unused_categories()
    a_df['month'] = a_df.date.dt.month
    a_df['year'] = a_df.date.dt.year
    g_df = a_df.groupby(['year', 'month', 'owner_age_group', 'pet_type'], observed=True).activity_type.value_counts().reset_index(name='counts')
    ag_df = g_df.loc[(g_df.year == 2023) | (g_df.month > 3)].groupby(['owner_age_group', 'pet_type', 'activity_type'], observed=True).counts.agg('mean').reset_index()
    activities = ag_df.activity_type.unique()
    fig, axes = plt.subplots(nrows=len(activities), figsize=(4,10));
    for ax, activity in zip(axes, activities):
        pag_df = ag_df.loc[ag_df.activity_type == activity].pivot(index='owner_age_group', columns='pet_type', values='counts')
        sns.heatmap(pag_df, ax=ax)
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title(activity)
    title = 'Monthly average activity count by owner age group and pet type'
    plt.suptitle(title)
    plt.tight_layout()
    # plt.show()

    # Reset palette
    if palette and reset_palette:
        sns.set_palette(orig_pal)

    if save:
        _save_figure(title)
    
    if return_df:
        return ag_df
    
def activities_elapsed_time_distributions(
        data: pd.DataFrame, 
        save: bool = False, 
        activity: str = 'health',
        health_activity: str = 'annual checkup', 
        group_by: str = 'pet type', 
        plot_type: str = 'box',
        palette: list[str]|str|None = None, 
        reset_palette: bool = True,
        return_df: bool = False):
    
    """Plots the distribution of time elapsed between activties per pet.
    Can be filtered by "activity type" and further filtered by "health visit type", if "health" is the activity.

    Args:
        data (pandas.DataFrame): the supplied dataframe.
        save (bool, optional): whether to save the created image to the `images` folder. Defaults to False.
        activity (str, optional): which activity type to focus on. Possible inputs include 'health', 'playing', 'resting', 'walking'. Defaults to 'health'.
        health_activity (str, optional): which 'health visit' type to visualize: select from 'annual checkup', 'ear infection', 'dental cleaning', 'injury'. Defaults to 'annual checkup'.
        group_by (str, optional): which grouping to visualize: select from 'pet type', 'owner ages' or 'both'. Defaults to 'pet type'.
        plot_type (str, optional): which distribution plot to use: select from 'box' or 'violin'. Defaults to 'box'.
        palette (list[str] | str | None, optional): which Seaborn color palette(s) to use. Defaults to None.
        reset_palette (bool, optional): whether to reset the color palette after calling this function. Defaults to True.
        return_df (bool, optional): whether to return the dataframe used to create this visualization. Defaults to False.

    Raises:
        ValueError: if `palette` is not of type `str` or `list` of length 1 or 2

    Returns:
        pandas.DataFrame|None: optionally returns the dataframe used to create this visual
    """
    
    # Set palette
    palettes = [sns.color_palette(), sns.color_palette()]
    if palette:
        if reset_palette:
            orig_pal = sns.color_palette()
        if isinstance(palette, str):
            palettes = [palette, palette]
        elif isinstance(palette, list):
            if len(palette) > 2 or len(palette) == 0:
                raise ValueError('`palette` should be a string or a list of length 1 or 2')
            elif len(palette) == 1:
                palettes = [palette[0], palette[0]]
            else:
                palettes = palette
        else:
            raise ValueError('`palette` should be a string or a list of length 1 or 2')


    # Determine which grouping type to plot
    group_type = {
        'pet type': ['pet_type'],
        'owner ages': ['owner_age_group'],
        'both': ['owner_age_group', 'pet_type']
    }[group_by]

    plot_func = {
        'box': sns.boxplot,
        'violin': sns.violinplot
    }[plot_type]

    visit_type = health_activity.title()
    activity_type = activity.capitalize()

    # Calculate average time between events and determine title variables
    conditions = data.activity_type == activity_type
    title = f'Distribution of time between '
    if activity == 'health':
        conditions = conditions & (data.issue == visit_type)
        subtitle = ', '.join([x.replace('_', ' ')  for x in group_type])
        title += f'health visits: {visit_type}'
        file_title = f'{title} ({subtitle})'
    else:
        title += f'activities: {activity_type}'
        file_title = title
    filtered_df = data.loc[conditions]
    diffs = filtered_df.groupby(['pet_id']).date.diff()
    revisit_index = diffs.loc[~diffs.isna()].index
    revisits = filtered_df.loc[filtered_df.index.isin(revisit_index), group_type]
    revisits = revisits.merge(diffs.reset_index(name='elapsed_time').set_index('index'), how='left', left_index=True, right_index=True)
    revisits.elapsed_time = revisits.elapsed_time.dt.days

    # Plot and display
    fig, axes = plt.subplots(nrows=len(group_type), squeeze=False, figsize=(8,7 if group_by == 'both' else 4))
    label_axes_palettes = zip(group_type, axes[:, 0], palettes)
    for l, a, p in label_axes_palettes:
        sns.set_palette(p)
        plot_func(revisits, x='elapsed_time', y=l, orient='h', hue=l, ax=a)
        a.set_xlabel('')
        a.set_ylabel('')
        a.set_title(f'By {l.replace("_", " ")}')
    plt.suptitle(title)
    plt.tight_layout()
    if save:
        _save_figure(file_title)
    plt.show()

    if palette and reset_palette:
        sns.set_palette(orig_pal)

    if return_df:
        return revisits