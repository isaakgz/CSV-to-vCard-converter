# CSV to vCard Converter

Simple Python script to convert contacts to vCard (.vcf) files. Supports CSV input or pasting directly into the terminal. Default output is timestamped at `/contacts/contacts_YYYYMMDD_HHMMSS.vcf`, and the script creates the target folder if missing.

## Requirements
- Python 3.7+

## Install
No install needed. Clone the repo and run the script from the project directory.

## Usage
### Paste mode (interactive)
```
python3 csv_to_vcard.py --paste
```
- Paste contacts line by line, then press Enter and Ctrl+D to finish.
- Accepted delimiters: tab, comma, or spaces between Name and Phone.
- Example input:
```
UC1022	+251901418341
UC1021	+251910515447
UC1015	+25191755 9317
```

### CSV mode
```
python3 csv_to_vcard.py --csv path/to/contacts.csv
```
- CSV must have headers: `Name,Phone`.

### Custom output path
```
python3 csv_to_vcard.py --paste --output ~/contacts/contacts.vcf
```

## Phone formatting
- Strips spaces from the phone field.
- Converts Ethiopian numbers from `+2519...` or `2519...` to `09...`.

## Output
- vCard 3.0 entries, one per contact.

## Tips
- If `/contacts` is root-owned, use an output you own (e.g., `~/contacts/contacts.vcf`).
- The script auto-creates the destination directory.
