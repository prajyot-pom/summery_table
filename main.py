import csv
import os
import pandas as pd
import argparse

# field names
FIELDS = ['Feature', 'Test ID', 'Last Tested', 'Image Version', 'Status', 'Automation', 'Jira', 'Test Description']

# name of csv file
FILENAME = "university_records.csv"
# FILEPATH = 'test1.md'


def create_csv(filename, field):
    print("Inside create")
    if not os.path.exists(FILENAME):
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(field)
        csvfile.close()


def write_data(filename, md_file, feature):
    row = [[feature]]
    with open(filename, 'a+') as csvfile:
        print("Inside write_data")

        writer_obj = csv.writer(csvfile)
        table_data = pd.read_table(md_file, sep="|", header=1, index_col=1, skipinitialspace=True)
        table_row = table_data.dropna(axis=1, how='all')
        for i in range(1, 7):
            var = table_row.iloc[i, -1]
            if str(var) == 'nan':
                break
            var = var.strip()
            row.append([var])
        writer_obj.writerow(row)
    csvfile.close()


parser = argparse.ArgumentParser()
parser.add_argument("--file", help="Add md file ", required=True)
parser.add_argument("--feature", help="Add Test Feature", required=True)
args = parser.parse_args()


def main():
    create_csv(FILENAME, FIELDS)
    write_data(FILENAME, args.file, args.feature)


main()
