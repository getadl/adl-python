import bisect, cgi, inspect, operator, os, time, types, sys, hashlib, md5, random, datetime, re
from urllib.parse import urlparse, parse_qs, parse_qsl
from urllib.parse import urlencode
import codecs
from decimal import Decimal

def isList(data): return (type(data) is list);
def isTuple(data): return (type(data) is tuple);
def isDict(data): return (type(data) is dict);
def isString(data): return (type(data) is bytes);
def isUnicode(data): return (type(data) is str);
def isInt(data): return (type(data) is int);
def isFloat(data): return (type(data) is float);
def isLong(data): return (type(data) is int);
def isNumber(data): 
	return (
		type(data) in [
			int,
			float,
			int
		]
	)

enc = codecs.getencoder('us-ascii')
def deUnicodeText(_text, _encoding='utf-8'):
	try:
		if not isUnicode(_text) and isString(_text):
			_text = str(_text, _encoding)
			return enc(_text, 'xmlcharrefreplace')[0]
		elif isUnicode(_text):
			return enc(_text, 'xmlcharrefreplace')[0]
		return _text
		
	except Exception as inst:
		print('deUnicodeText', inst)



def getFile(filename, display_exceptions=True):
	try:
		if os.path.exists(filename):
			return open(filename, 'r').read()
	except Exception as inst:
		if display_exceptions:
			print('getFile.error:', filename, inst)

def putFile(filename, content, mode='w', make_if_missing=False):
	try:
		if make_if_missing:
			a_dir = filename.split('/')
			a_dir.pop()
			dir = '/'.join(a_dir)
			if not os.path.exists(dir): os.makedirs(dir);
	except Exception as inst:
		pass

	try:
		fout = open(filename, mode)
		fout.write(content)
		fout.close()
			
	except Exception as inst:
		print('putFile.ERROR:',  filename, inst)


def cleanList(_list, _do_sort=True, _lower=False):
	try:
		if(_list == None):
			return
		
		if(_do_sort == True):
# 				_list = quick_sort(_list)
			_list.sort()
		
		cleaned_list = []
		last_item = ''
		for item in _list:
			
			if(type(item) == str or type(item) == bytes):
				item = item.strip()
			
			if(_lower == True):
				item = item.lower()
			
			if(last_item != item):
				last_item = item
				cleaned_list.append(item)
			else:
				continue
		return cleaned_list
	except Exception as inst:
		self.PrintException('Utilities.cleanList', inst)


def quickCleanList(data=None):
	if data is None or type(data) is not list: return;
	return sorted({}.fromkeys(data).keys())