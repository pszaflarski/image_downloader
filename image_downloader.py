import csv
import tkinter as tk
from tkinter import filedialog

# import openpyxl

from urllib import request
from urllib import error
import datetime
import requests


# def excel_work(filename):
#     wb = openpyxl.load_workbook(filename)
#     wb_out = []
#     for sheet in wb:
#         temp = [[x.value for x in row] for row in sheet.iter_rows()]
#         wb_out += temp
#     return (x for x in wb_out)

def download_image(link, filename):
    headers = {'user-agent': 'Mozilla/5.0'}
    p = requests.get(
        link,
        headers=headers, stream=True)

    if p.status_code != 200: raise Exception

    with open('downloads\\'+filename, 'wb') as f:
        for chunk in p.iter_content(1024):
            f.write(chunk)


def csv_work(filename):
    f = open(filename, 'r', encoding='windows-1252', errors='ignore')
    reader = csv.reader(f)
    return reader


def write_audit(file, row):
    try:
        csv.writer(open(file, mode='a', encoding='utf-8', errors='ignore'), lineterminator='\n').writerow(row)
    except FileNotFoundError:
        csv.writer(open(file, mode='w', encoding='utf-8', errors='ignore'), lineterminator='\n').writerow(row)


if __name__ == '__main__':

    has_headers = True

    # get a file dialogue box
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    folder = file_path.split('.')[0].split('\\')[-1].split('/')[-1]

    audit_file = 'audit_' + str(datetime.datetime.today()).replace('-', '').replace(':', '').replace('.', '').replace(' ', '') + '.csv'

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

    # loop through and and build dict
    d = {}
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
        if key not in d: d[key] = ([],set())
        for index, full_link in enumerate(links):
            link = full_link.split("?")[0]
            link = link.strip()

            if link == '' : continue

            if link not in d[key][1]: d[key][0].append(link)


    for key in d:
        for index, link in enumerate(d[key][0]):
            ext = link.split('.')[-1]
            name = key + '_' + str(index) + '.' + ext
            try:
                download_image(link, name)
                audit = ["successfully downloaded", name, link]
            except error.HTTPError:
                audit = ["error downloading", name, link]
            except (error.URLError, ValueError):
                audit = ["invalid link", name, link]
            except Exception:
                audit = ["unknown error", name, link]

            print(audit)
            write_audit(audit_file, audit)
