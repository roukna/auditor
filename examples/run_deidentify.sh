auditor deidentify/synthetic_data.csv deidentify/auditor.example.conf.yaml -o deidentify/deidentify.unclean.csv -v > deidentify/deidentify.unclean.log
auditor -c deidentify/deidentify.unclean.csv deidentify/auditor.example.conf.yaml -o deidentify/deidentify.clean.csv -v > deidentify/deidentify.clean.log
