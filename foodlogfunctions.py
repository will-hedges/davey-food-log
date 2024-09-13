#!/usr/bin/env python3
# foodlogfunctions.py - helper functions for davey-food-log.py

from datetime import timedelta
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
        time_list = date_df["Time"].tolist()
        volume_list = date_df["Volume"].tolist()

        # combine "close" feedings into one event
        # we can look at one row's time and calculate the timedelta between
        #   this time and the next one
        # if the timedelta is less than 90 minutes,
        #   combine the volumes and remove the "second" value from both the
        #       time and volume lists
        for i, time1 in enumerate(time_list):
            try:
                j = i + 1
                time2 = time_list[j]
                time_difference = timedelta(
                    hours=time2.hour - time1.hour,
                    minutes=time2.minute - time1.minute,
                )
                if time_difference < timedelta(minutes=90):
                    volume_list[i] += volume_list[j]
                    del time_list[j]
                    del volume_list[j]

            except IndexError:
                break

        num_feedings = len(volume_list)
        total_volume = sum(volume_list)
        vol_per_feed = round(total_volume / num_feedings, 1)

        # match with regex to see if we have a hundredths place
        #   if no match, add a zero
        total_volume = str(total_volume)
        mo = re.match(r"\d*.\d{2}", total_volume)
        if not mo:
            total_volume = total_volume + "0"

        newRow = pd.DataFrame(
            {
                "Date": [date.strftime("%m-%d-%y")],
                "Feedings": [str(num_feedings)],
                "Volume (oz)": [total_volume],
                "oz / Feed": [str(vol_per_feed)],
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
