#!/usr/bin/env python3
# foodlogfunctions.py - helper functions for davey-food-log.py

import re

import pandas as pd
from prettytable import PrettyTable


def generate_food_log_df(fp):
    if fp.endswith(".ods"):
        df = pd.read_excel(fp, engine="odf")
    else:
        df = pd.read_excel(fp)

    # get a list of unique dates
    dates = set(df.loc[:, "Date"])

    # initialize a summary dataframe
    summary_df = pd.DataFrame({"Date": [], "Feedings": [], "Volume (oz)": []})

    # for each unique date, get a list of all the volumes for that date
    #   and get the number of feedings for each date
    #       we will then add that row of data to the summary df
    for date in dates:
        date_df = df[df["Date"] == date]
        volume_list = date_df["Volume"].tolist()

        # TODO combine "close" feedings into one event
        # look at one row's date and time
        # calculate the timedelta between this one and the next row
        # if the timedelta is less than some value, say 90 min
        # combine the volumes and remove the next row

        total_volume = str(sum(volume_list))
        # match with regex to see if we have a hundredths place
        #   if no match, add a zero
        mo = re.match(r"\d*.\d{2}", total_volume)
        if not mo:
            total_volume += "0"

        newRow = pd.DataFrame(
            {
                "Date": [date.strftime("%m-%d-%y")],
                "Feedings": [str(len(volume_list))],
                "Volume (oz)": [total_volume],
            }
        )
        summary_df = pd.concat([summary_df, newRow], ignore_index=True)

    # return the summary df, sorted on date asc
    return summary_df.sort_values(by="Date")


def generate_summary_table(df):
    table = PrettyTable()
    table.field_names = df.columns
    for idx, row in df.iterrows():
        table.add_row(row)

    return table
