from auditor import __main__
import pandas as pd
import re
import datetime
import yaml


def test_added_headers(input_file, config_file, output_file):
    cmd_args = {'--clean': 0,
                '--output': output_file,
                '--verbose': 0,
                '<config>': config_file,
                '<file>': input_file}
    __main__.main(cmd_args)

    with open(config_file, 'r') as c_file:
        config = yaml.load(c_file.read())

    df = pd.read_csv(output_file)
    new_headers = config.get('new_headers')
    for n_header in new_headers:
        assert n_header in df.columns


def test_data_sorted(input_file, config_file, output_file):
    cmd_args = {'--clean': 1,
                '--output': output_file,
                '--verbose': 0,
                '<config>': config_file,
                '<file>': input_file}
    __main__.main(cmd_args)

    with open(config_file, 'r') as c_file:
        config = yaml.load(c_file.read())
    sort_field = config['sort']['header']

    df = pd.read_csv(output_file, usecols=[sort_field])
    df_list = df[sort_field].tolist()
    assert all(df_list[i] <= df_list[i+1] for i in range(len(df_list)-1))


def test_date_formatted(header, config, output_file):
    df = pd.read_csv(output_file, usecols=[header])
    df_list = df[header].tolist()
    assert all(df_list[i] in config['error_strings']['empty_cell'] or datetime.datetime.strptime(df_list[i], '%Y-%m-%d') for i in range(len(df_list)-1))


def test_regex(header, lookup_file, output_file, no_regex):
    with open(lookup_file, 'r') as l_file:
        lookup = yaml.load(l_file.read())

    df = pd.read_csv(output_file, usecols=[header])
    df_list = df[header].tolist()
    for l_val in lookup:
        regex = re.compile(l_val['pattern'])
        x = [m.group(0) for l in df_list for m in [regex.search(str(l))] if m]
        x = [t for t in x if x != no_regex]
        assert not (len(x))


def test_whitespace_stripped(header, output_file):
    df = pd.read_csv(output_file, usecols=[header])
    df_list = df[header].tolist()
    whitespace = tuple(' \n\r\t')
    assert all(not str(i).startswith(whitespace) and not str(i).endswith(whitespace) for i in range(len(df_list)-1))


def test_mappings(input_file, config_file, output_file):
    cmd_args = {'--clean': 0,
                '--output': output_file,
                '--verbose': 0,
                '<config>': config_file,
                '<file>': input_file}

    __main__.main(cmd_args)

    with open(config_file, 'r') as c_file:
        config = yaml.load(c_file.read())

    for mapping in config['mappings']:
        header = mapping['header']
        for map_index, m_map in enumerate(mapping['maps']):
            if type(m_map) != str:
                map_type = m_map['func']
            else:
                map_type = m_map
            # print(header, map_type)

            if map_type == 'format_date':
                test_date_formatted(header, config, output_file)
            if map_type == 'regex':
                lookup_file = (config['regexs'][0])['vals_file_path']
                no_regex = config['error_strings']['no_regex_match']
                test_regex(header, lookup_file, output_file, no_regex)
            if map_type == 'strip_whitespace':
                test_whitespace_stripped(header, output_file)


if __name__ == '__main__':
    input_file = 'test_audit.csv'
    output_file = 'file.csv'
    config_file = '/Users/rsengupta/workspace/auditor/auditor/auditor.example.conf.yaml'
    test_added_headers(input_file, config_file, output_file)
    test_data_sorted(input_file, config_file, output_file)
    test_mappings(input_file, config_file, output_file)
    exit()


