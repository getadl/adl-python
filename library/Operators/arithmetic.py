from operator import floordiv, pow

arithmetic = {
	'+' : lambda item1, item2: (item1+item2),
	'-' : lambda item1, item2: (item1-item2),
	'*' : lambda item1, item2: (item1*item2),
	'/' : lambda item1, item2: (item1/item2),
	'%' : lambda item1, item2: (item1%item2),
	'++' : lambda item: (item+1),
	'--' : lambda item: (item-1),
	'//' : lambda item1, item2: floordiv(item1, item2),
	'**' : lambda item1, item2: pow(item1,item2)
}