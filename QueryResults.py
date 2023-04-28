import itertools, types, time
from json import loads
from ADL.Utilities import *

class QueryResults:

	def __init__(self, accessors, data):
# 		print 'QueryResults.accessors: %s' % repr(accessors)
# 		print 'QueryResults.data: %s' % repr(data)
		accessors = accessors.split(':')
		
		def do(accessors, data, ret=[], i=0):
# 			print 'do.data: %s' % repr(data)
			if len(accessors)-1 < i: accessor = '*item';
			else: accessor = accessors[i]

			cast = None
			if accessor.find('>') != -1: accessor, cast = accessor.split('>');

			acclwr = accessor.lower()
			if acclwr == '*all' or acclwr == '*item':
				if cast == 'int': fx = lambda x: int(x);
				elif cast == 'str': fx = lambda x: str(x);
				else: fx = None;
				
# 				print 'do.data: %s' % data
				if fx:
# 					print '>>>fx!'
					if isList(data): 
# 						print 'isList'
						try: data = list(map(fx, data));
						except: pass;
					elif isDict(data): 
# 						print 'isDict'
						for k in list(data.keys()):
							try: data[k] = fx(data[k]); 
							except: pass;
					else: 
# 						print 'isElse'
						try: data = fx(data);
						except: pass;

				ret.append(data)

			elif acclwr == '*each':
#  				print 'elif.each.data: %s' % repr(data)
				if isDict(data): data = list(data.values());
				for d in data: do(accessors, d, ret, i+1);

			else:
				tmp_data = None
# 				print 'else.data: %s' % repr(data)
				if isDict(data):
# 					print '>>isDict'
					if accessor in data: tmp_data = data[accessor];
					elif int(accessor) in data: tmp_data = data[int(accessor)];

				elif isList(data) or isTuple(data):
# 					print '>>isList'
					accessor = int(accessor) 
					if len(data) > accessor: tmp_data = data[accessor];

				if tmp_data is None: return;
				do(accessors, tmp_data, ret, i+1)

			if i == 0 and len(ret) > 0:
# 				if isList(ret) and len(ret) == 1: return ret[0];
				if isList(ret) and isList(ret[0]): ret = list(itertools.chain(*ret));
				if isList(ret) and len(ret) == 1: ret = ret[0];
# 				print 'QueryResults.do.returning'
				return ret;
				
		self.Items = do(accessors, data)


# results = simplejson.loads('{\
# "username": "jason@jasonwiener.com",\
# "services": {"Twitter": {"username": null, "id": null},\
# "Google": {"username": null, "id": null},\
# "Facebook": {"username": "jasonwiener", "id": "717480403"}, \
# "LinkedIn": {"username": null, "id": null}},\
# "id": "23ae18e67d60f6e732cc902c2649f6a9", \
# "created": 1313514737\
# }')
# 
# item = ['i0', 'i1', 'i2', 'i3', 'i4']
# 
# item_itemindex = [
# 	['i0.i0', 'i0.i1', 'i0.i2', 'i0.i3', 'i0.i4'],
# 	['i1.i0', 'i1.i1', 'i1.i2', 'i1.i3', 'i1.i4']
# ]
# 
# item_itemindex_deeper = [
# 	[
# 		['i0.i0.i0', 'i0.i0.i1', 'i0.i0.i2', 'i0.i0.i3', 'i0.i0.i4'],
# 		['i0.i1.i0', 'i0.i1.i1', 'i0.i1.i2', 'i0.i1.i3', 'i0.i1.i4']
# 	],
# 	[
# 		['i1.i0.i0', 'i1.i0.i1', 'i1.i0.i2', 'i1.i0.i3', 'i1.i0.i4'],
# 		['i1.i1.i0', 'i1.i1.i1', 'i1.i1.i2', 'i1.i1.i3', 'i1.i1.i4']
# 	]
# ]
# 
# object = {
# 	'key0' : ['k0.i0', 'k0.i1', 'k0.i2', 'k0.i3', 'k0.i4'],
# 	'key1' : ['k1.i0', 'k1.i1', 'k1.i2', 'k1.i3', 'k1.i4']
# }
# 
# object_itemindex = {
# 	'key0' : [
# 		['k0.i0.i0', 'k0.i0.i1', 'k0.i0.i2', 'k0.i0.i3', 'k0.i0.i4'],
# 		['k0.i1.i0', 'k0.i1.i1', 'k0.i1.i2', 'k0.i1.i3', 'k0.i1.i4']
# 	],
# 	'key1' : [
# 		['k1.i0.i0', 'k1.i0.i1', 'k1.i0.i2', 'k1.i0.i3', 'k1.i0.i4'],
# 		['k1.i1.i0', 'k1.i1.i1', 'k1.i1.i2', 'k1.i1.i3', 'k1.i1.i4']
# 	]
# }
# 
# 
# breaker = '-------------------------------------------'
# 
# query = 'services:Facebook:id>int'
# r = QueryResults('services:Facebook:id:*item>int', results).Items
# print r
# print type(r)
# print breaker
# r = QueryResults('services:Facebook:*item>int', results).Items
# print r
# print type(r)
# print breaker
# r = QueryResults('services:Facebook:id', results).Items
# print r
# print type(r)
# print breaker
# print QueryResults('services:Facebook:*all', results).Items
# print breaker
# print QueryResults('*all', item).Items
# print breaker
# print QueryResults('*Each:4', item_itemindex).Items
# print breaker
# print QueryResults('*Each:0', item_itemindex_deeper).Items
# print breaker
# print QueryResults('*each:*all', object).Items
# print breaker
# print QueryResults('*Each:*all', object_itemindex).Items
# print breaker
# print QueryResults('*Each:*Each:0', object_itemindex).Items
# print breaker
# print breaker
# print breaker
# print breaker
