import csv
import os
import pandas as pd
import argparse
import markdown
from bs4 import BeautifulSoup

"""
This script takes absolute path of the directory containing all the *.md files
and add summery of each file in the summery table.
"""

# field names
FIELDS = ['Feature', 'Test ID', 'Last Tested', 'Image Version', 'Status', 'Automation', 'Jira', 'Test Description']

# name of csv file
FILENAME = "university_records.csv"


def create_csv(filename, field):
    """
    This function creates a csv file containing summery table if not already exists.
    :param filename: CSV file name
    :param field: Fields to be added in the csv file
    """
    if not os.path.exists(FILENAME):
        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(field)
        csvfile.close()


def get_description(md_file):
    """
    This function converts the md file into html and from html to text using html parser
    and returns the test description.
    After fetching the description, it deletes the text file.

    :param md_file: Mkdocs file
    :return: Test Description in string format
    """
    html = markdown.markdown(open(md_file).read())
    f = open("demo.txt", 'w')
    f.write("".join(BeautifulSoup(html, features="html.parser").findAll(text=True)))
    f.close()
    a_file = open("demo.txt", "r")
    for number, line in enumerate(a_file):
        if "Test Description" in line:
            line_number = number
            break
    contents = a_file.readlines()
    if os.path.exists("demo.txt"):
        os.remove("demo.txt")
    return contents[0]


def check_repeated_data(check_id):
    """
    This Function checks if the particular record is already exists in the csv file.
    :param id: Unique ID of the test case
    :return: True if record is not exists, otherwise False.
    """
    data = pd.read_csv("university_records.csv")
    ids = data['Test ID'].tolist()
    if check_id in ids:
        return True
    else:
        return False


def write_data(filename, md_file, feature):
    """
    This function writes the data into the csv file.

    :param filename: CSV file name
    :param md_file: MD File Name
    :param feature: Test Feature
    """
    row = [[feature]]
    with open(filename, 'a+') as csvfile:
        writer_obj = csv.writer(csvfile)
        table_data = pd.read_table(md_file, sep="|", header=1, index_col=1, skipinitialspace=True)
        table_row = table_data.dropna(axis=1, how='all')
        for i in range(1, 7):
            var = table_row.iloc[i, -1]
            if str(var) == 'nan':
                var = "NA"
            var = var.strip()
            row.append([var])
        description = get_description(md_file).rstrip()
        row.append([description])
        # print(row[1])
        if not check_repeated_data("{}".format(row[1])):
            writer_obj.writerow(row)
        else:
            print("Record Already exists.")
            csvfile.close()
    csvfile.close()


parser = argparse.ArgumentParser()
parser.add_argument("--directory", help="Add Test Feature", default="/home/afour/lynx/Provisioning/")
args = parser.parse_args()


def create_summery():
    path = args.directory
    feature = os.path.basename(os.path.normpath(args.directory))
    create_csv(FILENAME, FIELDS)
    for f in os.listdir(path):
        f = os.path.abspath("{}{}".format(path, f))
        write_data(FILENAME, f, feature)


# Start of the Program
create_summery()
