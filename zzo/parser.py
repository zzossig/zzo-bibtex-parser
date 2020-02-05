#!/usr/bin/env python3

import sys
import os
import re
import datetime
import argparse
from time import strptime
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


def main():
    parse(sys.argv[1:])

def parse(args):
    parser = argparse.ArgumentParser(description='zzo-bibtex-parser')
    parser.add_argument('--path', required=True, help='bib file path')
    args = parser.parse_args()

    if args.path == None:
        print('You must specify bib file path')
    else:
        # make list of dictionary for the data
        with open(args.path, 'r', encoding='utf8') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)

        for dic in bib_database.entries:
            year = '0000'
            month = '01'
            day = '01'
            entry_type = 'misc'
            result = ['---']

            for key in dic:
                # delete { } \ from value
                parsed_dict = re.sub('[{}\\\\]', '', dic[key])
                if key != 'file' and key != 'ID' and key != 'urldate' and key != 'language':
                    if key == 'author':
                        authors = parsed_dict.split('and')
                        result.append(f'authors: {authors}')
                    elif key == 'keywords':
                        keywords = parsed_dict.split(',')
                        result.append(f'keywords: {keywords}')
                    elif key == 'url':
                        result.append(f'link: "{parsed_dict}"')
                    elif key == 'journal':
                        result.append(f'publication: "{parsed_dict}"')
                    elif key == 'year':
                        year = parsed_dict
                    elif key == 'month':
                        month = month_string_to_number(parsed_dict)
                    elif key == 'day':
                        day = parsed_dict
                    elif key == 'ENTRYTYPE':
                        doubleQuoteEscape = parsed_dict.replace('"', '\\"')
                        result.append(f'{key}: "{doubleQuoteEscape}"')
                        entry_type = doubleQuoteEscape
                    else:
                        doubleQuoteEscape = parsed_dict.replace('"', '\\"')
                        result.append(f'{key}: "{doubleQuoteEscape}"')

            result.append(f'publishDate: "{year}-{month}-{day}"')
            result.append('---')

            # make file
            if dic['ID']:
                # md file
                renamedDir = re.sub(r'(?<!^)(?=[A-Z])', '_', dic['ID']).lower()
                filename = f"content/publication/{entry_type}/{renamedDir}/index.md"
                listfilename = f"content/publication/{entry_type}/_index.md"
                dirname = os.path.dirname(filename)
                listdirname = os.path.dirname(listfilename)

                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                with open(filename, 'w', encoding='utf8') as file:
                    file.write('\n'.join(result))

                if not os.path.exists(listdirname):
                    os.makedirs(listdirname)
                with open(listfilename, 'w', encoding='utf8') as listfile:
                    listdata = [
                        '---',
                        f'title: {entry_type}',
                        f'date: {datetime.datetime.now()}',
                        f'description: Publication - {entry_type}',
                        '---'
                    ]
                    listfile.write('\n'.join(listdata))


                # bib file
                db = BibDatabase()
                db.entries = [dic]
                writer = BibTexWriter()
                with open(f"content/publication/{entry_type}/{renamedDir}/cite.bib", 'w', encoding='utf8') as bibfile:
                    bibfile.write(writer.write(db))
            else:
                print('There is no ID')


def month_string_to_number(string):
    m = {
        'jan': "01",
        'feb': "02",
        'mar': "03",
        'apr': "04",
        'may': "05",
        'jun': "06",
        'jul': "07",
        'aug': "08",
        'sep': "09",
        'oct': "10",
        'nov': "11",
        'dec': "12"
    }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

if __name__ == "__main__":
    main()
