'''
	javascript module
'''

from ADL.type_checks import *
from json import loads, dumps

def makevar(name, value, dump=True):
	if dump: value = dumps(value);
	value = value.replace('{', 'array(').replace(':', ' =>').replace('}', ')')
	value = value.replace('[', 'array(').replace(']', ')')
	return 'var %s = %s;' % (name, value)


def updatevar(name, value):
	print('updatevar:', name, value)
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
		popvar(args[a]) if a in args else 'undefined'
		for a in arg_order
	]
	for i in range(len(arg_order)-1, -1, -1):
		if populated_args[i] != 'undefined': break;
		populated_args.pop()
	return populated_args


def makeclass(obj, args, arg_order):
	print('makeclass:', obj, args, arg_order)
	return 'new %s(%s)' % (obj, ', '.join(popargs(args, arg_order)))


def makecall(obj, action, args, arg_order):
	print('makecall:', obj, action, args, arg_order)
	return '%s.%s(%s)' % (obj, action, ', '.join(popargs(args, arg_order)))


def finalize(output, variables):
	vars = ['debug(%s);' % k for k in list(variables.keys())]
	return '\n'.join([
		'<html><head>',
		'<title>Test</title>',
		'<script type="text/javascript" src="../js/common.js"></script>',
		'<script type="text/javascript">',
		'\t'+'\n\t'.join(output + vars),
		'</script>',
		'</head>',
		'<body></body>',
		'</html>'
	])