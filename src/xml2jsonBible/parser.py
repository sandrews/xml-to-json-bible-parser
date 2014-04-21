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
    root = tree.getroot()
    
    books = {}
    ver = root.attrib["translation"]
    books.update(dict(version=ver)) 
    
    for book in tree.findall("./*/book"):
        book_name = book.attrib['name']
        print (book_name)
        if book_name not in books_metadata:
            print (book_name + " not found in books")
            return
        chapter_num = len(books_metadata[book_name])
        del books_metadata[book_name]
        
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
            for verse in list(chapter):
                verse_count += 1
                verse_number = int(verse.attrib["number"])
                if verse_number != verse_count:
                    print ("verse number error " + book.attrib['name'] + ' ' + chapter_number + ' ' + verse_number)
                    return
                verses.append(verse.text)
            chapters.append(verses)
        books.update({book_name : chapters})
        if chapter_count != chapter_num:
            print ("chapter number error " + book_name + ' chapter count is only ' + str(chapter_count))
            return
    with open(output, 'w') as f:
        json.dump(books, f, indent=2)

def generate_metadata(metadata_input_file, metadata_output_file):
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
        with open(metadata_output_file, 'w+') as f:
            json.dump(metadata_copy, f, indent = 2)
        return metadata

def main():
    """
    main function
    """
    parser = optparse.OptionParser("usage: %prog {metadata input file} {metadata output file} {input xml file} {output json file}")
    (options, args) = parser.parse_args()
    metadata = generate_metadata(args[0], args[1])
    generate_verses(metadata["verses"], args[2], args[3])
    
if "__main__" == __name__:
    main()
    
    
