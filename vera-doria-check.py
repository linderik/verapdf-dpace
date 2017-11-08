from oai import *
from f_filesys import *
from f_inet import *
from f_string import *
from f_xml import *
import xml.dom.minidom
import subprocess
import sys

# parsin command line arguments


# stats = dict()
result = [0, 0]
url = 'http://doria.fi/oai/request'
counter = 0


def check_pdf(pdf_file):
    # starts vera to check the pdf file. Verapdf then stores an xml file with the reults
    subprocess.call(['~/verapdf/verapdf', pdf_file, '--format', 'xml', '>', 'result.xml'])


def parse_result():
    # parses output xml from verapdf and stores error in result dictionary
    xml_file = xml.dom.minidom.parse('result.xml')
    report_tag = xml_file.getElementsByTagName('validationReports')[0]
    if report_tag.getAttribute('compliant') == '1':
        return True
    elif report_tag.getAttribute('compliant') == '0' and report_tag.getAttribute('nonCompliant') == '1':
        return False
    else:
        print('Error: XML result tag not found!')
        sys.exit(1)


def store_result(passed):
    # writes result dictionary to output.pdf
    if passed:
        result[0] = result[0] + 1
    else:
        result[1] = result[1] + 1


def write_stats():
    open('result.txt', 'w').write('Passed: ' + result[0] + '; Failed: ' + result[1])


# download all identifiers from dspace
items = oai_ListIdentifiers(url)  # The second argument is the collection or community id :-)
for orig_id, orig_ts in items.iteritems():
    counter += 1
    if counter == 5:
        break
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
                write_file(content, 'temp.pdf')
                check_pdf('temp.pdf')
                store_result(parse_result())

write_stats()