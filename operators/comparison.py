comparison = {
	'==' : lambda vr, vl: (vr == vl),
	'!=' : lambda vr, vl: (vr != vl),
	'<>' : lambda vr, vl: (vr != vl),
	'>' : lambda vr, vl: (vr > vl),
	'>=' : lambda vr, vl: (vr >= vl),
	'<' : lambda vr, vl: (vr < vl),
	'<=' : lambda vr, vl: (vr <= vl)
}