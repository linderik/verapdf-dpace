# -*- coding: utf-8 -*-
from datetime import date
import logging
import xml.dom.minidom
from f_filesys import *
from f_inet import *
from f_xml import *

# Maximum number of resumptiontokens followed.
# Used, unless value overridden in function call
MAX_RTOKENS = 2000

# create logger
module_logger = logging.getLogger('harvest.oai')


def get_from_date_str():
    # returns a string YYYY-MM-DD a year ago

    today = date.today()
    return date(today.year - 1, today.month, today.day + 1)


def get_tokenized_url(p_baseurl, p_verb, p_parameters, p_pages, p_n, p_max_rt=MAX_RTOKENS):
    # Recursive function to loop through xml responses with resumptiontokens.
    # p_baseurl = base url of oai service
    # p_verb = oai request verb part
    # p_parameters = parameters/resumptiontoken of oai request
    # p_pages = a list of contents of fetched urls
    # p_n = recursion counter to prevent inf. loops
    # p_max_rt = p_n maximum allowed

    page = str(get_url(p_baseurl + '?verb=' + p_verb + '&' + p_parameters))

    if page:
        p_pages.append(page)

        rtoken = ""
        rtoken = xml_element_value(page, 'resumptionToken')

        print("rt: " + rtoken)

        # Fix broken resumptiontokens in some platforms.
        rtoken = rtoken.replace("ListIdentifiers|cursor", "ListIdentifiers|metadataPrefix$oai_dc|cursor")

        if len(rtoken) > 0:
            if p_n < p_max_rt:
                get_tokenized_url(p_baseurl, p_verb, 'resumptionToken=' + rtoken, p_pages, p_n + 1, p_max_rt)

    return


def get_tokenized_url_nr(p_baseurl, p_verb, count):
    # NON-Recursive function to loop through xml responses with resumptiontokens.
    # p_baseurl = base url of oai service
    # p_verb = oai request verb part
    # p_parameters = parameters/resumptiontoken of oai request
    # p_pages = a list of contents of fetched urls
    # p_n = recursion counter to prevent inf. loops
    #  = p_n maximum allowed


    pages_list = []

    page = str(get_url(p_baseurl + '?verb=' + p_verb + '&metadataPrefix=oai_dc'))

    if page:
        pages_list.append(page)

        rtoken = ""
        rtoken = xml_element_value(page, 'resumptionToken')
        print("rt: " + rtoken)

        # Fix broken resumptiontokens in some platforms.
        rtoken = rtoken.replace("ListIdentifiers|cursor", "ListIdentifiers|metadataPrefix$oai_dc|cursor")

        if len(rtoken) > 0:

            continue_list = True
            p_n = 0

            while continue_list:

                p_n = p_n + 1
                page = str(get_url(p_baseurl + '?verb=' + p_verb + '&resumptionToken=' + rtoken))

                continue_list = False

                if page:
                    pages_list.append(page)

                    rtoken = ""
                    rtoken = xml_element_value(page, 'resumptionToken')
                    print("rt: " + rtoken)
                    # print("n: " + str(p_n))

                    # Fix broken resumptiontokens in some platforms.
                    rtoken = rtoken.replace("ListIdentifiers|cursor", "ListIdentifiers|metadataPrefix$oai_dc|cursor")

                    if len(rtoken) > 0:
                        if p_n < MAX_RTOKENS:
                            continue_list = True

    return pages_list


def oai_GetRecord(p_baseurl, p_item_id, p_mdformat):
    # Gets item metadata in specified metadataformat.
    # p_baseurl = base url of oai service
    # p_item_id = item id
    # p_mdformat = metadataformat

    metadata = ""
    metadata = get_url(p_baseurl + '?verb=GetRecord&metadataPrefix=' + p_mdformat + '&identifier=' + p_item_id)

    return metadata


def oai_ListMetadataFormats(p_baseurl):
    # Gets all available metadataformsats through ListMetadataFormats query.
    # p_baseurl = base url of oai service

    formats_xml = get_url(p_baseurl + '?verb=ListMetadataFormats')

    mdformats = []
    mdformats = xml_element_values_list(formats_xml, 'metadataPrefix')

    return mdformats


# --

def oai_ListIdentifiers(p_baseurl):
    # Gets all ID/timestamp pairs through ListIdentifiers queries.
    # p_baseurl = base url of oai service

    req_verb = 'ListIdentifiers'
    req_params = 'metadataPrefix=oai_dc'

    pages = []
    # get_tokenized_url(p_baseurl, req_verb, req_params, pages, 1)
    pages = get_tokenized_url_nr(p_baseurl, req_verb)

    id_list = []
    ds_list = []
    for page in pages:

        dom = xml.dom.minidom.parseString(page)
        for hnode in dom.getElementsByTagName('header'):
            id_list.append(hnode.getElementsByTagName('identifier')[0].childNodes[0].nodeValue)
            ds_list.append(hnode.getElementsByTagName('datestamp')[0].childNodes[0].nodeValue)

    items = {}
    items = dict(zip(id_list, ds_list))

    return items
