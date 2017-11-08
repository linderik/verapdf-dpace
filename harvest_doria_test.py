#made by merioksa

import logging
import time
from oai import *
from f_filesys import *
from f_inet import *
from f_string import *
from f_xml import *
import xml.dom.minidom

URL_OAIBASE = 'http://www.doria.fi/oai/request'
#URL_OAIBASE = URL_OAIBASE.strip('\'"')
#change!!!
#DIR = 'C:\HY-Data\LINDERIK\doria_harvest_testi\temp\\'
#DIR_LOGFILE = 'C:\HY-Data\LINDERIK\doria_harvest_testi\\temp\log\\'
DIR = 'C:/HY-Data/LINDERIK/doria_harvest_testi/temp'
DIR_LOGFILE = 'C:/HY-Data/LINDERIK/doria_harvest_testi/temp/log/'

def main():
	#url = "http://varia32-kk.lib.helsinki.fi/oai/request?verb=ListRecords&metadataPrefix=kk"
	#page = str(get_url(url))
	
	items = oai_ListIdentifiers(URL_OAIBASE)
	print len(items)
	
	#iteritem?
	items_got = 0
	for item_id, item_ts in items.iteritems():
		md = oai_GetRecord(URL_OAIBASE, item_id, 'kk')
		
		dom = xml.dom.minidom.parseString(md)
		
		item_id = dom.getElementsByTagName('identifier')[0].firstChild.nodeValue
		handle = str_after_last(item_id, ':')
		
		elems = dom.getElementsByTagName('kk:file')
		
		if len(elems) > 0:
			elem = elems[0]
			#print elem.getAttribute('bundle')
			link = elem.getAttribute('href')
			filename = str_after_last(link, '/')
			filename = str_before_last(filename, '?')

			#print link
			
			content = get_url(link)
			
						
			if (content != None):
				item_dir = DIR + '/' + id_to_pathname(item_id)
				#item_dir = DIR+id_to_pathname(item_id)
				#item_dir = os.path.join(DIR,item_id)
				ready_dir(item_dir)
				
				#write_file(md, item_dir + '\' + 'metadata_kk.xml')
				file_name = item_dir+'/'+'metadata_kk.xml'
				write_file(md, file_name)
				#write_file(md,item_dir+"metadata_kk.xml")
				
				#filename = str_after_last(link, "/")
				#filename = str_before_last(filename, "?")
				write_file(content, item_dir + '/' + filename)
				#write_file(content, os.path.join(item_dir,filename))
			
		items_got += 1
		if items_got > 10:
			break
		
	


if __name__ == '__main__':
	logger = logging.getLogger('harvest')
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler(DIR_LOGFILE + 'logging.log')
	fh.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	logger.addHandler(fh)
	logger.info('*** STARTING ***')
	logger.info('Project: ' + 'TESTING')
	
	main()
