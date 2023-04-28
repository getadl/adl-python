import datetime, time
from json import JSONEncoder

class JSONDateTimeEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, time.struct_time):
			return convert(datetime.datetime(*obj[:6]))
		if isinstance(obj, (datetime.date, datetime.datetime)): 
			return obj.isoformat();
		return JSONEncoder.default(self, obj)
