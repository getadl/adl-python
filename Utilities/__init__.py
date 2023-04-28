import bisect, cgi, inspect, operator, os, time, types, sys, hashlib, md5, random, datetime, re
from urlparse import urlparse, parse_qs, parse_qsl
from urllib import urlencode
import codecs
from decimal import Decimal

def isList(data): return (type(data) is types.ListType);
def isTuple(data): return (type(data) is types.TupleType);
def isDict(data): return (type(data) is types.DictType);
def isString(data): return (type(data) is types.StringType);
def isUnicode(data): return (type(data) is types.UnicodeType);
def isInt(data): return (type(data) is types.IntType);
def isFloat(data): return (type(data) is types.FloatType);
def isLong(data): return (type(data) is types.LongType);
def isNumber(data): 
	return (
		type(data) in [
			types.IntType,
			types.FloatType,
			types.LongType
		]
	)

enc = codecs.getencoder('us-ascii')
def deUnicodeText(_text, _encoding='utf-8'):
	try:
		if not isUnicode(_text) and isString(_text):
			_text = unicode(_text, _encoding)
			return enc(_text, 'xmlcharrefreplace')[0]
		elif isUnicode(_text):
			return enc(_text, 'xmlcharrefreplace')[0]
		return _text
		
	except Exception, inst:
		print 'deUnicodeText', inst



def getFile(filename, display_exceptions=True):
	try:
		if os.path.exists(filename):
			return open(filename, 'r').read()
	except Exception, inst:
		if display_exceptions:
			print 'getFile.error:', filename, inst

def putFile(filename, content, mode='w', make_if_missing=False):
	try:
		if make_if_missing:
			a_dir = filename.split('/')
			a_dir.pop()
			dir = '/'.join(a_dir)
			if not os.path.exists(dir): os.makedirs(dir);
	except Exception, inst:
		pass

	try:
		fout = open(filename, mode)
		fout.write(content)
		fout.close()
			
	except Exception, inst:
		print 'putFile.ERROR:',  filename, inst


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
			
			if(type(item) == types.UnicodeType or type(item) == types.StringType):
				item = item.strip()
			
			if(_lower == True):
				item = item.lower()
			
			if(last_item != item):
				last_item = item
				cleaned_list.append(item)
			else:
				continue
		return cleaned_list
	except Exception, inst:
		self.PrintException('Utilities.cleanList', inst)


def quickCleanList(data=None):
	if data is None or type(data) is not types.ListType: return;
	return sorted({}.fromkeys(data).keys())