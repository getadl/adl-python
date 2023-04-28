from datetime import date
from datetime import datetime as _datetime
from .helpers import convert, gmt0, makedatetime, converttime

def _replace(datetime, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None):
	args = {}
	if year: args['year'] = year;
	if month: args['month'] = month;
	if day: args['day'] = day;
	if hour: args['hour'] = hour;
	if minute: args['minute'] = minute;
	if second: args['second'] = seconds;
	if microsecond: args['microsecond'] = microsecond;
	return convert(makedatetime(datetime).replace(**args))

def _new(year, month, day, hour=None, minute=None, second=None, microsecond=None):
	args = {
		'year' : year,
		'month' : month,
		'day' : day,
		'tzinfo' : gmt0
	}
	if hour: args['hour'] = hour;
	if minute: args['minute'] = minute;
	if second: args['second'] = second;
	if microsecond: args['microsecond'] = microsecond;
	return convert(_datetime(**args))
	
def _isoformat(date): return makedatetime(date).isoformat();

functions = {
	"new" : _new,
	"today" : lambda: convert(_datetime.now(gmt0).replace(hour=0,minute=0,second=0,microsecond=0)),
	"now" : lambda: convert(_datetime.now(gmt0)),
	"fromordinal" : lambda ordinal: convert(_datetime.fromordinal(ordinal).replace(tzinfo=gmt0)),
	"year" : lambda date: makedatetime(date).year,
	"month" : lambda date: makedatetime(date).month,
	"day" : lambda date: makedatetime(date).day,
	"hour" : lambda date: makedatetime(date).hour,
	"minute" : lambda date: makedatetime(date).minute,
	"second" : lambda date: makedatetime(date).second,
	"microsecond" : lambda date: makedatetime(date).microsecond,
	"date" : lambda date: convert(makedatetime(date).replace(hour=0,minute=0,second=0,microsecond=0)),
	"time" : lambda date: converttime(makedatetime(date).time()),
	"replace" : _replace,
	"toordinal" : lambda date: makedatetime(date).toordinal(),
	"weekday" : lambda date: makedatetime(date).weekday(), 			#add string outputting here
	"isoweekday" : lambda date: makedatetime(date).isoweekday(),	#add string outputting here
	"isocalendar" : lambda date: dict(list(zip(['year', 'week', 'weekday'], makedatetime(date).isocalendar()))),
	"readable" : _isoformat,
	"isoformat" : _isoformat,
	"strptime" : lambda string, format: convert(_datetime.strptime(string, format).replace(tzinfo=gmt0)),
	"strftime" : lambda date, format: makedatetime(date).strftime(format)
}


if __name__ == '__main__':
	print('\nunit tests ---- start\n----------------------------------------------')
	import types
	print('datetime.new', functions['new'](2014, 11, 10, 12, 15, 23, 550000))
# 	print 'datetime.new', functions['new'](1, 1, 2)/1000000
	print('datetime.today', functions['today']())
	print('datetime.fromordinal', functions['fromordinal'](735613))
	print('datetime.isoformat', functions['isoformat'](functions['fromordinal'](735613)))
	print('datetime.time', functions['time'](1421325296123456))
	print('datetime.isocalendar', functions['isocalendar'](1421280000000000))
	print('datetime.strptime', functions['strptime']("21/11/06 16:30", "%d/%m/%y %H:%M"))
	print('datetime.readable', functions['readable'](functions['strptime']("21/11/06 16:30", "%d/%m/%y %H:%M")))
	print('datetime.strftime', functions['strftime'](1164126600000000, "%d/%m/%y %H:%M"))
	print('datetime.replace', functions['replace'](1415577600000000, 1973, 2, 7))
# 	# print functions['toordinal'](0)
# 	print functions['new'](2015, 1, 15)
