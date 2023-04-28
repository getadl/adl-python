from datetime import timedelta
from datetime import time as _time
from helpers import converttime, gmt0, makedatetime

def _replace(time, hour=None, minute=None, second=None, microsecond=None):
	args = {}
	if hour: args['hour'] = hour;
	if minute: args['minute'] = minute;
	if second: args['second'] = seconds;
	if microsecond: args['microsecond'] = microsecond;
	return converttime(makedatetime(time).time().replace(**args))

def _new(hour=None, minute=None, second=None, microsecond=None):
	args = { 'tzinfo' : gmt0 }
	if hour: args['hour'] = hour;
	if minute: args['minute'] = minute;
	if second: args['second'] = second;
	if microsecond: args['microsecond'] = microsecond;
	return converttime(_time(**args))

functions = {
	"min" : lambda: converttime(_time.min),
	"max" : lambda: converttime(_time.max),
	"new" : _new,
	"hour" : lambda time: makedatetime(time).time().hour,
	"minute" : lambda time: makedatetime(time).time().minute,
	"second" : lambda time: makedatetime(time).time().second,
	"microsecond" : lambda time: makedatetime(time).time().microsecond,
	"replace" : _replace,
	"isoformat" : lambda time: makedatetime(time).time().isoformat(),
	"strftime" : lambda time, format: makedatetime(time).time().strftime(format)
}

if __name__ == '__main__':
	print '\nunit tests ---- start\n----------------------------------------------'
	print 'min:', functions['min']()
	print 'max:', functions['max']()
	print 'new:', functions['new'](12, 34, 56, 123456)

	print 'hour:', functions['hour'](45296123456)
	print 'minute:', functions['minute'](45296123456)
	print 'second:', functions['second'](45296123456)
	print 'microsecond:', functions['microsecond'](45296123456)
	print 'strftime:', functions['strftime'](45296123456, "%H:%M:%S")


	print 'isoformat:', functions['isoformat'](functions['new'](12, 34, 56, 123456))
	print '----------------------------------------------\nunit tests ---- end'
