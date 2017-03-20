docstr = """
Auditor

Usage: auditor.py [-h] (<file> <config>) [-o <output.csv>]

Options:
  -h --help                                     show this message and exit
  -o <output.csv> --output=<output.csv>         optional output file for results

"""
import csv

from docopt import docopt
import yaml

from .mappings import Mapping

_file = '<file>'
_config = '<config>'
_output = '--output'

# config magic strings
# config mapping magic strings

def main(args=docopt(docstr)):
    with open(args[_config], 'r') as config_file:
        global config
        config = yaml.load(config_file.read())

    csv_file = open(args[_file], 'r')
    data = csv.reader(csv_file, **config['csv_conf'])

    new_rows = []
    indices = None
    new_header = None
    for index, row in enumerate(data):
        if index == 0:
            new_header = get_header(row)
            indices = [row.index(header) for header in new_header]
            new_rows.append(new_header)
        else:
            mappings = Mapping()
            apply_map = get_map(headers, mappings)
            new_row = get_new_data_row(row, indices, new_header, apply_map)
            new_rows.append(new_row)

    pass

def get_header(row):
    new_row = []
    for col in row:
        if col in config['headers']:
            new_row.append(col)
    return new_row

def get_map(headers, mappings):
    def apply_map(index, cell):
        nonlocal headers
        nonlocal mappings
        for mapping in config['mappings']:
            if headers[index] == mapping['header']:
                return getattr(mappings, mapping['map'])(cell)
    return apply_map

def get_new_data_row(row, indices, header, apply_map):
    raw = [row[index] for index in indices]


    mapped = [apply_map(index, cell) for index, cell in enumerate(raw)]


if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
    exit()

