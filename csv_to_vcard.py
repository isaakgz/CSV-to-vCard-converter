import argparse
import csv
import os
import sys
from datetime import datetime


def format_phone(phone: str) -> str:
    """
    Convert Ethiopian phone numbers from +251 format to 09 format.
    Example: +251911615924 -> 0911615924
    """
    phone = phone.strip().replace(" ", "")
    if phone.startswith("+2519"):
        return "0" + phone[4:]
    if phone.startswith("2519"):
        return "0" + phone[3:]
    return phone


def contacts_to_vcards(contacts):
    entries = []
    for name, phone in contacts:
        if not name or not phone:
            continue
        formatted_phone = format_phone(phone)
        vcard = (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"FN:{name}\n"
            f"TEL;TYPE=CELL:{formatted_phone}\n"
            "END:VCARD\n"
        )
        entries.append(vcard)
    return entries


def parse_pasted_contacts(raw_text: str):
    contacts = []
    for idx, line in enumerate(raw_text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        if "\t" in line:
            name, phone = line.split("\t", 1)
        elif "," in line and line.count(",") == 1:
            name, phone = line.split(",", 1)
        else:
            parts = line.split()
            if len(parts) < 2:
                print(f"⚠️ Skipping line {idx}: not enough columns -> {line}")
                continue
            name, phone = parts[0], " ".join(parts[1:])
        contacts.append((name.strip(), phone.strip()))
    return contacts


def default_output_path() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"/contacts/contacts_{timestamp}.vcf"


def write_vcards(vcard_entries, vcf_file: str):
    if not vcard_entries:
        print("⚠️ No valid contacts found to convert.")
        return
    os.makedirs(os.path.dirname(vcf_file), exist_ok=True)
    try:
        with open(vcf_file, "w", encoding="utf-8") as f:
            f.writelines(vcard_entries)
    except PermissionError:
        print(f"❌ Error: Permission denied when writing to '{vcf_file}'.")
        return
    except Exception as e:
        print(f"❌ Unexpected error writing vCard file: {e}")
        return
    print(f"✅ Successfully converted {len(vcard_entries)} contacts to {vcf_file}")


def csv_to_vcard(csv_file: str, vcf_file: str):
    """
    Convert contacts from CSV to vCard 3.0 format and save to .vcf file.
    Assumes CSV has headers: Name, Phone
    """
    vcard_entries = []
    try:
        with open(csv_file, newline="", encoding="utf-8") as f:
            try:
                reader = csv.DictReader(f)
                if not reader.fieldnames or not {"Name", "Phone"}.issubset(reader.fieldnames):
                    print("❌ Error: CSV file must contain 'Name' and 'Phone' columns.")
                    return
                for row in reader:
                    name = row.get("Name", "").strip()
                    phone = row.get("Phone", "").strip()
                    if not name or not phone:
                        continue
                    vcard_entries.append((name, phone))
            except csv.Error as e:
                print(f"❌ Error reading CSV file: {e}")
                return
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file}' not found.")
        return
    except PermissionError:
        print(f"❌ Error: Permission denied when reading '{csv_file}'.")
        return
    except Exception as e:
        print(f"❌ Unexpected error opening CSV file: {e}")
        return
    write_vcards(contacts_to_vcards(vcard_entries), vcf_file)


def paste_to_vcard(vcf_file: str):
    raw_text = sys.stdin.read()
    contacts = parse_pasted_contacts(raw_text)
    write_vcards(contacts_to_vcards(contacts), vcf_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert contacts to vCard (.vcf).")
    parser.add_argument("--csv", dest="csv_file", help="Path to CSV with Name and Phone columns.")
    parser.add_argument("--paste", action="store_true", help="Read contacts from pasted stdin (Name<TAB>Phone or Name Phone).")
    parser.add_argument(
        "--output",
        help="Output .vcf file (default: /contacts/contacts_<timestamp>.vcf)",
    )
    args = parser.parse_args()

    output_path = args.output or default_output_path()

    if args.paste:
        print("Paste your contacts now. Use Name<TAB>Phone or Name Phone per line. Press Ctrl+D when done.\n")
        paste_to_vcard(output_path)
    elif args.csv_file:
        csv_to_vcard(args.csv_file, output_path)
    else:
        parser.print_help()
