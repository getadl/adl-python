comparison = {
	'==' : lambda item1, item2: (item1 == item2),
	'!=' : lambda item1, item2: (item1 != item2),
	'<>' : lambda item1, item2: (item1 != item2),
	'>' : lambda item1, item2: (item1 > item2),
	'>=' : lambda item1, item2: (item1 >= item2),
	'<' : lambda item1, item2: (item1 < item2),
	'<=' : lambda item1, item2: (item1 <= item2),
	'truth' : lambda item: truth(item),
	'cmp' : lambda item1, item2: cmp(item1, item2)
}