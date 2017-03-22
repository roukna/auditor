import json
import re
import yaml
import dateutil.parser as date_parser

class Mappings(object):

    def __init__(self, config, **kwargs):
        self.bad_data = config['error_strings']['bad_data']
        self.empty_cell = config['error_strings']['empty_cell']
        self.blacklisted = config['error_strings']['blacklisted']
        self.not_whitelisted = config['error_strings']['not_whitelisted']
        self.no_regex_match = config['error_strings']['no_regex_match']
        self.empty_okay_string = config['control_strings']['empty_okay']

        self.whitelists = {}
        for item in config['whitelist']:
            with open(item['vals_file_path']) as values_file:
                self.whitelists[item['header_name']] = self.parse(values_file)

        self.blacklists = {}
        for item in config['blacklist']:
            with open(item['vals_file_path']) as values_file:
                self.blacklists[item['header_name']] = self.parse(values_file)

        self.regexs = {}
        for item in config['regexs']:
            with open(item['vals_file_path']) as values_file:
                self.regexs[item['header_name']] = self.parse(values_file)

    def format_date(self, item, header):
        try:
            if item == '':
                return self.empty_cell
            else:
                return date_parser.parse(item).strftime('%Y-%m-%d')
        except Exception as ex:
            print(ex)
            return self.bad_data

    def number(self, item, header):
        try:
            if item == '':
                return self.empty_cell
            else:
                return float(item)
        except Exception as ex:
            print(ex)
            return self.bad_data

    def is_whitelist(self, item, header):
        try:
            if item == '':
                return self.empty_cell
            else:
                return item if item in self.whitelists.get(header) else self.not_whitelisted
        except Exception as ex:
            print(ex)
            return self.bad_data

    def is_blacklist(self, item, header):
        try:
            if item == '':
                return self.empty_cell
            else:
                return self.blacklisted if item in self.blacklists.get(header) else item
        except Exception as ex:
            print(ex)
            return self.bad_data

    def regex(self, item, header):
        try:
            if item == '':
                return self.empty_cell
            else:
                regexs = self.regexs.get(header)
                for r in regexs.keys():
                    regex = re.compile(r)
                    match = regex.match(item)
                    if match:
                        try:
                            return match.group(1)
                        except Exception as ex:
                            print(ex)
                            return regex[r]
                # no match found
                return self.no_regex_match
        except Exception as ex:
            print(ex)
            return self.bad_data

    def empty_okay(self, item, header):
        if item == '' or item == None:
            return self.empty_okay_string
        else:
            return item

    def parse(self, infile):
        text = infile.read()
        try:
            values = yaml.load(text)
        except Exception as ex:
            print(ex)
            print('Value files must be written in yaml.')
        return values if values else []



