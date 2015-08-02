import click
import pandas as pd

"""
Script to sum up worked hours from a timeEdition csv export
"""


def to_minutes(timestring):
    """Convert a string in the format 'hh:mm:ss' to the total number of
    minutes"""
    hours, minutes, seconds = map(int, timestring.split(':'))
    return hours*60 + minutes + int(seconds >= 30)


def print_dataframe(df):
    """Very improvable function to generate a working hours report from a
    pandas dataframe
    """
    print 'Datum/Zeit gearbeitet'
    print '---------------------'
    for _, row in df.iterrows():
        print '{} - {} Stunden {} Minuten'.format(row['date'],
                                                  *divmod(row['minutes'], 60))
    print '\n---------------------'
    print 'Total: {} Stunden {} Minuten'.format(*divmod(df['minutes'].sum(), 60))


@click.command()
@click.argument('filename')
def main(filename):
    """Read csv and sum the number of worked minutes per date"""
    csv = pd.read_csv(filename)
    df = pd.DataFrame({'date': date,
                       'minutes': group['Duration'].map(to_minutes).sum()}
                      for date, group in csv.groupby('Start date'))
    print_dataframe(df)


if __name__ == '__main__':
    main()
