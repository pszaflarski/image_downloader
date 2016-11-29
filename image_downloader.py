import csv
import tkinter as tk
from tkinter import filedialog

# import openpyxl

from urllib import request
from urllib import error
import datetime


# def excel_work(filename):
#     wb = openpyxl.load_workbook(filename)
#     wb_out = []
#     for sheet in wb:
#         temp = [[x.value for x in row] for row in sheet.iter_rows()]
#         wb_out += temp
#     return (x for x in wb_out)


def csv_work(filename):
    f = open(filename, 'r', encoding='utf-8')
    reader = csv.reader(f)
    return reader


def write_audit(file, row):
    try:
        csv.writer(open(file, mode='a', encoding='utf-8', errors='ignore'), lineterminator='\n').writerow(row)
    except FileNotFoundError:
        csv.writer(open(file, mode='w', encoding='utf-8', errors='ignore'), lineterminator='\n').writerow(row)


if __name__ == '__main__':

    has_headers = True
    audit_file = 'audit_' + str(datetime.datetime.today()).replace('-', '').replace(':', '').replace('.', '').replace(
        ' ', '') + '.csv'

    # get a file dialogue box
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # quit if you hit cancel
    if file_path == '':
        audit = ["cancelled by user"]
        print(audit)
        write_audit(audit_file, audit)
        quit()

    # convert the file to an iterator
    if file_path.split('.')[-1] == 'csv':
        reader = csv_work(file_path)
    elif file_path.split('.')[-1] == 'xlsx':
        # reader = excel_work(file_path)
        pass

    # loop through and download links
    while True:
        try:
            row = next(reader)
        except StopIteration:
            break

        if has_headers:
            has_headers = False
            continue

        key = row[0]
        links = row[1:]

        for index, link in enumerate(links):
            ext = link.split('.')[-1]
            name = key + '_' + str(index) + '.' + ext

            try:
                request.urlretrieve(link, name)
                audit = ["successfully downloaded", name, link]
            except error.HTTPError:
                audit = ["error downloading", name, link]
            except (error.URLError, ValueError):
                audit = ["invalid link", name, link]
            except Exception:
                audit = ["unknown error", name, link]

            print(audit)
            write_audit(audit_file, audit)
