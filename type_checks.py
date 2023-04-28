import types

def isList(data): return (type(data) is types.ListType);
def isTuple(data): return (type(data) is types.TupleType);
def isDict(data): return (type(data) is types.DictType);
def isString(data): return (type(data) in [types.StringType, types.UnicodeType]);
def isInt(data): return (type(data) is types.IntType);
