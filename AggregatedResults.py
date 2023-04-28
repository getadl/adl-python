import itertools, types

class AggregatedResults:

	Items = None

	def __init__(self, args, data):
		print('AggregatedResults(%s, %s)' % (repr(args), repr(data)), True)
		a_args = args.split(':')
		print('AggregatedResults.a_args: %s' % (repr(a_args)), True)
		
		def isList(data): return (type(data) is types.ListType);
		def isDict(data): return (type(data) is types.DictType);
		
		def do(ret, a_args, i, data):
			print 'do.i: %s' % i

			arg = a_args[i]
			cast = None
			print 'arg.find: %s' % arg.find('>')

			if arg.find('>') != -1: arg, cast = arg.split('>');

			print 'i: %s, arg: %s, cast: %s' % (i, arg, cast)

			if arg.lower() == 'all':
				if isList(data) and isList(data[0]): data = list(itertools.chain(*data));
				ret.append(data);
			elif arg.lower() == 'each': 
				print 'each -> data(%s): %s' % (i, data)
				if isDict(data): data = data.values();
				for d in data: do(ret, a_args, i+1, d);
			elif isDict(data) and data.has_key(arg): 
				print 'object -> data(%s): %s' % (i, data)
				if isDict(data[arg]):
					print '>>doing'
					do(ret, a_args, i+1, data[arg]);
				else:
					print '>>appending: %s' % data[arg]
					print '>>cast: %s' % cast
					item_data = data[arg]
					if cast == 'int': item_data = int(item_data);
					elif cast == 'str': item_data = str(item_data);
						
					if not isList(item_data): item_data = [item_data];
					ret.append(item_data);
			elif data.has_key(arg) or data.has_key(int(arg)): 
				print 'item -> %s' % data[int(arg)]
				item_data = data[int(arg)]
				if cast is 'int': item_data = int(item_data);
				elif cast is 'str': item_data = str(item_data);

				if not isList(item_data): item_data = [item_data];
				ret.append(item_data)
			else:
				return arg
				
			if i == 0 and len(ret) > 0: return list(itertools.chain(*ret));
				
		self.Items = do([], a_args, 0, data)
		if isList(self.Items) and len(self.Items) == 1: self.Items = self.Items[0];
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
# print AggregatedResults('all', item).Items
# print
# print AggregatedResults('Each:4', item_itemindex).Items
# print
# print AggregatedResults('Each:0', item_itemindex_deeper).Items
# print
# print AggregatedResults('each:all', object).Items
# print
# print AggregatedResults('Each:all', object_itemindex).Items
# print
# print AggregatedResults('Each:Each:3', object_itemindex).Items
