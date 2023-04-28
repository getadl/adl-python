bitwise = {
	'|' : lambda item1, item2: item1 | item2,
	'^' : lambda item1, item2: item1 ^ item2,
	'&' : lambda item1, item2: item1 & item2,
	'<<' : lambda item1, item2: item1 << item2,
	'>>' : lambda item1, item2: item1 >> item2,
	'~' : lambda item: ~item
	# 	x | y	bitwise or of x and y	 
	# 	x ^ y	bitwise exclusive or of x and y	 
	# 	x & y	bitwise and of x and y (aka xor)
	# 	x << n	x shifted left by n bits	(1)(2)
	# 	x >> n	x shifted right by n bits	(1)(3)
	# 	~x	the bits of x inverted	
}