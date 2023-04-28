from math import *
import operator, random
from .constants import constants
from ADL.Utilities import *
from json import loads, dumps

def _fsum(list):
	try: 
		if not isList(list): list = loads(list);
	except: pass;
	return fsum(list)

def _minmax(list, fx):
	try: 
		if not isList(list): list = loads(list);
	except: pass;
	return list[0 if fx=='min' else -1]
	

functions = {
	'constants' : constants,
	"absolute" : lambda x: fabs(x),
	"ceil" : lambda x: ceil(x),
	"factorial" : lambda x: factorial(x),
	"floor" : lambda x: floor(x),
	"fmod" : lambda x,y: fmod(x,y),
	"frexp" : lambda x: dict(list(zip(['mantissa', 'exp'], frexp(x)))),
	"fsum" : _fsum,
	"isinf" : lambda x: isinf(x),
	"isnan" : lambda x: isnan(x),
	"ldexp" : lambda x,i: ldexp(x,i),
	"modf" : lambda x: dict(list(zip(['fractional', 'integer'], modf(x)))),
	"trunc" : lambda x: trunc(x),
	"exp" : lambda x: exp(x),
	"expm1" : lambda x: expm1(x),
	"log" : lambda x, base=None: log(x, base),
	"log1p" : lambda x: log1p(x),
	"log10" : lambda x: log10(x),
	"pow" : lambda x,y: pow(x,y),
	"sqrt" : lambda x: sqrt(x),
	"acos" : lambda x: acos(x),
	"asin" : lambda x: asin(x),
	"atan" : lambda x: atan(x),
	"atan2" : lambda y,x: atan2(y,x),
	"cos" : lambda x: cos(x),
	"hypot" : lambda x,y: hypot(x,y),
	"sin" : lambda x: sin(x),
	"tan" : lambda x: tan(x),
	"degrees" : lambda x: degrees(x),
	"radians" : lambda x: radians(x),
	"max" : lambda list: _minmax(list, 'max'),
	"min" : lambda list: _minmax(list, 'min'),
	"random" : {
		"<1" : lambda: random.Random().random(),
		"int" : lambda min=None, max=None: random.Random().randint(min, max),
		"range" : lambda min, max, step=None: random.Random().randrange(min, max, step)
	},
	"round" : lambda number, digits=None: round(number, digits),
	"neg" : lambda x: operator.neg(x),
	"pos" : lambda x: operator.pos(x)
}


# print 'absolute:', functions['absolute'](-7.25)
# print 'factorial:', functions['factorial'](5)
# print 'modf:', functions['modf'](7.5)
