import logging
import time
from oai import *
from f_filesys import *
from f_inet import *
from f_string import *
from f_xml import *
import xml.dom.minidom
import lxml.etree as et
import subprocess

stats = dict()
result = None
url = 'http://doria.fi/oai/request'


def get_identifiers():
    # download all identifiers from dspace
    items = oai_ListIdentifiers(url)  # The second argument is the collection or community id :-)
    for orig_id, orig_ts in items.iteritems():
        kk = oai_GetRecord(url, orig_id, 'kk')
        dom_kk = xml.dom.minidom.parseString(kk)

        # Check the metadata. If it's empty, it means the item is probably deleted from the dspace instance
        fields = dom_kk.getElementsByTagName('kk:field')
        if len(fields) == 0:
            print("No metadata found, item (probably) deleted" + orig_id)
            continue

        elems = dom_kk.getElementsByTagName('kk:file')

        # Check that we have some files. If not, log error
        if len(elems) > 0:
            # Fetch the actual files (pdfs etc)

            filename_list = []
            for elem in elems:
                link = elem.getAttribute('href')
                filename = str_after_last(link, '/')
                filename = str_before_last(filename, '?')
                filename_list.append(filename)

                content = get_url(str2url(link))

                if content is None:
                    # Something went wrong, abort!!
                    print("Could not download all files" + orig_id)
                    break  # Do not handle this item anymore
                else:
                    write_file(content, '/temp.pdf')


def get_pdf():
    # downloads pdf file and stores to current folder as temp.pdf
    pass


def check_pdf():
    # starts vera to check the pdf file. Verapdf then stores an xml file with the reults
    return result


def parse_result():
    # parses output xml from verapdf and stores error in result dictionary
    pass


def store_result():
    # writes result dictionary to output.pdf
    return stats


def write_stats():
    return


get_pdf()
check_pdf()
write_stats(store_result(parse_result()))

