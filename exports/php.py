'''
	php module
'''

from ADL.type_checks import *
from json import loads, dumps

def makevar(name, value, dump=True):
	if dump: 
		value = dumps(value);
		value = value.replace('{', 'array(').replace(':', ' =>').replace('}', ')')
		value = value.replace('[', 'array(').replace(']', ')')
	return '$%s = %s;' % (name, value)


def updatevar(name, value):
	print 'updatevar:', name, value
	if isString(name): return makevar(name, value);

	var = []
	for n in name:
		if not len(var):
			var.append(n)
		else:
			var.append('[%s]' % dumps(n))
	return makevar(''.join(var), value)


def popvar(v):
	if isDict(v) and '~' in v: return v['~'];
	return v


def popargs(args, arg_order):
	populated_args = [
		popvar(args[a]) if a in args else 'null'
		for a in arg_order
	]
	for i in range(len(arg_order)-1, -1, -1):
		if populated_args[i] != 'null': break;
		populated_args.pop()
	return populated_args


def makeclass(obj, args, arg_order):
	print 'makeclass:', obj, args, arg_order
	return 'new %s(%s)' % (obj, ', '.join(popargs(args, arg_order)))


def makecall(obj, action, args, arg_order):
	print 'makecall:', obj, action, args, arg_order
	return '%s::%s(%s)' % (obj, action, ', '.join(popargs(args, arg_order)))


def finalize(output, variables):
	vars = ['Common::Dump($%s);' % k for k in variables.keys()]
	
	return '\n'.join([
		'<?php',
		'\t'+'\n\t'.join(['require "../ADL.php";'] + output + vars),
		'?>'
	])	
# 	return '<?php\n\t'+'\n\t'.join(['require "../ADL.php";'] + output + vars)+'\n?>'	