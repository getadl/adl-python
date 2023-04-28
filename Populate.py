from .json import dumps
from copy import deepcopy
from .type_checks import *
from ADL.Utilities import *

class Populate(object):

	LocalData = None
	GlobalData = None
	args = None
	Indent = None
	
	def __init__(self, logicclass, args, globaldata, localdata=None):
			
		self.LocalData = localdata
		self.GlobalData = globaldata
		self.LogicClass = logicclass

		self.Indent = self.LogicClass.Indent if logicclass else 0
		
		args = deepcopy(args)
		self.Indent += 1
		self.LogicClass.Console.emit(self.Indent, 'Populate.__init__.dumps(args):', dumps(args))
		self.LogicClass.Console.emit(self.Indent, 'Populate.__init__.dumps(args).find("~"):', dumps(args).find('"~"'))
		
		self.Indent += 1
		if dumps(args).find('"~"') != -1:
			self.LogicClass.Console.emit(self.Indent, 'Populate. -> found "~"')
			self.args = self.populateDict(args) if isDict(args) else self.populateList(args)
		else:
			self.LogicClass.Console.emit(self.Indent, 'Populate. -> NOT found "~"')
			self.args = args
		self.Indent -= 1

		self.LogicClass.Console.emit(self.Indent, 'Populate.done')
		self.Indent -= 1
# 		print 'Populate.done:', self.args
			

	def getDottedObject(self, obj, name, stack=False):
		self.Indent += 1

		def _parseInt(p):
			try:
				return int(p)
			except:
				return p

		if isList(name):
			split_name = name
		else:
			split_name = name.split('.') if name.find('.') != -1 else [name]
			split_name = [_parseInt(sn) for sn in split_name]

		getobj = (lambda o,p: o[p]) if isDict(obj) else (lambda o,p: getattr(o, p))
		ret_stack = []
		for p in split_name:
			self.LogicClass.Console.emit(self.Indent, 'Populate.getDottedObject.p:', split_name, p)
			tmpobj = getobj(obj, p)
# 			print 'Populate.getDottedObject.tmpobj:', split_name, tmpobj
			if stack: ret_stack.append(tmpobj);
			obj = tmpobj
# 			print 'Populate.getDottedObject.obj:', split_name, obj
		if not stack: return obj;

		self.Indent -= 1
		return (obj, stack)


	'''
		this will take in a dict with 1 key and a key == '~'
		{ "~" : "variablename" }
		this can be a straight variable name or a .syntax name
	'''
	def populateVar(self, var):
		self.Indent += 1
		localdata = self.LocalData
		globaldata = self.GlobalData
		
		self.LogicClass.Console.emit(self.Indent, 'localdata:', localdata)
		
		self.LogicClass.Console.emit(self.Indent, 'populateVar checking localdata for', var)
		if localdata and var in localdata: 
			self.LogicClass.Console.emit(self.Indent+1, 'populateVar returning', var, 'from localdata')
			self.Indent -= 1
			return localdata[var]
		
		self.LogicClass.Console.emit(self.Indent, 'populateVar checking globaldata for', var)
		if globaldata and var in globaldata: 
			self.LogicClass.Console.emit(self.Indent+1, 'populateVar returning', var, 'from globaldata')
			self.Indent -= 1
			return globaldata[var]
		
		self.LogicClass.Console.emit(self.Indent, 'populateVar(',var,') checking getDottedObject.localdata')
		if var.find('.') != -1: 
			if localdata:
				value = self.getDottedObject(localdata, var)
				if value: 
					self.Indent -= 1
					return value;

			self.LogicClass.Console.emit(self.Indent+1, 'populateVar(',var,') checking getDottedObject.globaldata')
			value = self.getDottedObject(globaldata, var)
			if value: 
				self.Indent -= 1
				return value;
		
		self.LogicClass.Console.emit(self.Indent, 'populateVar(',var,'): None')
		self.Indent -= 1


	def populateDict(self, obj):
		self.Indent += 1
		self.LogicClass.Console.emit(self.Indent, 'populateDict:', obj)
		if len(obj) == 1 and '~' in obj:
			self.Indent -= 1
			try:
				return self.populateVar(obj['~'])
			except Exception as inst:
				print(('populateDict', inst))
				return None
# 				return obj
	
		for k in obj:
			if k == 'do': continue;
			v = obj[k]
			self.Indent += 1
			self.LogicClass.Console.emit(self.Indent, 'populateDict.k:', k)
			if isDict(v):
				obj[k] = self.populateDict(v)
			elif isList(v):
				obj[k] = self.populateList(v)
			self.Indent -= 1
		
# 		print 'populateDict.returning_obj:', obj
		self.Indent -= 1
		return obj


	def populateList(self, list):
		self.Indent += 1
		self.LogicClass.Console.emit(self.Indent, 'populateList:', list)
		for i in range(len(list)):
			item = list[i]
			self.Indent += 1
			self.LogicClass.Console.emit(self.Indent, 'populateList.item:', item)
			if isDict(item): 
				list[i] = self.populateDict(item)
			elif isList(item): 
				list[i] = self.populateList(item)
			self.Indent -= 1
			
		self.Indent -= 1
		return list


if __name__ == '__main__':

	cmd = {
		"target" : "utilities",
		"action" : "print",
		"args" : {
			"cmd" : {
				"nested2" : {
					"nested" : { "~" : "testvariable" }
				}
			},
			"cmd2" : { "~" : "var2" },
			"cmd3" : [
				"jason",
				"tanja",
				"adele",
				{ "~" : "testvariable" },
				["1", 2, { "~" : "var2" }]
			]
		}
	}
	
	data = {
		"testvariable" : "hello world",
		"var2" : "sup bitches"
	}
	
	print('cmd_data:', cmd['args'])
	
	populated = Populate(None, cmd['args'], data).args
	
	print('populated_data:', populated)
