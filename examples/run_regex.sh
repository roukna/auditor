auditor regex/synthetic_data.csv regex/auditor.example.conf.yaml -o regex/regex.unclean.csv -v > regex/regex.unclean.log
auditor -c regex/regex.unclean.csv regex/auditor.example.conf.yaml -o regex/regex.clean.csv -v > regex/regex.clean.log
