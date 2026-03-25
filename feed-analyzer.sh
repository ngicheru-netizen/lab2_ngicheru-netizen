#!/bin/bash

input_file="twitter_dataset.csv"
python3 -c "import csv; f=open('$input_file', newline='', encoding='utf-8'); r=csv.DictReader(f); [print((row.get('Username') or '').strip()) for row in r]"\
    cut -d',' -f2 "$input_file" | tail -n +2 | sort | uniq -c | sort -nr | head -n 5 | awk '{printf "%-10s %s\n", $1, $2}'
# if [ -z "$input_file" ]; then
#     echo "Usage: bash feed-analyzer.sh twitter_dataset.csv"
#     exit 1
# fi

