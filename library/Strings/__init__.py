import string as _string
from json import loads, dumps
from .constants import constants
from ADL.Utilities import *
import re, urllib.request, urllib.parse, urllib.error

def _format(template, data):
	try: data = loads(data);
	except: pass;
	if isList(data): return template.format(*data);
	elif isDict(data): return template.format(**data);
	return template.format(data)

def _translate(word, input=None, output=None, deletecharacters=None):
	table = None
	if input and output: table = _string.maketrans(input, output);
	return _string.translate(word, table, deletecharacters)

functions = {
	'constants' : constants,
	"format" : _format,
	"capitalize" : lambda word: _string.capitalize(word),
	"find" : lambda word, fragment, start=None, end=None: _string.find(word, fragment, start, end),
	"count" : lambda word, fragment, start=None, end=None: _string.count(word, fragment, start, end),
	"lower" : lambda word: _string.lower(word),
	"split" : lambda word, separator, max=None: _string.split(word, separator, max),
	"join" : lambda words, separator: _string.join(words, separator),
	"strip" : lambda word, characters=None: _string.strip(word, characters),
	"lstrip" : lambda word, characters=None: _string.lstrip(word, characters),
	"rstrip" : lambda word, characters=None: _string.rstrip(word, characters),
	"translate" : _translate,
	"upper" : lambda word: _string.upper(word),
	"ljust" : lambda word, width=None, character=None: _string.ljust(word, width, character),
	"rjust" : lambda word, width=None, character=None: _string.rjust(word, width, character),
	"cjust" : lambda word, width=None, character=None: _string.center(word, width, character),
	"replace" : lambda word, old, new, max=None: _string.replace(word, old, new, max),
	"startswith" : lambda word, fragment, start=None, end=None: word.startswith(fragment, start, end),
	"endswith" :  lambda word, fragment, start=None, end=None: word.endswith(fragment, start, end),
	"length" : lambda word: len(word),
	"escape" : lambda word: urllib.parse.quote(word, ''),
	"unescape" : lambda word: urllib.parse.unquote(word),
	"deunicode" : lambda string: deUnicodeText(string)
}
# 
# regex = {
# # 	"search" : lambda pattern, string, flags=0: re.search(pattern, string, flags).groupdict(),
# # 	"match" : {},
# # 	"split" : {},
# # 	"findall" : {},
# # 	"sub" : {}
# }
