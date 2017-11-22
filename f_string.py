# -*- coding: utf-8 -*-
import logging
import re
import time
import unicodedata
import urllib
import os

# create logger
module_logger = logging.getLogger('harvest.string')


def htc(m):
    # used by urldecode
    return chr(int(m.group(1), 16))


def id_to_pathname(p_str):
    # Converts an ID string to a suitable dir name.
    # Currently just converts some characters to underscores.
    # p_str = ID string

    normalized = p_str.replace(':', '_')
    normalized = normalized.replace('/', '_')
    normalized = normalized.replace(' ', '_')

    return normalized


def id_to_pathname_long(p_str):
    # Converts an ID string to a suitable dir name.
    # Currently just converts some characters to underscores.
    # p_str = ID string

    normalized = p_str.replace(':', '_')
    normalized = normalized.replace('/', '_')
    normalized = normalized.replace(' ', '_')
    normalized = normalized[-1:] + '/' + normalized

    return normalized


def l_remove_containing(p_list, p_str):
    # Returns list of strings that don't contain a specified substring.
    # p_list = original list
    # p_str = substring

    result = []

    for tstr in p_list:
        if (tstr.count(p_str) > 0):
            pass
        else:
            result.append(tstr)

    return result


def l_remove_endswith(p_list, p_str):
    # Returns list of strings, that don't end with specified string.
    # p_list = original list
    # p_str = string to check

    result = []

    for tstr in p_list:
        if (tstr.endswith(p_str)):
            pass
        else:
            result.append(tstr)

    return result


def l_remove_not_containing(p_list, p_str):
    # Returns list of strings that contain a specified substring.
    # p_list = original list
    # p_str = substring

    result = []

    for tstr in p_list:
        if (tstr.count(p_str) > 0):
            result.append(tstr)

    return result


def l_remove_startswith(p_list, p_str):
    # Returns list of strings, that don't start with specified string.
    # p_list = original list
    # p_str = string to check

    result = []

    for tstr in p_list:
        if (tstr.startswith(p_str)):
            pass
        else:
            result.append(tstr)

    return result


def l_str_before_last(p_list, p_delimiter):
    # Returns list of pathnames, truncated at a specified delimiter.
    # p_list = a list of paths
    # p_delimiter = string is split at the first occurence of this character

    result = []

    for tstr in p_list:
        if (tstr.count(p_delimiter) > 0):
            res, dummy = tstr.split(p_delimiter, 1)
        else:
            res = tstr

        result.append(res)

    return result


def list2str(p_list):
    # Converts list to comma separated string.
    # p_list = list to convert

    result = ""

    if (len(p_list) > 0):

        c = 1
        for tstr in p_list:

            result = result + tstr
            if c < len(p_list):
                result = result + ", "
            c = c + 1

    return result


def parse_timestring(p_str):
    # Converts strings to time.
    # p_str = Time as "YYYY-MM-DDThh:mm:ss" or "YYYY-MM-DD"

    t = None

    try:
        t = time.strptime(p_str[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError, e:
        try:
            t = time.strptime(p_str[:10], "%Y-%m-%d")
        except ValueError, e:
            t = None

    return t


def str_after_last(p_str, p_delimiter):
    # Get substring after delimiter. If delimiter is not found, return whole string.
    # p_str = original string
    # p_delimiter = delimiter string

    result = p_str

    if p_str.count(p_delimiter):
        dummy, result = p_str.rsplit(p_delimiter, 1)

    return result


def str_before_last(p_str, p_delimiter):
    # Get substring before delimiter. If delimiter is not found, return whole string.
    # p_str = original string
    # p_delimiter = delimiter string

    result = p_str

    if p_str.count(p_delimiter):
        result, dummy = p_str.rsplit(p_delimiter, 1)

    return result


def str2url(p_str):
    # URLencode a string
    # p_str = string to encode

    result = ""
    result = urllib.url2pathname(p_str)

    return result


def url2filename(p_url):
    # URLencoding + UTF-strangeness turned to a neat filename.

    result = ""

    result = str_after_last(p_url, "/")
    result = str_before_last(result, "?")

    try:
        result = urldecode(result)
    except UnicodeDecodeError, e:
        result = str2url(result)
        result = unicodedata.normalize('NFC', result).encode('utf-8')

    try:
        result = result.decode("utf-8", "ignore")
    except UnicodeEncodeError, e:
        # result = str2url(result)
        result = unicodedata.normalize('NFC', result).encode('utf-8')
        # result = result.decode("iso-8859-1", "ignore")
        result = result.decode("utf-8", "ignore")

        print result

    result = id_to_pathname(result)

    return result


def urldecode(url):
    # found from internets..

    rex = re.compile('%([0-9a-hA-H][0-9a-hA-H])', re.M)
    return rex.sub(htc, url)
