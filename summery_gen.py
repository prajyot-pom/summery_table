#!/usr/bin/python3

import csv
import os
import pandas as pd
import markdown
from bs4 import BeautifulSoup
from pathlib import Path
import sys


class SummeryGenerator:
    "This class contains APIs for generating a summery of test procedures."

    fields = ['Feature', 'Test ID', 'Last Tested', 'Image Version', 'Status', 'Automation', 'Designed-By', 'Keywords',
              'Test Description']

    def __init__(self, file_name="summery_table.csv", test_dir="/home/kmalhotra/code/prajyot/lmm/test_procedure/docs/",
                 html_file="index.html"):
        self.file_name = file_name
        self.test_dir = test_dir
        self.html_file = html_file
        self.neg_files = []

    def get_list_of_files(self, dir_path):
        """
        This function creates and returns list of all files inside directories and subdirectories.
        :param dir_name: Path to parent directory
        :return: List of all files present in directory and sub-directories.
        """
        list_of_file = os.listdir(dir_path)
        all_files = []
        for entry in list_of_file:
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                all_files = all_files + self.get_list_of_files(full_path)
            else:
                all_files.append(full_path)
        # create one more variable which contains list of excluded files
        if "{}index.md".format(self.test_dir) in all_files:
            self.neg_files.append("{}index.md".format(self.test_dir))
            all_files.remove("{}index.md".format(self.test_dir))
        return all_files

    def create_csv_file(self):
        """
        This function creates a csv file containing summery table if not already exists.
        :param filename: CSV file name
        :param field: Fields to be added in the csv file
        """
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

        with open(self.file_name, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(SummeryGenerator.fields)
        csvfile.close()

    def get_test_description(self, md_file):
        """
        This function converts the md file into html and from html to text using html parser
        and returns the test description.
        After fetching the description, it deletes the text file.

        :param md_file: Mkdocs file
        :return: Test Description in string format
        """
        html = markdown.markdown(open(md_file).read())
        f = open("temp.txt", 'w')
        f.write("".join(BeautifulSoup(html, features="html.parser").findAll(text=True)))
        f.close()
        temp = open("temp.txt", "r")
        for number, line in enumerate(temp):
            if "Test Description" in line or "Description" in line:
                break
        contents = []
        for ln in temp.readlines():
            if "Dependencies" not in ln:
                contents.append(ln)
            else:
                break
        if os.path.exists("temp.txt"):
            os.remove("temp.txt")
        if len(contents) == 1:
            return contents[0]
        else:
            return ' '.join([str(elem).rstrip() for elem in contents])

    def check_repeated_data(self, check_id):
        """
        This Function checks if the particular record is already exists in the csv file.
        If it is exists, this function delets the particular record.
        :param check_id: Unique ID of the test case
        """
        lines = []
        with open(self.file_name, 'r') as read_file:
            reader = csv.reader(read_file)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == check_id:
                        lines.remove(row)
        read_file.close()
        with open(self.file_name, 'w') as write_file:
            writer = csv.writer(write_file)
            writer.writerows(lines)
        write_file.close()

    def write_data(self, md_file, feature):
        """
        This function writes the data from md file into the csv file.
        And creates html and pdf file for the summery table.

        :param filename: CSV file name
        :param md_file: MD File Name
        :param feature: Test Feature
        """
        row = [feature]
        with open(self.file_name, 'a+') as csv_file:
            writer_obj = csv.writer(csv_file)
            try:
                print(md_file)
                table_data = pd.read_table(md_file, sep="|", header=1, index_col=1, skipinitialspace=True)
                table_row = table_data.dropna(axis=1, how='all')
            except IndexError as e:
                print("Index Error: {}".format(e))
                print(self.neg_files)
                sys.exit(1)
            for i in range(1, 8):
                var = table_row.iloc[i, -1]
                if str(var) == 'nan':
                    var = "NA"
                var = var.strip()
                row.append(var)
            description = self.get_test_description(md_file).rstrip()
            row.append(description)
            self.check_repeated_data("{}".format(row[1]))
            writer_obj.writerow(row)
        csv_file.close()

    def create_summery_table(self):
        self.create_csv_file()
        list_of_files = self.get_list_of_files(self.test_dir)
        for f in list_of_files:
            name, exts = os.path.splitext(f)
            if exts == ".md":
                feature = os.path.basename(os.path.normpath(Path(f).parent))
                self.write_data(f, feature)
                continue
            else:
                print("File extension is other than .md. Skipping the file {}...".format(f))
                self.neg_files.append(f)
                continue
        csv_to_convert = pd.read_csv(self.file_name)
        if os.path.exists(self.html_file):
            os.remove(self.html_file)
        csv_to_convert.to_html(self.html_file)


summery_obj = SummeryGenerator()
summery_obj.create_summery_table()