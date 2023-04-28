arithmetic = {
	'+' : lambda vr, vl: (vr+vl),
	'-' : lambda vr, vl: (vr-vl),
	'*' : lambda vr, vl: (vr*vl),
	'/' : lambda vr, vl: (vr/vl),
	'%' : lambda vr, vl: (vr%vl),
	'++' : lambda vr: (vr+1),
	'--' : lambda vr: (vr-1)
}