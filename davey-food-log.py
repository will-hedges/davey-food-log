#!/usr/bin/env python3
# daveys-food-log.py - quick pandas table for tracking my son's feedings


import foodlogfunctions as flf


def main():
    food_log_df = flf.generate_food_log_df("~/Documents/Davey Feedings.ods")
    summary_table = flf.generate_summary_table(food_log_df)
    print(summary_table)
    return


if __name__ == "__main__":
    main()
