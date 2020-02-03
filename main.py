import sys
import os
import re
from time import strptime
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

if len(sys.argv) < 2:
    print('You must specify bib file')
else:
    # make list of dictionary for the data
    with open(sys.argv[1], 'r', encoding='utf8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    for dic in bib_database.entries:
        result = ['---']
        
        for key in dic:
            # delete { } \ from value
            parsed_dict = re.sub('[{}\\\\]', '', dic[key])
            if key != 'file' and key != 'ID':
                if key == 'author':
                    authors = parsed_dict.split('and')
                    result.append(f'authors: {authors}')
                elif key == 'keywords':
                    keywords = parsed_dict.split(',')
                    result.append(f'keywords: {keywords}')
                else:
                    result.append(f'{key}: "{parsed_dict}"')
        
        result.append('---')

        # make file
        if dic['ID']:
            # md file
            filename = f"content/publication/{dic['ID']}/index.md"
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(filename, 'w', encoding='utf8') as file:
                file.write('\n'.join(result))

            # bib file
            db = BibDatabase()
            db.entries = [dic]
            writer = BibTexWriter()
            with open(f"content/publication/{dic['ID']}/cite.bib", 'w', encoding='utf8') as bibfile:
                bibfile.write(writer.write(db))
        else:
            print('There is no ID')
