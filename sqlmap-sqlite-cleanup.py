import sqlite3
import csv

# Connect to sqlmap session database
conn = sqlite3.connect('session.sqlite')
cursor = conn.cursor()

# Fetch all id and value entries
cursor.execute("SELECT id, value FROM storage")
rows = cursor.fetchall()

# Function to parse each raw value string
def parse_value(raw):
    records = []
    # First, handle database names and system tables
    parts = raw.split('qjkbq')  # qjkbq is the normal field separator
    for part in parts:
        if not part.strip():
            continue
        # Check for database marker
        if 'deftxwsqp' in part:
            try:
                _, dbname = part.split('deftxwsqp')
                dbname = dbname.replace('qqvbq', '').strip()
                records.append(("Database", dbname, ""))
            except ValueError:
                continue
        # Check for system table marker
        elif 'systxwsqp' in part:
            try:
                _, tablename = part.split('systxwsqp')
                tablename = tablename.replace('qqvbq', '').strip()
                records.append(("Table", tablename, ""))
            except ValueError:
                continue
        # Check for normal field definition
        elif 'txwsqp' in part:
            try:
                field_name, rest = part.split('txwsqp')
                field_type, _ = rest.split('qqvbq')
                records.append(("Field", field_name.strip(), field_type.strip()))
            except ValueError:
                continue
    return records

# Function to substitute markers for human readability
def clean_substituted_value(raw):
    substituted = raw
    substituted = substituted.replace('deftxwsqp', ' [DATABASE] ')
    substituted = substituted.replace('systxwsqp', ' [TABLE] ')
    substituted = substituted.replace('qjkbq', ' [FIELD] ')
    substituted = substituted.replace('txwsqp', ' [TYPE] ')
    substituted = substituted.replace('qqvbq', ' [END] ')
    substituted = substituted.replace('glzvvtxwsqp', ' [VALUE] ')
    substituted = substituted.replace('txwsvv', ' [SEP] ')
    return substituted

# Open CSV for writing
with open('parsed_sqlmap_storage.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["ID", "Type", "Name", "Data", "Substituted Original Value"])  # Header row

    # Parse all entries
    for row in rows:
        record_id = row[0]
        raw_value = row[1]

        # Clean readable version of the raw value
        substituted_value = clean_substituted_value(raw_value)

        # Parse structured fields
        parsed_records = parse_value(raw_value)

        if parsed_records:
            for entry_type, name, data in parsed_records:
                csvwriter.writerow([record_id, entry_type, name, data, substituted_value])
        else:
            # If parsing failed, still write id and substituted raw value
            csvwriter.writerow([record_id, "", "", "", substituted_value])

print("✅ Parsing complete. Output saved to parsed_sqlmap_storage.csv")

# Close database
conn.close()
