docstr = """
Auditor

Usage: auditor.py [-h] (<file> <config>) [-o <output.csv>]

Options:
  -h --help                                     show this message and exit
  -o <output.csv> --output=<output.csv>         optional output file for results

"""
import csv

from docopt import docopt
import dateutil.parser as date_parser
import yaml

from .StagingArea import StagingArea

_file = '<file>'
_config = '<config>'
_output = '--output'

# config magic strings
# config mapping magic strings

transforms = {
    'format_date': lambda d : date_parser.parse(d).strftime('%Y-%m-%d')
}

def main(args=docopt(docstr)):
    with open(args[_config], 'r') as config_file:
        global config
        config = yaml.load(config_file.read())

    pass

if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
    exit()

