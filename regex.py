import re
from .json import loads, dumps

def replfx(matchobj):
	print('Logic.regex.replfx.match:', matchobj.group(1))
	slashes = matchobj.group(2)
	print('Logic.regex.replfx.slashct:', len(slashes)) #the number of slashes if any
	var = matchobj.group(3)
	print('Logic.regex.replfx.variable:', var) #the variable name
	
	replaced_value = dumps(values[var])
	if replaced_value[0:1] == '"' and len(slashes):
		replaced_value = ''.join([slashes,replaced_value[0:-1],slashes,'"'])
	return replaced_value
		
# 	return matchobj.group(0)


# print adl
# print
# 
# pattern = '(\{([^"]*)\"~[^"]*\"\s*\:[^"]*\"([a-zA-Z_][a-zA-Z_0-9]*)[^"]*\"\s*\})'
# for i in range(len(adl)):
# 	for k in adl[i]:
# 		if k == 'events': continue;
# 		v = adl[i][k]
# 		print i, dumps(v)
# 		print re.findall(pattern, dumps(v))
# 	 	adl[i][k] = loads(re.sub(pattern, replfx, dumps(v)))
# 		print		
# 
# print dumps(adl)

# # 	print i, adl[i]
# 	print i, dumps(adl[i])
# 	print re.findall(pattern, dumps(adl[i]))
# # 	print re.sub(pattern, replfx, dumps(adl[i]))
# 	print
