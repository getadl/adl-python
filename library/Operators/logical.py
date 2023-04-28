def _anyall(list, fx):
	try: 
		if not isList(list): list = loads(list);
	except: pass;
	if fx == 'any': return any(list);
	return all(list)

logical = {
	'&&' : lambda item1, item2: (item1 and item2),
	'||' : lambda item1, item2: (item1 or item2),
	'!' : lambda item1: (not item),
	'any' : lambda list: _anyall(list, 'any'),
	'all' : lambda list: _anyall(list, 'all'),
}