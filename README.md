# auditor
Makes sure your CSV's remain compliant

There are times that CSV files need either cleaning, or replacement of certain items, or filtering 
of specific values or sorting etc. 

Enter Auditor. This software is meant to scan through and clean your csv in various ways and make sure that
everything is ready to go before your application needs to do the rest of the data processing.

## Configs

Look in docs/config_information.org for a detailed treatment of the configuration options

## Usage

  First run auditor on the file you want to alter. This will give a csv with the same number of
rows with some cells replaced by control strings.

  Then run auditor with the -c flag on the control string output. This will give a much smaller
csv that only has the rows that you want. No blacklisted items, only whitelisted, no empty data
no bad data.

`$ auditor raw_data.txt auditor.conf.yaml -o data/audited.unclean.csv -v > logs/auditor.unclean.log`
`$ auditor -c data/audited.unclean.csv auditor.conf.yaml -o data/auditor.clean.csv -v > logs/auditor.clean.log`
