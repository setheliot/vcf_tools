# read in a file containing 1 or more vcf records and returns whether all of the contained vcf records are valid

import re
import sys

def is_valid_vcf_record(record):
    # Split the record into lines
    lines = record.split('\n')

    # Check if the record starts with BEGIN:VCARD and ends with END:VCARD
    if not lines[0].strip() == 'BEGIN:VCARD' or not lines[-1].strip() == 'END:VCARD':
        return False, None

    # Define regular expressions for common VCF fields
    n_regex = re.compile(r'^N:([^;]*);([^;]*);?([^;]*)?;?([^;]*)?;?([^;]*)?$')
    fn_regex = re.compile(r'^FN:(.+)$')
    email_regex = re.compile(r'^EMAIL;TYPE=(.+?):(.+)$')
    tel_regex = re.compile(r'^TEL;TYPE=(.+?):(.+)$')

    formatted_name = None

    # Iterate through the lines and validate each field
    for line in lines[1:-1]:  # Skip BEGIN:VCARD and END:VCARD lines
        if line:
            #print (line)
            if line.startswith(' ') or line.startswith('\t'):
                continue
            else:
                line = line.strip()
            field_name, field_value = line.split(':', 1)
            if field_name == 'FN':
                formatted_name = line
                if not fn_regex.match(line):
                    print(f"Invalid FN field: {line}")
                    return False, formatted_name
            elif field_name == 'N':
                if not n_regex.match(line):
                    print(f"Invalid N field: {line}")
                    return False, None
            elif field_name == 'EMAIL':
                if not email_regex.match(line):
                    print(f"Invalid EMAIL field: {line}")
                    return False, None
            elif field_name == 'TEL':
                if not tel_regex.match(line):
                    print(f"Invalid TEL field: {line}")
                    return False, None
            # Add more field validations as needed

    return True, formatted_name

def validate_vcf_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        records = []
        current_record = []
        for line in file_content.split('\n'):
#            line = line.strip()
            if line == 'BEGIN:VCARD':
                current_record = []
                current_record.append(line)
            elif line == 'END:VCARD':
                current_record.append(line)
                records.append('\n'.join(current_record))
                current_record = []
            else:
                current_record.append(line)
        i = 0
        for record in records:
            i+=1
            print(f"Validating record {i}")
            is_valid, formatted_name = is_valid_vcf_record(record)
            if formatted_name:
                print(f"Formatted name: {formatted_name}")
            if not is_valid:
                #print(f"Invalid record: {record}")
                return False
    return True

if __name__ == '__main__':
    file_path = sys.argv[1]
    if validate_vcf_file(file_path):
        print("All VCF records are valid.")
    else:
        print("One or more VCF records are invalid.")