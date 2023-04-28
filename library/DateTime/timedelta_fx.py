from datetime import timedelta

functions = {
	"min" : lambda: timedelta.min,
	"max" : lambda: timedelta.max,
	"timedelta" : lambda days=None, seconds=None, microseconds=None, milliseconds=None, minutes=None, hours=None, weeks=None: timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks),
	"seconds" : lambda timedelta: timedelta.total_seconds()
}