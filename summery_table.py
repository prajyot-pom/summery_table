import csv
import os
import pandas as pd
import markdown
from bs4 import BeautifulSoup
from pathlib import Path
import sys
from fpdf import FPDF


"""
This script takes absolute path of the directory containing all the *.md files
and add summery of each file in the summery table.
"""

# field names
FIELDS = ['Feature', 'Test ID', 'Last Tested', 'Image Version', 'Status', 'Automation', 'Designed-By', 'Keywords',
          'Test Description']

# name of csv file
FILENAME = "summery_table.csv"
CURR = os.getcwd()
print(CURR)
TESTDIR = "{}/docs/".format(CURR)


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
    if "{}/docs/index.md".format(CURR) in all_files:
        all_files.remove("{}/docs/index.md".format(CURR))
    return all_files


def create_csv_file(filename, field):
    """
    This function creates a csv file containing summery table if not already exists.
    :param filename: CSV file name
    :param field: Fields to be added in the csv file
    """
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field)
    csvfile.close()


def get_test_description(md_file):
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
    contents = list()
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


def check_repeated_data(check_id):
    """
    This Function checks if the particular record is already exists in the csv file.
    If it is exists, this function delets the particular record.
    :param check_id: Unique ID of the test case
    :return: True if record is not exists, otherwise False.
    """
    lines = list()
    with open(FILENAME, 'r') as read_file:
        reader = csv.reader(read_file)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == check_id:
                    lines.remove(row)
    read_file.close()
    with open(FILENAME, 'w') as write_file:
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
        try:
            table_data = pd.read_table(md_file, sep="|", header=1, index_col=1, skipinitialspace=True)
            table_row = table_data.dropna(axis=1, how='all')
        except IndexError as e:
            print("Index Error: {}".format(e))
            sys.exit(1)
        for i in range(1, 8):
            var = table_row.iloc[i, -1]
            if str(var) == 'nan':
                var = "NA"
            var = var.strip()
            row.append(var)
        description = get_test_description(md_file).rstrip()
        row.append(description)

        if check_repeated_data("{}".format(row[1])):
            writer_obj.writerow(row)
    csv_file.close()


def create_summery_table():
    create_csv_file(FILENAME, FIELDS)
    list_of_files = get_list_of_files(TESTDIR)
    for f in list_of_files:
        name, exts = os.path.splitext(f)
        if exts == ".md":
            feature = os.path.basename(os.path.normpath(Path(f).parent))
            write_data(FILENAME, f, feature)
            continue
        else:
            print("File extension is other than .md. Skipping the file {}...".format(f))
            continue
    csv_to_convert = pd.read_csv(FILENAME)
    if os.path.exists("index.html"):
        os.remove("index.html")
    csv_to_convert.to_html("index.html")


# Start of the Program
create_summery_table()
print("Summery Table Created. Please open index.html in your browser.")


# pdf = FPDF(orientation='L')
# pdf.add_page()
# page_width = pdf.w - 2 * pdf.l_margin
#
# pdf.set_font('Times', 'B', 14.0)
# pdf.cell(page_width, 0.0, 'Summary Table', align='C')
# pdf.ln(10)
# print("This is page width:{}".format(page_width))
# pdf.set_font('Courier', '', 8)
#
# col_width = page_width / 6
#
# pdf.ln(1)
#
# th = pdf.font_size
# with open(FILENAME, newline='') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         pdf.cell(30, th, row[0], border=1)
#         pdf.cell(30, th, row[1], border=1)
#         pdf.cell(20, th, row[2], border=1)
#         pdf.cell(25, th, row[3], border=1)
#         pdf.cell(15, th, row[4], border=1)
#         pdf.cell(20, th, row[5], border=1)
#         pdf.cell(20, th, row[6], border=1)
#         pdf.cell(20, th, row[7], border=1)
#         pdf.cell(80, th, row[8], border=1)
#         pdf.ln(th)
#
#     pdf.ln(10)
#
# pdf.set_font('Times', '', 10.0)
# pdf.cell(page_width, 0.0, '- end of report -', align='C')
#
# pdf.output('summery_table.pdf', 'F')

# ====================================================================
# pdf = FPDF()
# pdf.add_page()
# page_width = pdf.w - 2 * pdf.l_margin
#
# pdf.set_font('Times', 'B', 14.0)
# pdf.cell(page_width, 0.0, 'Students Data', align='C')
# pdf.ln(10)
#
# pdf.set_font('Courier', '', 6)
#
# col_width = page_width / 10
#
# pdf.ln(1)
#
# th = pdf.font_size
# with open(FILENAME, newline='') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         pdf.cell(col_width, th, str(row[0]), border=1)
#         pdf.cell(col_width, th, row[1], border=1)
#         pdf.cell(col_width, th, row[2], border=1)
#         pdf.cell(col_width, th, row[3], border=1)
#         # pdf.cell(col_width, th, str(row[0]), border=1)
#         pdf.cell(col_width, th, row[4], border=1)
#         pdf.cell(col_width, th, row[5], border=1)
#         pdf.cell(col_width, th, row[6], border=1)
#         # pdf.cell(col_width, th, str(row[0]), border=1)
#         pdf.cell(col_width, th, row[7], border=1)
#         pdf.cell(col_width, th, row[8], border=1)
#         pdf.ln(th)
#
#     pdf.ln(10)
#
# pdf.set_font('Times', '', 8.0)
# pdf.cell(page_width, 0.0, '- end of report -', align='C')
#
# pdf.output('student.pdf', 'F')
