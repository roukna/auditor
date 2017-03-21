import json
import yaml
import dateutil.parser as date_parser

class Mappings(object):

    def __init__(self, config, **kwargs):
        self.bad_data_string = config['bad_data_string']
        self.empty_cell_string = config['empty_cell_string']
        self.blacklisted_string = config['blacklisted_string']
        self.not_whitelisted_string = config['not_whitelisted_string']
        self.whitelists = {}
        for item in config['whitelist']:
            with open(item['vals_file_path']) as values_file:
                self.whitelists[item['header_name']] = self.parse(values_file)

        self.blacklists = {}
        for item in config['blacklist']:
            with open(item['vals_file_path']) as values_file:
                self.blacklists[item['header_name']] = self.parse(values_file)

        self.lookups = {}
        for item in config['lookups']:
            with open(item['vals_file_path']) as values_file:
                self.lookups[item['header_name']] = self.parse(values_file)

    def format_date(self, item, header):
        try:
            if item == '':
                return self.empty_cell_string
            else:
                return date_parser.parse(item).strftime('%Y-%m-%d')
        except:
            return self.bad_data_string

    def number(self, item, header):
        try:
            if item == '':
                return self.empty_cell_string
            else:
                return float(item)
        except:
            return self.bad_data_string

    def is_whitelist(self, item, header):
        try:
            if item == '':
                return self.empty_cell_string
            else:
                return item if item in self.whitelists.get(header) else self.not_whitelisted_string
        except:
            return self.bad_data_string

    def is_blacklist(self, item, header):
        try:
            if item == '':
                return self.empty_cell_string
            else:
                return self.blacklisted_string if item in self.blacklists.get(header) else item
        except:
            return self.bad_data_string

    def lookup(self, item, header):
        try:
            return self.lookups.get(header).get(item)
        except:
            return self.bad_data_string

    def parse(self, infile):
        text = infile.read()
        try:
            values = yaml.load(text)
        except:
            print('Value files must be written in yaml.')
        return values



