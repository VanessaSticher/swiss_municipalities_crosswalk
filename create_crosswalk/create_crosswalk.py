##########
# Create crosswalk file for Swiss municipalities
#
# created: 2021-04-30, Vanessa Sticher (VS)
# last edited: 2021-08-24, VS
##########

import glob
import numpy as np
import pandas as pd
import requests
import warnings

from datetime import datetime

'''
Required input:
- date_since: date as string in US date format (mm/dd/yyyy), e.g. '12/31/2019'
- date_to: date as string in US date format (mm/dd/yyyy), e.g. '12/31/2019'
- cantons: to include all cantons: empty string or 'all'
           to include only certain cantons: list of canton abbreviations, e.g. ["BE", "ZH", "AG"]
'''


def create_crosswalk(date_since, date_to, cantons):
    # ============================== CHECK VALIDITY OF INPUT ============================== #
    # Check dates
    if datetime.strptime(date_since, '%m/%d/%Y') < datetime.strptime('09/12/1848', '%m/%d/%Y'):
        raise ValueError("Invalid date input: earlier date must be >= 09/12/1848")
    if datetime.strptime(date_to, '%m/%d/%Y') > datetime.today():
        raise ValueError("Invalid date input: later date cannot be in the future")
    if datetime.strptime(date_since, '%m/%d/%Y') > datetime.strptime(date_to, '%m/%d/%Y'):
        raise ValueError("Invalid date input: first date input must be before second date input")
    # Check list of cantons:
    if cantons != "" and cantons != "all":
        if len(cantons) != len(set(cantons)):
            raise ValueError("Invalid list of cantons: list includes duplicates")
        if set(cantons).issubset(
                {"AG", "AI", "AR", "BE", "BL", "BS", "FR", "GE", "GL", "GR", "JU", "LU", "NE", "NW", "OW", "SG", "SH",
                 "SO", "SZ", "TG", "TI", "UR", "VD", "VS", "ZG", "ZH"}):
            pass
        else:
            raise ValueError("Invalid list of cantons: list contains incorrect canton abbreviations")

    # ============================== FUNCTIONS ============================== #
    def date_US_to_CH(date_US_str):
        date_split = date_US_str.split('/')
        date_split[0], date_split[1] = date_split[1], date_split[0]
        date_CH_str = '.'.join(date_split)
        return date_CH_str

    def date_US_to_ymd(date_US_str):
        date_split = date_US_str.split('/')
        date_ymd = '-'.join([date_split[2], date_split[0], date_split[1]])
        return date_ymd

    # Create the list of variables to merge on based on the prefix
    def merge_varlist(iterator):
        vars_merge = ['canton', 'district_nr', 'municipality_nr', 'municipality']
        varlist_merge = ['new' + str(iterator) + '_' + var for var in vars_merge]
        return varlist_merge

    # ============================== PULL DATA FROM OFFICIAL WEBSITE ============================== #
    url_main = 'https://www.agvchapp.bfs.admin.ch/de/mutated-communes/results/xls'
    params = {'EntriesFrom': date_US_to_CH(date_since),
              'EntriesTo': date_US_to_CH(date_to),
              'Deleted': True,
              'Created': True,
              'TerritoryChange': False,
              'NameChange': True,
              'DistrictChange': True,
              'Other': True}

    # If only one canton: add canton to request
    if cantons != 'all' and len(cantons) == 1:
        params['Canton'] = cantons

    # Read data, rename columns, drop row with German column names
    try:  # Try to download data
        with warnings.catch_warnings(record=True):  # suppress warning of no default style
            warnings.simplefilter("always")
            df = pd.read_excel(requests.post(url_main, params, allow_redirects=True).content,
                               names=['change_nr', 'old_canton', 'old_district_nr', 'old_municipality_nr',
                                      'old_municipality', 'new_canton', 'new_district_nr', 'new_municipality_nr',
                                      'new_municipality', 'change_date']).drop([0]).reset_index(drop=True)

    except:  # Use most recent download in case download fails
        df = pd.read_excel(glob.glob('data/*.xlsx')[-1],
                           names=['change_nr', 'old_canton', 'old_district_nr', 'old_municipality_nr',
                                  'old_municipality', 'new_canton', 'new_district_nr', 'new_municipality_nr',
                                  'new_municipality', 'change_date']).drop([0]).reset_index(drop=True)
        df = df[date_since <= df['change_date'] <= date_to]
        if cantons != 'all' and len(cantons) == 1:
            df = df[(df['canton_old'] == cantons) | (df['canton_new'] == cantons)]

    # Drop if old == new (this is important to not create an infinite loop after of change in the for A->A->A...)
    df = df[-((df['old_canton'] == df['new_canton'])
              & (df['old_district_nr'] == df['new_district_nr'])
              & (df['old_municipality_nr'] == df['new_municipality_nr'])
              & (df['old_municipality'] == df['new_municipality']))]

    # Restrict to selected cantons (if more than 1 canton)
    if cantons != 'all' and len(cantons) > 1:
        df = df[(df['canton_old'].isin(cantons)) | (df['canton_new'].isin(cantons))]

    # =================================================================================== #
    #                                CREATE CROSSWALK FILE                                #
    # =================================================================================== #

    '''
    Aufgehobene Gemeinden: change of Gemeindenummer und Gemeindename
    Neu entstandene Gemeinden: change of Gemeindenummer und Gemeindename
    Gebietsänderung: no change in Gemeindenummer or Gemeindename -->ignore for now
    Namensänderung: change in Gemeindename, no change in Gemeindenummer
    Änderung der Kantons- oder Bezirkszugehörigkeit: change in Gemeindenummer, no change in Gemeindename
    Andere Mutationen: e.g. change in Gemeindenummer
    
    '''

    # ============================ Create cascade of changes ============================ #
    '''
    Change list of changes from long shape to wide, i.e. to a cascade
    Example: A->B and B->C becomes A->B->C
    '''

    # Create start dataframe
    df_left = df.copy()  # start dataframe
    df_left.columns = df_left.columns.str.replace('new', 'new1') \
        .str.replace('old', 'new0') \
        .str.replace('change_nr', 'change_nr1') \
        .str.replace('change_date', 'change_date1')

    # Append changes for as long as possible
    i = 1  # start value
    changes = 1  # start with a value non-zero value
    while changes > 0:
        # Create dataframe with all changes to append
        df_right = df.copy()
        df_right.columns = df_right.columns.str.replace('new', 'new' + str(i + 1)) \
            .str.replace('old', 'new' + str(i)) \
            .str.replace('change_nr', 'change_nr' + str(i + 1)) \
            .str.replace('change_date', 'change_date' + str(i + 1))

        # Append dataframe if change_date2>change_date1
        df_left = df_left.merge(df_right, on=merge_varlist(i), how='left')

        # Make sure that changes are in the correct order
        newvars = [var for var in df_left.columns if str(i + 1) in var]
        date1 = 'change_date' + str(i)
        date2 = 'change_date' + str(i + 1)
        df_left.loc[(df_left[date2] < df_left[date1]), newvars] = np.nan

        # Count number of changes and increase counter
        changes = len(df_left['change_date' + str(i + 1)].dropna())
        i = i + 1

    # Drop last merge (because that resulted in 0 changes)
    last_cols = [col for col in df_left.columns if str(i) in col]
    df_merged = df_left.drop(columns=last_cols)

    # ============================ Keep only first and last  ============================ #
    df_final = df_merged.copy()

    N_changes = i - 1
    col_list = [col.replace('new0_', '') for col in df_final.columns if 'new0' in col]
    for col in col_list:
        for i in range(N_changes - 1, -1, -1):
            df_final['new' + str(N_changes) + '_' + col] = df_final['new' + str(N_changes) + '_' + col].fillna(
                df_final['new' + str(i) + '_' + col])

    df_final.columns = df_final.columns.str.replace('new5', 'new').str.replace('new0', 'old')
    df_final = df_final[['old_' + col for col in col_list] + ['new_' + col for col in col_list]]

    # Format numeric columns
    df_final['old_district_nr'] = df_final['old_district_nr'].astype(int)
    df_final['old_municipality_nr'] = df_final['old_municipality_nr'].astype(int)
    df_final['new_district_nr'] = df_final['new_district_nr'].astype(int)
    df_final['new_municipality_nr'] = df_final['new_municipality_nr'].astype(int)

    # Export crosswalk dataset

    df_final.to_stata("crosswalk_" + date_US_to_ymd(date_since) + "_to_" + date_US_to_ymd(date_to) + ".dta",
                      write_index=False, version=118,
                      variable_labels=dict(old_canton='Canton ' + date_since,
                                           old_district_nr='District number ' + date_since,
                                           old_municipality_nr='Municipality number ' + date_since,
                                           old_municipality='Municipality name ' + date_since,
                                           new_canton='Canton ' + date_to,
                                           new_district_nr='District number ' + date_to,
                                           new_municipality_nr='Municipality number ' + date_to,
                                           new_municipality='Municipality name ' + date_to))
