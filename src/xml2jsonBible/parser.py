'''
Created on Apr 11, 2014

@author: lcabancla
'''
import xml.etree.ElementTree as ET
import optparse
import json
import copy


def generate_verses(books_metadata, xml, output):
    """
    convert xml to json
    original XML schema:
    bible translation
        -> testament
            -> book
                -> chapter
                    -> verse
    """
    tree = ET.parse(xml)    
    books = []
    
    # for each book
    for book in tree.findall("./*/book"):
        book_name = book.attrib['name']
        print (book_name)
        if book_name not in books_metadata:
            print (book_name + " not found in books")
            return
        chapter_num = len(books_metadata[book_name])
        del books_metadata[book_name]
        
        # for each chapter
        chapters = []
        chapter_count = 0
        for chapter in list(book):
            chapter_count += 1
            chapter_number = int(chapter.attrib['number'])
            if chapter_number != chapter_count:
                print ("chapter number error " + book.attrib['name'] + ' ' + chapter_number)
                return
            verses = []
            verse_count = 0
            
            # for each verse
            for verse in list(chapter):
                verse_count += 1
                verse_number = int(verse.attrib["number"])
                if verse_number != verse_count:
                    print ("verse number error " + book.attrib['name'] + ' ' + chapter_number + ' ' + verse_number)
                    return
                # append to verse list
                verses.append(verse.text)
            # append to chapter list
            chapters.append(verses)
        # append to book list
        books.append(chapters)
        
        # error checking
        if chapter_count != chapter_num:
            print ("chapter number error " + book_name + ' chapter count is only ' + str(chapter_count))
            return

    # write to file
    with open(output, 'w') as f:
        json.dump(books, f, indent=2)

def generate_metadata(metadata_input_file):
    """
    open the metadata file for reading
    """
    with open(metadata_input_file) as json_data:
        metadata = json.load(json_data)
        metadata_copy = copy.copy(metadata)
        verse_list = []
        book_map= metadata_copy["verses"]
        for book in metadata_copy["names"]:
            verse_list.append(book_map[book[0]])
        metadata_copy.update(dict(verses = verse_list))
        with open('processed_' + metadata_input_file, 'w+') as f:
            json.dump(metadata_copy, f, indent = 2)
        return metadata

def main():
    """
    main function
    """
    parser = optparse.OptionParser("usage: %prog {metadata input file}")
    (options, args) = parser.parse_args()
    metadata = generate_metadata(args[0])
    for version in metadata['versions']:
        generate_verses(metadata["verses"], version + '.xml', version + '.json')
    
if "__main__" == __name__:
    main()
    
    
