#!/usr/bin/env python3

import re, csv, os

def filter_urls(csv_file_path, regex_pattern, output, filename):
    output_file_path = os.path.join(output, filename)

    with open(csv_file_path, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the first row (header)
        matching_urls = []
        for row in reader:
            if len(row) > 1:
                url = row[1]
                if re.search(regex_pattern, url):
                    matching_urls.append(url)
    
    with open(output_file_path, 'w') as output_file:
        for url in matching_urls:
            output_file.write(url + '\n')

def parse_url(file_path, output):
    cid_regex = r"(Qm[1-9A-HJ-NP-Za-km-z]{44}|baf[A-Za-z2-7]{56})"
    dns_regex = r"^https?://[a-zA-Z0-9-]+\.on\.fleek\.co"

    filter_urls(file_path, cid_regex, output, "cid_result.txt")
    filter_urls(file_path, dns_regex, output, "dns_result.txt")
