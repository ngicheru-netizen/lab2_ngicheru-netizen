Data Detective Lab

Run it with:
python3 data-dective.py
bash feed-analyzer.sh

To test the clean_data function, I added 3 "bad" rows to the dataset, but removed them once it was confirmed that the function ran as needed.

For feed-analyzer.sh I used:
python3 -c "import csv; f=open('$input_file', newline='', encoding='utf-8'); r=csv.DictReader(f); [print((row.get('Username') or '').strip()) for row in r]"

The reason is simple: this CSV has quoted text with commas and line breaks.
Plain cut is line-based, so it can break rows and pull the wrong field so I was getting numbers instead of usernames.

After usernames are extracted correctly, the Bash part is still:
sort | uniq -c | sort -nr | head -n 5
