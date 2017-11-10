# -*- coding: utf-8 -*-
import httplib
import logging
import socket
import time
import unicodedata
import urllib2

# Waiting time between http requests.
WAIT_SECS = 0

# create logger
module_logger = logging.getLogger('harvest.inet')


def be_nice():
	# Sleep.
	# p_secs = Seconds to sleep
	
	time.sleep(WAIT_SECS)
	
	return


def get_url(p_url):
	# Tries to fetch URL.
	# p_url = URL to get
	# p_wait = Time to wait after request.

	socket.setdefaulttimeout(300)
	
	headers = { 'User-Agent' : 'Mozilla/5.0' }

	url = p_url
	try:
		url = url.decode("utf-8", "strict")
		#print('success')
	except UnicodeEncodeError, e:
		url = unicodedata.normalize('NFC', url).encode('utf-8')
		#print('fail')
	request = urllib2.Request(url, None, headers)
	data = None

	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError, e:
		module_logger.error('HTTPError: ' + str(e) + ' URL: ' + p_url)
	except urllib2.URLError, e:
		module_logger.error('URLError: ' + str(e) + ' URL: ' + p_url)
	except httplib.BadStatusLine, e:
		module_logger.error('BadStatusLine: ' + str(e) + ' URL: ' + p_url)
	except UnicodeDecodeError, e:
		module_logger.error('UnicodeDecodeError: ' + str(e) + ' URL: ' + p_url)
	else:
		# check for redirects to login, dont mind about ADDITION OF some querystring
		rd_check = response.geturl()
		#if (((url == rd_check) or (rd_check2 in url)) and (rd_check.count("login") == 0)):

		if (rd_check.count("login") == 0):
			data = response.read()
		else:
			module_logger.info('Login detected: ' + rd_check + ' URL: ' + p_url)
		
	be_nice()

	return data
	
	


