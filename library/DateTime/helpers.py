from datetime import *

def interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    ret = diff.days * 24 * 60 * 60 * 1000000
    ret += diff.seconds * 1000000
    ret += diff.microseconds
    return ret

def convert(d):
    diff = d - datetime(1970,1,1,0,0, tzinfo=gmt0)
    ret = diff.days * 24 * 60 * 60 * 1000000
    ret += diff.seconds * 1000000
    ret += diff.microseconds
    return ret

def converttime(t):
	ret = t.hour * 60 * 60 * 1000000
	ret += t.minute * 60 * 1000000
	ret += t.second * 1000000
	ret += t.microsecond
	return ret


class GMT0(tzinfo):
	def utcoffset(self, dt): return timedelta(hours=0) + self.dst(dt);
	def tzname(self,dt): return "GMT +0";
	def dst(self, dt): return timedelta(0);

gmt0 = GMT0()
epoch = datetime(1970,1,1,0,0, tzinfo=gmt0)

def makedatetime(d): return epoch+timedelta(microseconds=d);

