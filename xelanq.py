from __future__ import print_function

import csv
import glob
from collections import defaultdict

"""XElanQ v0.1a."""

#  Python script for creating a CSV file from an output generated by
#  the software of Perkin Elmer Elan DRC II Inductively Coupled
#  Plasma Mass Spectrometer (ICP-MS).

#  Currently only works for (certain types of) TotalQuant report files.

import sys

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


def get_value(value):
    if not value:
        return 'N/A'
    elif value == 'S':
        return 'S'
    else:
        value = float(value)
        if value > 100:
            return int(value)
        else:
            return round(value, 1)


def parse(f_name):
    with open(f_name, 'r') as f:
        content = [x.strip() for x in f.readlines()]

    idx = 0
    data_dict = defaultdict(dict)
    headers = set()
    if content[15] == 'ppb':
        file_type = 'TQ'
    else:
        file_type = 'CC'
    while idx < len(content):
        header = content[idx], content[idx + 1]
        headers.add(header)
        idx += 15
        code = content[idx - 15]
        # if code.startswith('Standard') or code.startswith('Blank'):
        #     skip = True
        # else:
        #     skip = False
        data = []
        if file_type == 'TQ':
            idx += 1
        while idx < len(content):
            if ',' not in content[idx]:
                break
            data.append(content[idx])
            idx += 1
        # if skip:
        #     continue
        buffer = StringIO('\n'.join(data))
        data = []
        for line in csv.reader(buffer):
            if file_type == 'CC':
                data.extend(line[i:i + 7] for i in range(1, len(line), 7))
            else:
                data.append(line)
        for measurement in data:
            if file_type == 'CC':
                if measurement[-1] == 'ppb':
                    data_dict[measurement[0]][header] = get_value(measurement[4])
            if file_type == 'TQ':
                data_dict[measurement[0]][header] = get_value(measurement[1])

    return data_dict, file_type, headers


def save(data, headers, csvfilename):
    headers = list(headers)
    with open(csvfilename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(h[0] for h in [('Element', '')] + headers)
        writer.writerow(h[1] for h in [('Element', '')] + headers)
        for element, values in data.items():
            writer.writerow([element] + [values[header] for header in headers])



def parse_and_save():
    files = glob.glob("**/*.rep", recursive=True)
    files.insert(0, "EXIT")
    for i in range(0, len(files)):
        print(i, ":", files[i])
    print(len(files) - 1, "file(s) detected")
    file_idx = int(input('Which file? '))
    if (file_idx == 0) or (file_idx not in range(0, len(files))):
        sys.exit()

    repfilename = str(files[int(file_idx)])
    # .rep file that will be processed;

    csvfilename = repfilename.split('.')[0].rstrip() + "2.csv"
    data, _, headers = parse(repfilename)
    save(data, headers, csvfilename)


def find(code_to_find):
    files = glob.glob("**/*.rep", recursive=True)
    for file in files:
        found = False
        data, file_type, headers = parse(file)
        for code, date in headers:
            if code_to_find == code:
                print(date, code, file_type)
                code_date = code, date
                found = True
                break
        if found:
            for element, values in data.items():
                print(element, values.get(code_date, 'Not found'))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        parse_and_save()
    else:
        find(sys.argv[1])
