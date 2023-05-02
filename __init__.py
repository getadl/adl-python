from ADL.type_checks import *
import ADL.exports as exports
from ADL.Utilities import *
from ADL.Console import ConsoleClass

import re
from inspect import signature
from json import loads, dumps
from copy import deepcopy

import ADL.library as library
from ADL.Populate import Populate

from ADL.Utilities import *

# this is for development only outside of the wsgi app --- start
import hashlib, datetime, random, os
from functools import reduce


def cond_if(cmp, throw=True, **kwargs):
	logicclass = kwargs['*logicclass']
	logicclass.Console.emit(logicclass.Indent, 'cond_if.cmp:', cmp)
	
	def condition(c): return _global['operators']['comparison'][c['cmp']](c['var'], c['value']);
	
	cmp_type = type(cmp)
	result = False
	isnot = False

	if cmp_type is list:
		oper = None
		logicclass.Indent += 1
		for c in cmp:
			logicclass.Console.emit(logicclass.Indent, 'cond_if.c: ', c)
			
			if 'value' in c and isString(c['value']) and c['value'].lower() == '<empty>': c['value'] = None;
			
			if c in ['not', '!']:
				isnot = True
				continue
			elif c in ['and', 'or', '&&', '||']: 
				oper = c
				continue

			if oper:
				tmp_result = condition(c)
				if oper in ['and', '&&']:
					result = result and tmp_result
				else:
					result = result or tmp_result
				oper = None
			else:
				result = condition(c)

			if isnot:
				result = result is False
				isnot = False

			logicclass.Console.emit(logicclass.Indent, 'c:', c, result)
		logicclass.Indent -= 1

	elif cmp_type is dict:
		result = condition(cmp)

	logicclass.Console.emit(logicclass.Indent, 'cond_if.result:', result)
	if not result and throw: raise Exception('if condition failed');
	return result

''' 
	loops can be:
		- counter based
		- iterator based
			- list/string
			- key, value
'''

def loops_while(**kwargs):
	logicclass = kwargs['*logicclass']
	logicclass.Indent += 1
	logicclass.Console.emit(logicclass.Indent, 'loops_while --- start')
	logicclass.Console.emit(logicclass.Indent, 'loop_while:', kwargs)
	localdata = {}
	operators_comparison = library.Operators

	logicclass_do = kwargs['*logicclass']._do
	do = kwargs['do']

	globaldata = kwargs['*logicclass'].GlobalVariables
	logicclass.Console.emit(logicclass.Indent, 'loops_while.globaldata:', globaldata)

	logicclass.Console.emit(logicclass.Indent, 'loops_while.kwargs[cond]:', kwargs['cond'])
	cond_on_init = Populate(kwargs['*logicclass'], deepcopy(kwargs['cond']), globaldata, localdata).args
	
	logicclass.Console.emit(logicclass.Indent, 'loops_while.cond_on_init:', cond_on_init)
	cond_result = cond_if(kwargs['*logicclass'], cond_on_init,throw=False)
	logicclass.Console.emit(logicclass.Indent, 'loops_while.cond_result:', cond_result)
# 	return

	i=0
	while True:
		if i > 5: break;
		logicclass.Console.emit(logicclass.Indent, 'loops_while -> doing loop', i)
			
		globaldata = kwargs['*logicclass'].GlobalVariables
		logicclass.Console.emit(logicclass.Indent, 'loops_while.globaldata:', globaldata)
		
		cond = Populate(kwargs['*logicclass'], deepcopy(kwargs['cond']), globaldata, localdata).args
		logicclass.Console.emit(logicclass.Indent, 'loops_while.cond:', cond)
		cond_result = cond_if(kwargs['*logicclass'], cond)
		
# 		print 'indent.pre:', logicclass.Indent
		logicclass.Console.emit(logicclass.Indent, 'loops_while -> doing do')
		do_data = logicclass_do(deepcopy(do), localdata)
# 		print 'indent.post:', logicclass.Indent

		logicclass.Console.emit(logicclass.Indent, 'loops_while.do_data:', do_data)
		i+=1
# 		break;	

	logicclass.Console.emit(logicclass.Indent, 'loops_while --- done')
	logicclass.Indent -= 1


def loops_items(**kwargs):
	logicclass = kwargs['*logicclass']
	logicclass.Indent += 1
	logicclass.Console.emit(logicclass.Indent, 'loops_items --- start')
	logicclass.Console.emit(logicclass.Indent, 'loops_items:', kwargs)
	localdata = {}

	items = kwargs['items']
	logicclass_do = kwargs['*logicclass']._do
	do = kwargs['do']

	logicclass.Console.emit(logicclass.Indent, 'loops_items.kwargs[items]:', kwargs['items'])
	globaldata = kwargs['*logicclass'].GlobalVariables
	items = Populate(kwargs['*logicclass'], kwargs['items'], globaldata, localdata).args
	logicclass.Console.emit(logicclass.Indent, 'loops_items.items:', items)
# 	localdata.update(init_data)
# 	print 'loop_for.localdata:', localdata

	logicclass.Console.emit(logicclass.Indent, 'do:', do)

	if isList(items):
		logicclass.Indent += 1
		logicclass.Console.emit(logicclass.Indent, 'loops_items.items -> isList')
		for item in items:
			logicclass.Indent += 1
			logicclass.Console.emit(logicclass.Indent, 'loops_items.items.isList.item:', item)

			localdata.update({'item' : item})
			try:
				logicclass_do(deepcopy(do), localdata)
			except:
				pass
			logicclass.Indent -= 1
		logicclass.Indent -= 1

	elif isDict(items):
		logicclass.Indent += 1
		logicclass.Console.emit(logicclass.Indent, 'loops_items.items -> isDict')
		for k,v in list(items.items()):
			logicclass.Indent += 1
			logicclass.Console.emit(logicclass.Indent, 'loops_items.items.isDict.k:', k)
# 			print 'k,v:', k, v
			localdata.update({'k' : k, 'v' : v})
			try:
				logicclass_do(deepcopy(do), localdata)
			except:
				pass
			logicclass.Indent -= 1
		logicclass.Indent -= 1

	logicclass.Console.emit(logicclass.Indent, 'localdata.final:', localdata)
	logicclass.Console.emit(logicclass.Indent, 'kwargs.final:', kwargs)
	logicclass.Console.emit(logicclass.Indent, 'loops_items --- end')
	logicclass.Indent -= 1


def loops_times(**kwargs):
	logicclass = kwargs['*logicclass']
	logicclass.Indent += 1
	logicclass.Console.emit(logicclass.Indent, 'loops_times --- start')
	logicclass.Console.emit(logicclass.Indent, 'loops_times:', kwargs)
	localdata = {}
	logicclass_do = kwargs['*logicclass']._do
	do = kwargs['do']
	
	for i in range(int(kwargs['times'])):
		logicclass.Indent += 1
		logicclass.Console.emit(logicclass.Indent, 'loops_times.i:', i)
		localdata.update({'i' : i})
		logicclass_do(deepcopy(do), localdata)
		logicclass.Indent -= 1

	logicclass.Console.emit(logicclass.Indent, 'localdata.final:', localdata)
	logicclass.Console.emit(logicclass.Indent, 'kwargs.final:', kwargs)
	logicclass.Console.emit(logicclass.Indent, 'loops_times --- end')
	logicclass.Indent -= 1


# def loop_for(INITIALIZATION; CONDITION; AFTERTHOUGHT):
def loops_for(**kwargs):
	logicclass = kwargs['*logicclass']
	logicclass.Indent += 1
	logicclass.Console.emit(logicclass.Indent, 'loop_for --- start')
	logicclass.Console.emit(logicclass.Indent, 'loop_for:', kwargs)
	localdata = {}
	logicclass_do = kwargs['*logicclass']._do
	do = kwargs['do']
	after = kwargs['after']
	
	logicclass.Console.emit(logicclass.Indent, 'loop_for.kwargs[init]:', kwargs['init'])
	globaldata = kwargs['*logicclass'].GlobalVariables
	init_data = Populate(kwargs['*logicclass'], kwargs['init'], globaldata, localdata).args
	logicclass.Console.emit(logicclass.Indent, 'loop_for.init_data:', init_data)
	localdata.update(init_data)
	logicclass.Console.emit(logicclass.Indent, 'loop_for.localdata:', localdata)

	logicclass.Console.emit(logicclass.Indent, 'loop_for.kwargs[cond]:', kwargs['cond'])
	cond_on_init = Populate(kwargs['*logicclass'], deepcopy(kwargs['cond']), globaldata, localdata).args
	logicclass.Console.emit(logicclass.Indent, 'loop_for.cond_on_init:', cond_on_init)
	cond_result = cond_if(kwargs['*logicclass'], cond_on_init,throw=False)
	logicclass.Console.emit(logicclass.Indent, 'loop_for.cond_result:', cond_result)

	tmp = 0
	while cond_result:
		logicclass.Indent += 1
		logicclass.Console.emit(logicclass.Indent, tmp, 'whilelooping --- start loop iteration')
		logicclass.Console.emit(logicclass.Indent, tmp, 'whilelooping >> loop_for.kwargs[cond]:', kwargs['cond'])
		cond_looping = Populate(kwargs['*logicclass'], deepcopy(kwargs['cond']), globaldata, localdata).args
		logicclass.Console.emit(logicclass.Indent, tmp, 'whilelooping >> loop_for.cond_looping:', cond_looping)
		cond_result = cond_if(kwargs['*logicclass'], cond_looping, throw=False)
		logicclass.Console.emit(logicclass.Indent, tmp, 'whilelooping >> loop_for.cond_result:', cond_result)

		if not cond_result:
			logicclass.Console.emit(logicclass.Indent+1, 'breaking')
			break;
		
		# do the do tasks -- should be a do stack too
		logicclass_do(deepcopy(do), localdata)
		
		# after is a do stack
		logicclass_do(deepcopy(after), localdata)
		
		logicclass.Console.emit(logicclass.Indent, tmp, 'whilelooping --- end loop iteration')
		tmp += 1
		logicclass.Indent -= 1
# 		if tmp == 4: break;
		
	logicclass.Console.emit(logicclass.Indent, 'localdata.final:', localdata)
	logicclass.Console.emit(logicclass.Indent, 'kwargs.final:', kwargs)
	logicclass.Console.emit(logicclass.Indent, 'loops_times --- end')
	logicclass.Indent -= 1


def printout(cmd):
	print('printout:', cmd)
# 	print dumps(cmd)


def testfx(cmd, abd, fff):
	return {'cmd_ret' : cmd, 'abd_ret' : abd, 'fff_ret' : fff}
	

class testclass(object):
	def __init__(self, arg1, arg2=None, arg3=None):
		return
	
	def test(self, **kwargs):
		print('testclass.test:', kwargs)
		return kwargs


_global = {
	'operators' : library.Operators,
	'string' : library.Strings,
	'properties' : {
		'length' : lambda item: len(item),
		'hash' : lambda item: hash(item)
	},
	'utilities' : library.Utilities,
	'list/array' : library.Lists,
	'dict/object' : library.Objects,
	'datetime' : library.DateTime,
	'crypto' : library.Crypto,
	'math' : library.Math,
	'testfx' : testfx,
	'conditionals' : {
		'if' : cond_if
	},
	'loops' : {
		'for' : loops_for,
		'items' : loops_items,
		'times' : loops_times,
		'while' : loops_while
	},
	'testclass' : testclass,
	'internet' : library.Internet
}

# this is for development only outside of the wsgi app --- end


def _parseInt(p):
	try:
		return int(p)
	except:
		return p


def _getDottedObject(obj, name, stack=False):
# 	print '_getDottedObject --- start'
# 	print '_getDottedObject:', obj, name, stack
	
	if isList(name):
		split_name = name
	else:
		split_name = name.split('.') if name.find('.') != -1 else [name]
		split_name = [_parseInt(sn) for sn in split_name]

	getobj = (lambda o,p: o[p]) if isDict(obj) else (lambda o,p: getattr(o, p))
	ret_stack = []
	for p in split_name: 
		tmpobj = getobj(obj, p)
		if stack: ret_stack.append(tmpobj);
		obj = tmpobj
	if not stack: return obj;
	return (obj, stack)


def _setDottedObject(obj, name, value):
	print('_setDottedObject --- start')
	print('_setDottedObject:', obj, name, value)

	if isList(name):
		split_name = name
	else:
		split_name = name.split('.') if name.find('.') != -1 else [name]
		split_name = [_parseInt(sn) for sn in split_name]
	
	getobj = (lambda o,p: o[p] if p in o else None) if isDict(obj) else (lambda o,p: getattr(o, p, None))

	def setobj(obj, key, value):
		obj = reduce(getobj, key[:-1], obj)
		obj[key[-1]] = value

	setobj(obj, split_name, value)

	print('_setDottedObject --- done')


def _getAction(obj, action):
# 	print '_getAction:', obj, action
	if isDict(obj): return obj[action];
	return getattr(obj, action, None)


def _getArgOrder(cmd):
	plugin = _getDottedObject(_global, cmd['target']);
	action = _getAction(plugin, cmd['action'])
	sig = signature(action)
	return list(sig.parameters.keys())


def isVariable(cmd):
	return (isDict(cmd) and 'target' not in cmd and 'action' not in cmd)


def checkDictKey(d, k, v): return (d and k in d and d[k] == v);

class LogicClass(object):
	GlobalVariables = None
	Project = None
	ReturnData = None
	Headers = None
	Indent = None
	Console = None
	Errors = None

	def __init__(self, view, args=None):
		self.GlobalVariables = args if args else {}
		self.ReturnData = None
		self.Indent = 0
		self.Errors = []
		self.Console = ConsoleClass()
		
		print('LogicClass.GlobalVariables:', self.GlobalVariables)

	def _export(self, filename, instructions, language):
		print('_export --- start')
		print()
		print('instructions:', instructions)
		print()

		self_variables = self.variables
		output = []

		lang = getattr(exports, language)
		makevar = getattr(lang, 'makevar')
		updatevar = getattr(lang, 'updatevar')
		finalize = getattr(lang, 'finalize')
		makecall = getattr(lang, 'makecall')
		makeclass = getattr(lang, 'makeclass')
		
		for cmd in instructions:
			events = cmd['events'] if 'events' in cmd else {}
			cmdid = hashlib.md5(dumps(cmd)).hexdigest()

			print('cmd(%s):' % cmdid, cmd)
			try:
				# if value is in the cmd, then this is a set variable cmd
				if 'target' not in cmd and 'action' not in cmd and isDict(cmd):
					for k,v in list(cmd.items()):
						if k == '>':
							if 'target' not in v:
								output.append(updatevar(**v))
								continue
							
							if 'action' not in v: 
								args = deepcopy(v)
								args['action'] = '__init__';
								arg_order = _getArgOrder(args)
								if arg_order[0] == 'self': arg_order = arg_order[1:];
								print('arg_order:', arg_order)
								print('args:', args)
								output.append(makevar(v['name'], makeclass(v['target'], v['args'], arg_order), False))
							else:
								arg_order = _getArgOrder(v)
								print('arg_order:', arg_order)
								print('args:', v)
								output.append(makevar(v['name'], makecall(v['target'], v['action'], v['args'], arg_order), False))
							continue

						print('k, v, v.type:', k, v, type(v))
						self_variables[k] = v
						output.append(makevar(k,v))
				else:
					arg_order = _getArgOrder(cmd)
					print('arg_order:', arg_order)
					print('args:', cmd['args'])
					output.append(makecall(cmd['target'], cmd['action'], cmd['args'], arg_order))
					
			except Exception as inst:
				print(('_export', inst))

			print()

# 		putFile('_exporttests/%s.%s' % (filename, language), finalize(output, self_variables))
		print('_export --- end')


	def _do(self, instructions, localdata=None, **kwargs):
		self.Indent += 1
		self.Console.emit(self.Indent, 'Logic._do --- start:', instructions, localdata)

		for cmd in instructions:
			self.Indent += 1
			events = cmd['events'] if 'events' in cmd else {}
			cmdid = hashlib.md5(dumps(cmd).encode('utf-8')).hexdigest()

			self.Console.emit(self.Indent, 'CMD:', cmdid, cmd);
# 			print 'cmd(%s).GlobalVariables:' % cmdid, self.GlobalVariables

			# if value is in the cmd, then this is a set variable cmd

			#if the cmd is a variable this is a setter action
			if isVariable(cmd):
				self.Indent += 1
				self.Console.emit(self.Indent, 'cmd(%s).isVariable:' % cmdid, cmd)
				variable = Populate(self, cmd, self.GlobalVariables, localdata).args
				self.Console.emit(self.Indent, 'variable:', variable)
				
				update_target = localdata if localdata is not None else self.GlobalVariables
				self.Console.emit(self.Indent, 'update_target is localdata:', update_target is localdata)
				
				is_dotted = '>' in variable
				
				if is_dotted and 'value' in variable['>']:
					self.Indent += 1
					_setDottedObject(
						update_target, 
						variable['>']['name'], 
						variable['>']['value']
					)
					self.Indent -= 1

				# this will set a var based on the response
				elif is_dotted:
					self.Indent += 1
					self.Console.emit(self.Indent, 'is_dotted')
					variable = variable['>']
					self.Console.emit(self.Indent,  'variable:', variable)
					var_name = variable['name']
					self.Console.emit(self.Indent,  'var_name:', var_name)
					del variable['name']
					self.Console.emit(self.Indent,  'variable:', variable)
					response = self._do([variable])
					self.Console.emit(self.Indent,  'calling function to set variable:', var_name)
					self.Console.emit(self.Indent,  'response:', response)
					update_target.update(dict([(var_name, response)]))
					self.Indent -= 1

				elif str(list(variable.values()).pop()).lower() != '<empty>':
					self.Indent += 1
					self.Console.emit(self.Indent,  'updating the variable...')
					update_target.update(variable)
					self.Indent -= 1

				self.Console.emit(self.Indent,  'cmd(%s).localdata:' % cmdid, localdata)

				self.Indent -= 1

# 			elif (
# 				checkDictKey(cmd, 'target', 'list/array') and
# 				cmd['action'] in ['pop']
# 			):
# 				self.Indent += 1
# 				variable = Populate(self, cmd['args'], self.GlobalVariables, localdata).args
# 				self.Console.emit(self.Indent, 'list/array.(pop).variable:', type(variable), variable)
# 				plugin = _getDottedObject(_global, cmd['target'])
# 				action = _getAction(plugin, cmd['action'])
# 
# 				try:
# 					updated_variable  = action(**variable)
# 
# 					print 'list/array.(pop).variable:', variable
# 					print 'list/array.(pop).updated_variable:', updated_variable
# 					print 'list/array.(pop).localdata:', localdata
# 					print 'list/array.(pop).GlobalVariables:', self.GlobalVariables
# 					print 'list/array.(pop).len(cmd[args]):', len(cmd['args'])
# 				
# 					target_var = cmd['args']['list']
# 					print 'list/array.(pop).target_var:', target_var
# 
# 					self.Console.emit(self.Indent, 'list/array.(pop).target_var:', target_var)
# 					update_dict = dict([(target_var['~'], updated_variable)])
# 					self.Console.emit(self.Indent, 'list/array.(pop).update_dict:', update_dict)
# 
# 					self.Indent += 1
# 					if localdata is not None and target_var['~'] in localdata:
# 						self.Console.emit(self.Indent, 'updating localdata')
# 						localdata.update(update_dict)
# 					else:
# 						self.Console.emit(self.Indent, 'updating global')
# 						self.GlobalVariables.update(update_dict)
# 					self.Indent -= 1
# 
# 					self.Console.emit(self.Indent, 'localdata:', localdata)
# 
# 					self.Console.emit(self.Indent, 'list/array.(pop)(done).localdata:', localdata)
# # 					print 'operators.(arithmetic||assignment)(done).GlobalVariables:', self.GlobalVariables
# 
# 				except Exception, inst:
# 					self.Console.emit(self.Indent, 'Exception:', inst)
# 
# 				self.Indent -= 1

			elif (
				checkDictKey(cmd, 'target', 'operators.arithmetic') or 
				checkDictKey(cmd, 'target', 'operators.assignment') or 
				(
					checkDictKey(cmd, 'target', 'list/array') and
					cmd['action'] in ['append','extend','insert','remove','sort','reverse','empty']
				)
			):
				self.Indent += 1
				variable = Populate(self, cmd['args'], self.GlobalVariables, localdata).args
				self.Console.emit(self.Indent, 'operators.(arithmetic||assignment).variable:', type(variable), variable)
				plugin = _getDottedObject(_global, cmd['target'])
				action = _getAction(plugin, cmd['action'])
				try:
					updated_variable = action(**variable)

# 					print 'operators.(arithmetic||assignment).updated_variable:', updated_variable
# 					print 'operators.(arithmetic||assignment).localdata:', localdata
# 					print 'operators.(arithmetic||assignment).GlobalVariables:', self.GlobalVariables
# 					print 'operators.(arithmetic||assignment).len(cmd[args]):', len(cmd['args'])
				
					if len(cmd['args']) == 1:
						target_var = cmd['args']['item']
					elif(checkDictKey(cmd, 'target', 'list/array')):
						target_var = cmd['args']['list']
					else:
						target_var = cmd['args']['item1']

					self.Console.emit(self.Indent, 'operators.(arithmetic||assignment).target_var:', target_var)
					update_dict = dict([(target_var['~'], updated_variable)])
					self.Console.emit(self.Indent, 'operators.(arithmetic||assignment).update_dict:', update_dict)

					self.Indent += 1
					if localdata is not None and target_var['~'] in localdata:
						self.Console.emit(self.Indent, 'updating localdata')
						localdata.update(update_dict)
					else:
						self.Console.emit(self.Indent, 'updating global')
						self.GlobalVariables.update(update_dict)
					self.Indent -= 1

					self.Console.emit(self.Indent, 'localdata:', localdata)
					self.Console.emit(self.Indent, 'operators.(arithmetic||assignment)(done).localdata:', localdata)
# 					print 'operators.(arithmetic||assignment)(done).GlobalVariables:', self.GlobalVariables

				except Exception as inst:
# 					print('_do', inst)
					self.Console.emit(self.Indent, 'Exception:', inst)
					self.Errors.append({'cmd' : dumps(cmd), 'error' : repr(inst) })

				self.Indent -= 1

			elif checkDictKey(cmd, 'target', 'internet') and cmd['action'] == 'headers':
				self.Indent += 1
			
				variable = Populate(self, cmd['args'], self.GlobalVariables, localdata).args
				self.Console.emit(self.Indent, 'internet.headers.variable:', variable)
				plugin = _getDottedObject(_global, cmd['target'])
				action = _getAction(plugin, cmd['action'])
				try:
					if not self.Headers: self.Headers = {};
					updated_variable = action(**variable)
					self.Console.emit(self.Indent, 'internet.headers.updated_variable:', updated_variable)
					self.Console.emit(self.Indent, 'internet.headers.localdata:', localdata)
# 					self.Console.emit(self.Indent, 'internet.headers.GlobalVariables:', self.GlobalVariables)
					self.Console.emit(self.Indent, 'internet.headers.len(cmd[args]):', len(cmd['args']))
					self.Headers.update(updated_variable)

				except Exception as inst:
# 					print('_do', inst)
					self.Console.emit(self.Indent, 'Exception:', inst)
					self.Errors.append({'cmd' : dumps(cmd), 'error' : repr(inst) })

				self.Indent -= 1

			elif checkDictKey(cmd, 'target', 'loops') and checkDictKey(cmd, 'action', 'for'):
				self.Indent += 1

				action = _global['loops']['for']
				self.Console.emit(self.Indent, 'cmd(%s).action(%s):' % (cmdid, cmd['action']), action)
				self.Console.emit(self.Indent, 'cmd(%s).cmd[args]:' % cmdid, cmd['args'])
				args = cmd['args']
				try:
					args['*logicclass'] = self
					results = {'data' : action(**args)}
					self.Console.emit(self.Indent, 'results:', results)
				except Exception as inst:
					self.Console.emit(self.Indent, 'Exception:', inst)
					self.Errors.append({'cmd' : dumps(cmd), 'error' : repr(inst) })
# 					print('_do', inst)

				self.Indent -= 1

			elif checkDictKey(cmd, 'target', 'return'):
				self.Indent += 1

				self.Console.emit(self.Indent, 'return --- start')
				self.Console.emit(self.Indent, 'return.cmd:', cmd)
# 				print 'return.globaldata:', self.GlobalVariables	
				self.Console.emit(self.Indent, 'return.localdata:', localdata)
				data = Populate(self, cmd, self.GlobalVariables, localdata).args

				self.ReturnData = data['data']
				self.Console.emit(self.Indent, 'return --- end')
				self.Indent -= 1
				break

			#else the cmd is a function/method call
			else:
				self.Indent += 1
				# get the plugin identified by "target"
				target = cmd['target']

				isplugin = False
				plugin = None
				self.Console.emit(self.Indent, 'cmd(%s).plugin from plugins:' % cmdid, plugin)
				
				cmdaction = cmd['action'] if 'action' in cmd else None
				if plugin:
					cmdaction = '_'.join([cmdaction, cmd['verb']])
					isplugin = True

				self.Indent += 1
				if not plugin and localdata and target in localdata:
					plugin = localdata[target]
					self.Console.emit(self.Indent, 'cmd(%s).plugin from localdata:' % cmdid, plugin)

				if not plugin and target in self.GlobalVariables:
					plugin = self.GlobalVariables[target]
					self.Console.emit(self.Indent, 'cmd(%s).plugin from globaldata:' % cmdid, plugin)
				
				# no plugin found -> try the built-in libraries
				if not plugin: 
					plugin = _getDottedObject(_global, target);
					self.Console.emit(self.Indent, 'cmd(%s).plugin from libraries:' % cmdid, plugin)
				self.Indent -= 1

				action = _getAction(plugin, cmdaction)
				self.Console.emit(self.Indent, 'cmd(%s).action(%s):' % (cmdid, cmdaction), action)
				
				if not action:
					self.Indent += 1
					self.Console.emit(self.Indent, 'init plugin', cmd['args'])
					#this is a class init call
					ret_plugin = plugin(**cmd['args'])
					self.Console.emit(self.Indent, 'plugin:', ret_plugin)
					self.Indent -= 1
					return ret_plugin
				
				# go through the args and populate the ~ args
				self.Console.emit(self.Indent, 'cmd(%s).cmd[args](b4populating):' % cmdid, cmd['args'])
				
				#populate the args
				
				# if the cmd is a loop call, include the Logic Class instance in the args
				if 'target' in cmd and cmd['target'] == 'loops': 
					args = cmd['args']
				else:
					args = Populate(self, cmd['args'], self.GlobalVariables, localdata).args

				if cmd['target'] in ['conditionals', 'loops']:
					args['*logicclass'] = self

				self.Console.emit(self.Indent, 'cmd(%s).args(populated):' % cmdid, args)
				
				try:
					self.Console.emit(self.Indent, cmd['target'],'-> action(%s).args:' % cmd['action'], args)
					results = action(**args)

					if(
						checkDictKey(cmd, 'target', 'list/array') and
						cmd['action'] in ['pop','shift']
					):
						self.Indent += 1
						self.Console.emit(self.Indent, 'list/array.pop/shift --- start')
						self.Console.emit(self.Indent+1, 'list/array.pop/shift.cmd[args][list]', cmd['args']['list'])
						
						if '~' in cmd['args']['list']:
							cmd_ps_l = cmd['args']['list']['~']
							self.Console.emit(self.Indent+1, 'list/array.pop/shift.cmd[args][list] is a variable', cmd['args']['list']['~'])
							popshift_data = None
							if localdata and cmd_ps_l in localdata:
								self.Console.emit(self.Indent+2, 'list/array.pop/shift var in localdata')
								popshift_data = localdata
							elif self.GlobalVariables and cmd_ps_l in self.GlobalVariables:
								self.Console.emit(self.Indent+2, 'list/array.pop/shift var in globaldata')
								popshift_data = self.GlobalVariables
							
							if popshift_data:
								ps_l = popshift_data[cmd_ps_l]
								popshift_data[cmd_ps_l] = ps_l[:-1] if cmd['action'] == 'pop' else ps_l[1:]

							self.Console.emit(self.Indent+1, 'list/array.pop/shift updated data', popshift_data)
						self.Console.emit(self.Indent, 'list/array.pop/shift --- end')
						self.Indent -= 1
					
					self.Console.emit(self.Indent+1, 'action(%s).results:' % cmd['action'], results)
					if not isplugin or not isDict(results) or 'dict' not in results:
						results = {'data' : results }

					self.Console.emit(self.Indent+1, 'action(%s).results:' % cmd['action'], results)
					
					if localdata and 'data' in localdata: 
						localdata['data'] = results['data']
					else:
						self.GlobalVariables['data'] = results['data']

					if 'success' in events:
						self.Indent += 1
						events_success = events['success']
						self.Console.emit(self.Indent, 'events_success', events_success)
						if not isList(events_success): events_success = [events_success];
						self.Console.emit(self.Indent, 'events_success.listed', events_success)
						self._do(events_success)
						self.Indent -= 1

				except Exception as inst:
					results = {}
					self.Console.emit(self.Indent, 'Exception:', inst)
					self.Errors.append({'cmd' : dumps(cmd), 'error' : repr(inst) })
					if 'failure' in events:
						self.Indent += 1
						events_failure = events['failure']
						self.Console.emit(self.Indent, 'events_failure', events_failure)
						if not isList(events_failure): events_failure = [events_failure];
						self._do(events_failure)
						self.Indent -= 1
					elif 'success' in events:
						self.Indent += 1
						events_success = events['success']
						self.Console.emit(self.Indent, 'events_success', events_success)
						if not isList(events_success): events_success = [events_success];
						self.Console.emit(self.Indent, 'events_success.listed', events_success)
						self._do(events_success)
						self.Indent -= 1

				self.Indent -= 1
			self.Indent -= 1

		self.Console.emit(self.Indent, '_do.ReturnData:', self.ReturnData)
		self.Console.emit(self.Indent, '_do --- end')
		
		ret = self.ReturnData if self.ReturnData is not None else self.GlobalVariables

		self.Indent -= 1

		if self.Headers:
			self.Console.emit(self.Indent, 'HEADERS:', self.Headers)
			self.Console.emit(self.Indent, 'DATA:', ret)
			
		if self.Indent == 0: 
			self.Console.emit(self.Indent, 'DATA:', ret)
		return ret


# class _makestring(_process):
# 	def __init__(self, instructions, parent): 
# 		self.value = instructions['tpl'] % instructions['val'];
# 		if instructions.has_key('var'): parent.variables[instructions['var']] = self.value;


if __name__ == '__main__':
	print('\nSTARTSTARTSTART\n----------------------------------------------\n')

	class main(LogicClass):
		def __init__(self, filename):
			LogicClass.__init__(self, 'view')
			instructions = loads(''.join(getFile('json/%s.json' % filename)))
			self.results = self._do(instructions)

# 	class export(LogicClass):
# 		def __init__(self, filename, project, language):
# 			LogicClass.__init__(self, project)
# 			instructions = loads(''.join(getFile('json/%s.json' % filename)))
# 			self.results = self._export(filename, instructions, language)

	import sys
	m = main(sys.argv[1:][0])


	print('\nm.results:', m.results)
	print('\n----------------------------------------------\nENDENDEND')
