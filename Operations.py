import types
from simplejson import loads
from ADL.Utilities import *
from GraphFM.Classes.Graph.IntersectClassRC import IntersectClass
from GraphFM.Classes.Graph.ExclusionClassRC import ExclusionClass

class Operations(object):

# 	def _handlelists(self, lists):
# 		if type(lists) is types.StringType: node_ids = simplejson.loads(lists);
# 		if type(lists) is not types.ListType: raise Exception('lists must be ListType');
# 		if type(lists[0]) is not types.ListType: raise Exception('lists items must be of ListType');
# 		return lists


	def _handlelists(self, list):
		if type(list) is types.StringType: list = loads(list);
		if type(list) is not types.ListType: raise Exception('list must be ListType');
		return quickCleanList(list)


	def intersect(self, list1, list2):
		list1, list2 = map(self._handlelists, (list1, list2))
		return IntersectClass(list1+list2, 2).Items


	def exclude(self, list1, list2):
		list1, list2 = map(self._handlelists, (list1, list2))
		return ExclusionClass(list1, list2).Items


	def join(self, list1, list2, clean=True):
		list1, list2 = map(self._handlelists, (list1, list2))
		ret = list1+list2
		return quickCleanList(ret) if clean else ret


# p = Operations()
# 
# list1 = [1,2,3,4,5,6,7,8]
# list2 = [3,4,5]
# 
# print p.intersect(list1, list2)
# print p.exclude(list1, list2)