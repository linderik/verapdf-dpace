# -*- coding: utf-8 -*-
import logging
from lxml import etree
import xml.dom.minidom


# create logger
module_logger = logging.getLogger('harvest.xml')


def xml_element_value(p_xml, p_element):
	# Return contents of the first occurence of a specified element in XML.
	# p_xml = XML to search
	# p_element = element name to search for
	
	result = ""

	if p_xml:
		dom = xml.dom.minidom.parseString(p_xml)
		if len(dom.getElementsByTagName(p_element))>0:
			if len(dom.getElementsByTagName(p_element)[0].childNodes) > 0:
				result = str(dom.getElementsByTagName(p_element)[0].childNodes[0].nodeValue)

	return result


def xml_element_values_list(p_xml, p_element):
	# Return contents of specified elements as list.
	# p_xml = XML to search
	# p_element = element name to search for
	
	result = []

	if p_xml:
		dom = xml.dom.minidom.parseString(p_xml)
		for node in dom.getElementsByTagName(p_element):
			result.append(node.childNodes[0].nodeValue)

	return result


def is_link(p_str):
	# Checks if given string is link. Currenly pretty simple...
	# -contains no spaces (multiple links in xml declarations)

	result = False
	
	if p_str:
		if p_str.startswith('http://') or p_str.startswith('https://') or p_str.startswith('ftp://'):
			result = True
			
			"""
			# XML declarations contain multiple links separated by spaces.
			# Also, URLs should not contain spaces anyway.
			if p_str.count(' ') > 0: 
				result = False
			"""
			
	return result


def xml_find_links_rec(p_nodelist, p_llist):
	# Recursively walk througn XML elements and attributes, gathering links.
	# p_nodelist = current list of childnodes
	# p_llist = list of found links
	
	for subnode in p_nodelist:
		if (subnode.nodeType == subnode.ELEMENT_NODE):

			attrs = subnode.attributes
			for attrName in attrs.keys():
				attrNode = attrs.get(attrName)
				
				if is_link(attrNode.nodeValue):
					p_llist.append(attrNode.nodeValue)
			
			if len(subnode.childNodes)>0:
				if is_link(subnode.childNodes[0].nodeValue):
					p_llist.append(subnode.childNodes[0].nodeValue)

			xml_find_links_rec(subnode.childNodes, p_llist)
	return


def xml_find_links(p_metadata):
	# Find all links within XML document
	# p_metadata = XML document
	
	links = []
	xml_doc = xml.dom.minidom.parseString(p_metadata)
	xml_find_links_rec(xml_doc.childNodes, links)

	return links

	
def xsl_transform(p_xml, p_xslf):
	# p_xml: source xml string
	# p_xslf: path to xsl file
	# Returns transform result as string

	result = None
	
	try:
		xml_tree = etree.fromstring(p_xml)

		xsl_file = open(p_xslf, 'r')
		xsl_str = xsl_file.read()
		xsl_file.close()
		xsl_tree = etree.fromstring(xsl_str)

		xsl_transf = etree.XSLT(xsl_tree)
		result_tree = xsl_transf.apply(xml_tree)
		result = etree.tostring(result_tree, pretty_print=True, encoding="utf-8", xml_declaration=True)

		if (result == None):
			module_logger.warn('Empty XSLT result. (' + p_xslf + ')')
			
	except etree.XMLSyntaxError, e:
		# sometimes xml contains ampersands and shit...
		module_logger.error('XMLError: ' + str(e))
		
	return result

