import types
from .arithmetic import arithmetic
from .assignment import assignment
from .comparison import comparison
from .bitwise import bitwise
from .logical import logical

functions = {
	'arithmetic' : arithmetic,
	'assignment' : assignment,
	'comparison' : comparison,
	'bitwise' : bitwise,
	'logical' : logical,
	'typeof' : lambda item: type(item)
}