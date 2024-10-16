# This script reads in a vcf file containing multiple contacts and then writes out a new file containing all the same contacts with
# all of the same fields. 
# You can specify the following clean-up operations:
# * Contacts that do not have a first or last name will have the first name added with the same value as the ORG field
# * Photos will be removed from all contacts
#
# Usage:
# python vcf_convert.py [-h] [-n] [-p] input_file output_file
#
# Arguments:
#   input_file   The input VCF file
#   output_file  The output VCF file
#   -n, --name   Add names to contacts that do not have them
#   -p, --photo  Remove photos from contacts
#
# I created this script after exporting the contacts from my iPhone and finding that because many of them did not have names, they were
# considered invalid when I tried to import them into Google Contacts or Apple iCloud contacts.
# In my case the contacts on the iPhone were created by Exchange.

import argparse
import sys

def process_vcf(input_file, output_file, add_name, remove_photo):

    contacts = read_contacts(input_file)
    processed_contacts = [process_contact(contact, add_name, remove_photo) for contact in contacts]
    write_contacts(output_file, processed_contacts)

    print(f"{len(contacts)} records processed")

def read_contacts(input_file):
    contacts = []
    contact = []
    with open(input_file, 'r') as f_in:
        for line in f_in:
            line = line.strip()
            if not line:
                continue            
            elif line.startswith('BEGIN:VCARD'):
                contact = []
            elif line.startswith('END:VCARD'):
                contacts.append(contact)
            else:
                contact.append(line.strip())
    return contacts


def process_contact(contact, add_name, remove_photo):
        first_name = ''
        last_name = ''
        org = ''
        set_name_to_org = False
        updatedFN = False
        for field in contact:
            if field.startswith('N:'):
                name_parts = field.split(':')[1].split(';')
                last_name = name_parts[0]
                first_name = name_parts[1] if len(name_parts) > 1 else ''
            elif field.startswith('ORG:'):
                org = field.split(':')[1]

        # Determine if we need to set the name to the org for this contact
        if add_name and (not first_name and org):
            first_name = org
            set_name_to_org = True

        new_contact = ['BEGIN:VCARD']

        # if we need to set the name to the org, update the name fields (N and FN)
        # if we need to remove the photo, skip the photo field
        for field in contact:
            if add_name and set_name_to_org and field.startswith('N:'):
                new_contact.append(f'N:{last_name};{first_name}')
            elif add_name and set_name_to_org and field.startswith('FN:'):
                new_contact.append(f'FN:{first_name} {last_name}')
                updatedFN = True;
            elif remove_photo and field.startswith('PHOTO;'):
                break # assumes photo is the last field in the contact
            else:
                new_contact.append(field)

        # if we need to set the name to the org and there was no FN field, add the FN field
        if add_name and set_name_to_org and not updatedFN:
            new_contact.append(f'FN:{first_name} {last_name}')
            #new_contact.append('\n')

        new_contact.append('END:VCARD')
        return new_contact

def write_contacts(output_file, contacts):
    with open(output_file, 'w') as f_out:
        for contact in contacts:
            f_out.write('\n'.join(contact))
            f_out.write('\n\n')


if __name__ == '__main__':
    # usage: vcf_convert.py [-h] [-n] [-p] input_file output_file
    parser = argparse.ArgumentParser(description='Modify VCF contacts to make them easier to import into Google Contacts.')
    parser.add_argument('input_file', type=str, help='Input VCF file')
    parser.add_argument('output_file', type=str, help='Output VCF file')
    parser.add_argument('-n', '--name', help='Add names to contacts that do not have them', action='store_true')
    parser.add_argument('-p', '--photo', help='Remove photos from contacts', action='store_true')

    args = parser.parse_args()
    process_vcf(args.input_file, args.output_file, args.name, args.photo)

