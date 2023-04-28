from json import dumps
from ADL.library.DateTime import functions as dt

class ConsoleClass(object):

	def __init__(self, triple=None):
		self.Indent = 0
		self.Stack = []


	def _pkgarg(self, arg):
		try:
			return dumps(arg)
		except:
			return repr(arg)


	def emit(self, indent, *args):
		i_indent = indent-1
		s_indent = str(i_indent)+('\t'*i_indent if indent else '')

		pkgarg = self._pkgarg
		data = ' '.join([pkgarg(a) for a in args])

		print(s_indent + data)

		pkg = {
			'timestamp' : dt['datetime']['strftime'](dt['datetime']['now'](), "%H:%M:%S.%f"),
			'indent' : i_indent,
			'data' : data 
		}
		self.Stack.append(pkg)