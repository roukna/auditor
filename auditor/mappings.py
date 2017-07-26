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

        self.verbose = kwargs.get('verbose')

        self.whitelists = {}
        for item in config.get('whitelist') or []:
            with open(item['vals_file_path']) as values_file:
                self.whitelists[item['header_name']] = self.parse(values_file)

        self.blacklists = {}
        for item in config.get('blacklist') or []:
            with open(item['vals_file_path']) as values_file:
                self.blacklists[item['header_name']] = self.parse(values_file)

        self.regexs = {}
        for item in config.get('regexs') or []:
            with open(item['vals_file_path']) as values_file:
                self.regexs[item['header_name']] = self.parse(values_file)

    def handler(self, **kwargs):
        map = kwargs['map']
        if type(map) != type('string'):
            map = map['func']
        return getattr(self, map)(**kwargs)

    def format_date(self, **kwargs):
        item = kwargs.get('item')
        try:
            if item == '':
                return self.empty_cell
            else:
                return date_parser.parse(item).strftime('%Y-%m-%d')
        except Exception as ex:
            if self.verbose:
                print('format_date exception')
                print(ex)
            return self.bad_data

    def is_whitelist(self, **kwargs):
        item = kwargs.get('item')
        header = kwargs.get('header')
        try:
            if item == '':
                return self.empty_cell
            else:
                return item if item in self.whitelists.get(header) else self.not_whitelisted
        except Exception as ex:
            if self.verbose:
                print('is_whitelist exception')
                print(ex)
            return self.bad_data

    def is_blacklist(self, **kwargs):
        item = kwargs.get('item')
        header = kwargs.get('header')
        try:
            if item == '':
                return self.empty_cell
            else:
                return self.blacklisted if item in self.blacklists.get(header) else item
        except Exception as ex:
            if self.verbose:
                print('is_blacklist exception')
                print(ex)
            return self.bad_data

    def regex(self, **kwargs):
        item = kwargs.get('item')
        header = kwargs.get('header')
        try:
            if item == '':
                return self.empty_cell
            else:
                regexs = self.regexs.get(header)
                for regex in regexs:
                    pattern = re.compile(regex['pattern'])
                    match = pattern.match(item)
                    if match:
                        try:
                            return match.group(1)
                        except Exception as ex:
                            if self.verbose:
                              print('no matched group found for {}, trying to use the value key'.format(item))
                            return regex.get('value')
                # no match found
                return self.no_regex_match
        except Exception as ex:
            if self.verbose:
                print('regex exception')
                print(ex)
            return self.bad_data

    def strip_whitespace(self, **kwargs):
        item = kwargs.get('item')
        return item.strip()

    def empty_okay(self, **kwargs):
        item = kwargs.get('item')
        if item == '' or item == None:
            return self.empty_okay_string
        else:
            return item

    def greater_equal(self, **kwargs):
        try:
            item = kwargs.get('item')
            headers = kwargs.get('headers')
            row = kwargs.get('row')
            arg1 = kwargs.get('map').get('args')[0]
            arg1_val = row[headers.index(arg1)]
            arg2 = kwargs.get('map').get('args')[1]
            arg2_val = row[headers.index(arg2)]
            retval_header = kwargs.get('map').get('retval')[0]
            retval = row[headers.index(retval_header)]
            return retval if arg1_val >= arg2_val else self.bad_data
        except Exception as ex:
            if self.verbose:
                print('greater_equal exception')
                print(ex)
            return self.bad_data

    def parse(self, infile):
        text = infile.read()
        try:
            values = yaml.load(text)
        except Exception as ex:
            if self.verbose:
                print(ex)
                print('Value files must be written in yaml.')
        return values if values else []



