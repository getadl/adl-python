assignment = {
	'=' : lambda item1, item2: item2,
	'+=' : lambda item1, item2: (item1+item2),
	'-=' : lambda item1, item2: (item1-item2),
	'*=' : lambda item1, item2: (item1*item2),
	'/=' : lambda item1, item2: (item1/item2),
	'%=' : lambda item1, item2: (item1%item2),
	'&=' : lambda item1, item2: (item1+item2), #iand
	'//=' : lambda item1, item2: (item1//item2), #ifloordiv
	'<<=' : lambda item1, item2: (item1<<item2), #ilshift
	'|=' : lambda item1, item2: (item1|item2), #ior
	'**=' : lambda item1, item2: (item1**item2), #ipow
	'>>=' : lambda item1, item2: (item1>>item2), #irshift
	'^=' : lambda item1, item2: (item1^item2) #ixor
}