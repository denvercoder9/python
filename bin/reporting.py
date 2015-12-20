#!/usr/bin/env python

""" Script to sum up worked hours from a timeEdition csv export """

import click
import pandas as pd


def to_minutes(timestring):
    """Convert a string in the format 'hh:mm:ss' to the total number of
    minutes"""
    hours, minutes, seconds = map(int, timestring.split(':'))
    return hours*60 + minutes + int(seconds >= 30)


def get_hours_and_minutes(row):
    """Returns the total time in hours and minutes for a dataframe row"""
    return divmod(row['minutes'], 60)


def get_total_hours_and_minutes(df):
    """Returns the total time in hours and minutes for the whole dataframe"""
    return divmod(df['minutes'].sum(), 60)


def print_results(df):
    """Pretty-print results"""
    for _, row in df.iterrows():
        print '{} - {:>3} hours {:>2} minutes'.format(row['date'], *get_hours_and_minutes(row))
    print
    print 'Total    - {:>3} hours {:>2} minutes'.format(*get_total_hours_and_minutes(df))


@click.command()
@click.argument('filename')
def main(filename):
    """Read csv and sum the number of worked minutes per date"""
    csv = pd.read_csv(filename)
    df = pd.DataFrame({'date': date,
                       'minutes': group['Duration'].map(to_minutes).sum()}
                      for date, group in csv.groupby('Start date'))

    print_results(df)


if __name__ == '__main__':
    main()
