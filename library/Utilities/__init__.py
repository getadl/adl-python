from json import loads, dumps
from copy import copy, deepcopy

functions = {
	'cast' : {
		'string' : lambda var:(str(var)),
		'int' : lambda var:(int(var)),
		'number' : lambda var:(float(var)),
		'json' : lambda var:(dumps(var)),
		'bool' : lambda value:(bool(value)),
		'chr' : lambda value:(chr(value)),
		'hex' : lambda value:(hex(value)),
		'hash' : lambda value:(hash(value))
	},
	"copy" : {
		"copy" : lambda value:(copy(value)),
		"deepcopy" : lambda value:(deepcopy(value))
	},
	"json" : {
		"encode" : lambda value:(dumps(value)),
		"decode" : lambda value:(loads(value))
	}
}