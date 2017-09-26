docstr = """
Auditor

Usage: auditor.py [-hcv] (<file> <config>) [-o <output.csv>] [-c --clean] [--verbose]

Options:
  -h --help                                     show this message and exit
  -v --version                                  Show version
  -o <output.csv> --output=<output.csv>         optional output file for results
  -c --clean                                    remove rows of a csv that have control strings
  --verbose                                     print errors with the mappings handler

Instructions:
  First run auditor on the file you want to alter. This will give a csv with the same number of
rows with some cells replaced by control strings.
  Then run auditor with the -c flag on the control string output. This will give a much smaller
csv that only has the rows that you want. No blacklisted items, only whitelisted, no empty data
no bad data.

$ auditor raw_data.txt auditor.conf.yaml -o data/audited.unclean.csv -v > logs/auditor.unclean.log
$ auditor -c data/audited.unclean.csv auditor.conf.yaml -o data/auditor.clean.csv -v > logs/auditor.clean.log
"""
import csv

from docopt import docopt
import yaml

from .mappings import Mappings
from auditor.version import __version__

_file = '<file>'
_config = '<config>'
_output = '--output'
_do_clean = '--clean'
_verbose = '--verbose'

def main(args):
    with open(args[_config], 'r') as config_file:
        global config
        config = yaml.load(config_file.read())

    csv_file = open(args[_file], 'r', encoding=config['csv_encoding'])
    data = csv.reader(csv_file, **config['csv_conf'])

    if not args[_do_clean]:
        data = do_add_headers(data, config.get('new_headers'))
        new_rows = do_audit(data, verbose=args[_verbose])
    else:
        new_rows = do_clean(data)

    if args[_do_clean] and config.get('sort'):
        index = config['headers'].index(config['sort']['header'])
        header = new_rows[0]
        new_rows = new_rows[1:]
        new_rows.sort(key=lambda row : row[index])
        new_rows.insert(0, header)

    if args.get(_output):
        with open(args[_output], 'w') as outfile:
            outfile.write(rows_format(new_rows))
    else:
        print(rows_format(new_rows))

def do_add_headers(data, new_headers):
    new_rows = []
    if not new_headers:
        return data
    for key in new_headers.keys():
        header_data = new_headers[key]
        with open(header_data['lookup_file'], 'r') as lookup_file:
            lookup_data = yaml.load(lookup_file.read())
        for index, row in enumerate(data):
            if index == 0:
                old_headers = row
                row.append(new_headers[key]['name'])
                try:
                    new_rows[index] = row
                except IndexError:
                    new_rows.append(row)
            else:
                lookup_key = row[old_headers.index(header_data['key'])]
                lookup_value = lookup_data.get(lookup_key) or header_data['default'] or ''
                row.append(lookup_value)
                try:
                    new_rows[index] = row
                except IndexError:
                    new_rows.append(row)
    return new_rows

def do_audit(data, verbose):
    new_rows = []
    indices = None
    new_header = None
    mappings = Mappings(config, verbose=verbose)
    for index, row in enumerate(data):
        if index == 0:
            new_header = get_header(row)
            indices = [row.index(header) for header in new_header]
            new_rows.append(new_header)
        else:
            apply_map = get_map(new_header, mappings)
            new_row = get_new_data_row(row, indices, new_header, apply_map)
            if new_row:
                new_rows.append(new_row)
    return new_rows

def get_header(row):
    new_row = []
    for col in row:
        if col in config['headers']:
            new_row.append(col)
    return new_row

def get_map(headers, mappings):
    def apply_map(index, row):
        nonlocal headers
        nonlocal mappings
        cell = row[index]
        for mapping in config['mappings']:
            if headers[index] == mapping['header']:
                for map_index, my_map in enumerate(mapping['maps']):
                    kwargs = {
                        'item': cell,
                        'headers': headers,
                        'header': headers[index],
                        'index': index,
                        'row': row,
                        'map': mapping['maps'][map_index]
                    }
                    cell = mappings.handler(**kwargs)
        return cell
    return apply_map

def get_new_data_row(row, indices, header, apply_map):
    if len(row):
        raw = [row[index] for index in indices]
        mapped = [apply_map(index, raw) for index, cell in enumerate(raw)]
        valid = True
        for cell in mapped:
            if cell == '' or cell == None:
                valid = False
        return mapped if valid else None
    else:
        return None

def do_clean(data):
    new_rows = []
    error_strings = config['error_strings'].values()
    for row in data:
        valid = True
        for cell in row:
            if cell in error_strings:
                valid = False
        for index, cell in enumerate(row):
            if cell == config['control_strings']['empty_okay']:
                row[index] = ''
        if valid:
            new_rows.append(row)
    return new_rows

def rows_format(rows):
    quotechar = config['quotechar_write']
    delim = config['csv_conf']['delimiter']
    text = None
    for row in rows:
        srow = [quotechar + str(cell) + quotechar for cell in row]
        line = delim.join(srow)
        if not text:
            text = line
        else:
            text = '\n'.join([text, line])
    return text + '\n'

def cli_run():
    args = docopt(docstr, version=__version__)
    main(args)

if __name__ == '__main__':
    cli_run()
    exit()

