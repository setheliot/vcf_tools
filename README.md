# vcf_tools
Tools for working with VCF (vCard File Format) contacts files.

I wrote these tools after having trouble exporting the contacts from my iPhone and getting any other system (Google contact, iCloud contacts) to read them.

`vcf_convert.py` 
* This script reads in a vcf file containing multiple contacts and then writes out a new file containing all the same contacts with all of the same fields. 
* You can specify the following clean-up operations:
  * Contacts that do not have a first or last name will have the first name added with the same value as the ORG field
  * Photos will be removed from all contacts

`vcf_validator.py`
* This is intended to check he validity of a VCF file containing one or more contacts. It is currently quite limited and only validates four fields of each contact.
