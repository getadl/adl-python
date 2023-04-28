import hashlib, random, datetime, os, hmac

def _unique(type, seed=None):
	lib = getattr(hashlib, type)
	return lib(
		''.join([
			str(x) for x in [
				os.getpid(),
				random.Random().randint(0,100000000),
				datetime.datetime.now(),
				seed
			]
		])
	).hexdigest()

def _hexdigest(type, string=None):
	return getattr(hashlib, type)(string).hexdigest()

functions = {
	'hmac' : {
		'hexdigest' : lambda string: hmac.new(string).hexdigest()
	},
	'md5' : {
		'unique' : lambda string: _unique('md5', string),
		'hexdigest' : lambda string: _hexdigest('md5', string)
	},
	'sha1' : {
		'unique' : lambda string: _unique('sha1', string),
		'hexdigest' : lambda string: _hexdigest('sha1', string)
	},
	'sha224' : {
		'unique' : lambda string: _unique('sha224', string),
		'hexdigest' : lambda string: _hexdigest('sha224', string)
	},
	'sha256' : {
		'unique' : lambda string: _unique('sha256', string),
		'hexdigest' : lambda string: _hexdigest('sha256', string)
	},
	'sha384' : {
		'unique' : lambda string: _unique('sha384', string),
		'hexdigest' : lambda string: _hexdigest('sha384', string)
	},
	'sha512' : {
		'unique' : lambda string: _unique('sha512', string),
		'hexdigest' : lambda string: _hexdigest('sha512', string)
	}
}
