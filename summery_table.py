import csv
import os
import pandas as pd
import argparse
import markdown
from bs4 import BeautifulSoup
from pathlib import Path

"""
This script takes absolute path of the directory containing all the *.md files
and add summery of each file in the summery table.
"""

# field names
FIELDS = ['Feature', 'Test ID', 'Last Tested', 'Image Version', 'Status', 'Automation', 'Jira', 'Test Description']

# name of csv file
FILENAME = "university_records.csv"


def get_list_of_files(dir_name):
    """
    This function creates and returns list of all files inside directories and subdirectories.
    :param dir_name: Path to parent directory
    :return: List of all files present in directory and sub-directories.
    """
    list_of_file = os.listdir(dir_name)
    all_files = []
    for entry in list_of_file:
        full_path = os.path.join(dir_name, entry)
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)
    return all_files


def create_csv_file(filename, field):
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
            break
    contents = a_file.readlines()
    if os.path.exists("demo.txt"):
        os.remove("demo.txt")
    return contents[0]


def check_repeated_data(check_id):
    """
    This Function checks if the particular record is already exists in the csv file.
    :param check_id: Unique ID of the test case
    :return: True if record is not exists, otherwise False.
    """
    lines = list()
    with open('university_records.csv', 'r') as read_file:
        reader = csv.reader(read_file)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == check_id:
                    lines.remove(row)
    read_file.close()
    with open('university_records.csv', 'w') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(lines)
    write_file.close()
    return True


def write_data(filename, md_file, feature):
    """
    This function writes the data into the csv file.

    :param filename: CSV file name
    :param md_file: MD File Name
    :param feature: Test Feature
    """
    row = [feature]
    with open(filename, 'a+') as csv_file:
        writer_obj = csv.writer(csv_file)
        table_data = pd.read_table(md_file, sep="|", header=1, index_col=1, skipinitialspace=True)
        table_row = table_data.dropna(axis=1, how='all')
        for i in range(1, 7):
            var = table_row.iloc[i, -1]
            if str(var) == 'nan':
                var = "NA"
            var = var.strip()
            row.append(var)
        description = get_description(md_file).rstrip()
        row.append(description)
        print(row[1])
        if check_repeated_data("{}".format(row[1])):
            writer_obj.writerow(row)
    csv_file.close()


parser = argparse.ArgumentParser()
parser.add_argument("--directory", help="Add Test Feature", default="/home/afour/lynx/IDT_Deployment/")
args = parser.parse_args()


def create_summery_table():
    path = args.directory
    create_csv_file(FILENAME, FIELDS)
    list_of_files = get_list_of_files(path)
    for f in list_of_files:
        name, exts = os.path.splitext(f)
        if exts == ".md":
            feature = os.path.basename(os.path.normpath(Path(f).parent))
            write_data(FILENAME, f, feature)
            continue
        else:
            print("File extension is other than .md. Skipping the file...")
            continue
    csv_to_convert = pd.read_csv("university_records.csv")
    csv_to_convert.to_html("index.html")


# Start of the Program
create_summery_table()
print("Summery Table Created. Please open index.html in your browser.")
