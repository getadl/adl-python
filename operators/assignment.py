def equal(vars, vr, vl): 
	if '~' in vr: 
		vars[vr['~']] = vars[vl['~']] if '~' in vl else vl
	else:
		vr = vars[vl['~']] if '~' in vl else vl


def plusequal(vars, vr, vl):
	if '~' in vr: 
		vars[vr['~']] += vars[vl['~']] if '~' in vl else vl
	else:
		vr += vars[vl['~']] if '~' in vl else vl


def minusequal(vars, vr, vl):
	if '~' in vr: 
		vars[vr['~']] -= vars[vl['~']] if '~' in vl else vl
	else:
		vr -= vars[vl['~']] if '~' in vl else vl


def timesequal(vars, vr, vl): 
	if '~' in vr: 
		vars[vr['~']] *= vars[vl['~']] if '~' in vl else vl
	else:
		vr *= vars[vl['~']] if '~' in vl else vl


def divideequal(vars, vr, vl):
	if '~' in vr: 
		vars[vr['~']] /= vars[vl['~']] if '~' in vl else vl
	else:
		vr /= vars[vl['~']] if '~' in vl else vl


def percentequal(vars, vr, vl):
	if '~' in vr: 
		vars[vr['~']] %= vars[vl['~']] if '~' in vl else vl
	else:
		vr %= vars[vl['~']] if '~' in vl else vl


assignment = {
	'=' : equal,
	'+=' : plusequal,
	'-=' : minusequal,
	'*=' : timesequal,
	'/=' : divideequal,
	'%=' : percentequal
}