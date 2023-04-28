import types, urllib.request, urllib.parse, urllib.error
from json import loads, dumps
from copy import deepcopy
from ADL.Utilities import *

from ADL.QueryResults import QueryResults

def _jsonobj(obj):
	return loads(obj) if not isDict(obj) else deepcopy(obj)


def _update(obj, update):
	o = _jsonobj(obj)
	o.update(_jsonobj(update))
	return o


def _contains(obj, item, type='key'):
	o = _jsonobj(obj)
	if type == 'key': return item in o;
	return item in sorted(o.values())


def _addgetremove(obj, fx, key, value=None):
	o = _jsonobj(obj)
	if fx == 'add': 
		o[key] = value
	elif fx == 'remove':
		del o[key] 
	elif fx == 'empty':
		return {}
	elif fx == 'get':
		return o[key] if key in o else None
	return o

functions = {
	"has_key" : lambda obj, key: key in obj,
	"update" : _update,
	"keys" : lambda obj: list(obj.keys()),
	"values" : lambda obj: list(obj.values()),
	"contains" : _contains,
	"querystring" : lambda obj: urllib.parse.urlencode(dict([(k, str(v).encode('utf-8')) for k, v in list(_jsonobj(obj).items()) if v is not None])),
	"length" : lambda obj: len(obj),
	"add" : lambda obj, key, value: _addgetremove(obj, 'add', key, value),
	"remove" : lambda obj, key: _addgetremove(obj, 'remove', key),
	"get" : lambda obj, key: _addgetremove(obj, 'get', key),
	"empty" : lambda obj: _addgetremove(obj, 'empty'),
	"json" : lambda obj: dumps(_jsonobj(obj)),
	"query" : lambda obj, query: QueryResults(query, obj).Items
}