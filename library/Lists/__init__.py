import types
from json import loads, dumps
from copy import deepcopy
from collections import deque
from itertools import chain

from ADL.Utilities import *
from ADL.QueryResults import QueryResults
from functools import reduce

castlist = list

def _jsonlist(list):
	return loads(list) if not isList(list) else list[:]


def _listitem(method, list, item=None):
# 	print 'Lists._listitem.method:', method
# 	print 'Lists._listitem.list:', list
# 	print 'Lists._listitem.item:', item

# 	l = _jsonlist(list) if not isList(list) else list
	l = _jsonlist(list) #UPDATED 12052014 - think the above is redundant fx
# 	print 'Lists._listitem.l:', l
	
	fx = getattr(l, method)
# 	print 'Lists._listitem.fx:', fx

	fx_result = fx(item) if item is not None else fx()
	return l if not fx_result else fx_result


def _get(list, item):
# 	print 'Lists._get:', list, item
# 	l = _jsonlist(list) if not isList(list) else list
	l = _jsonlist(list) #UPDATED 12052014 - think the above is redundant fx
	return l[item]


def _popshift(list, method):
	return getattr(deque(_jsonlist(list)), method)()


def _splice(list, values, start, end):
	l = _jsonlist(list)
	l[start:end] = _jsonlist(values)
	return l


def _range(count=None, start=None, end=None, step=1):
	if count: 
		start = 0
		end = count
	return [i for i in range(int(start), int(end), int(step))]


def _flatten(arr):
# 	print '_flatten:', arr
# 	print '_flatten.type:', type(arr)
	def _reducefx(flat, toFlatten):
# 		print '_reducefx.flat:', flat
# 		print '_reducefx.toFlatten:', toFlatten
		# See if this index is an array that itself needs to be flattened.
		if isList(toFlatten) and list in [type(l) for l in toFlatten]:
# 			print 'call _flatten'
			return (flat if isList(flat) else [flat])+_flatten(toFlatten)
		#Otherwise just add the current index to the end of the flattened array.
		else:
# 			print 'else.flat:', flat
# 			print 'else.toFlatten:', toFlatten
			return (flat if isList(flat) else [flat])+(toFlatten if isList(toFlatten) else [toFlatten])
	ct=0
	while list in [type(l) for l in arr]:
		if ct > 10: break;
		arr = reduce(_reducefx, arr)
		ct+=1
	return arr


functions = {
	"append" : lambda list, item: _listitem('append', list, item),
	"get" : _get,
	"extend" : lambda list, item: _listitem('extend', list, _jsonlist(item)),
	"insert" : lambda list, item, index: _splice(list, item if isList(item) else [item], int(index), 0),
	"remove" : lambda list, item: _listitem('remove', list, item),
	"pop" : lambda list: _popshift(list, 'pop'),
	"index" : lambda list, value: _listitem('index', list, value),
	"count" : lambda list, value: _listitem('count', list, value),
	"sort" : lambda list: _listitem('sort', list),
	"reverse" : lambda list: _listitem('reverse', list),
	"join" : lambda list, separator: separator.join(_jsonlist(list)),
	"shift" : lambda list: _popshift(list, 'popleft'),
	"slice" : lambda list, start=None, end=None: _jsonlist(list)[start:end],
	"splice" : _splice,
	"unshift" : lambda list, values: _splice(list, values, 0, 0),
	"flatten" : lambda list: _flatten(_jsonlist(list)),
	"empty" : lambda list: [],
	"zip" : lambda lists: list(zip(*_jsonlist(lists))),
	"range" : _range,
	"contains" : lambda list, value: value in _jsonlist(list),
	"length" : lambda list: len(_jsonlist(list)),
	"sum" : lambda list: sum(_jsonlist(list)),
	"json" : lambda list: dumps(_jsonlist(list)),
	"query" : lambda list, query: QueryResults(query, list).Items,
	"clean" : lambda list: cleanList(list)
}

# print 'get:', functions['get']([1,2,3], 2)