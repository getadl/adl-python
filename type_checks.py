import types

def isList(data): return (type(data) is list);
def isTuple(data): return (type(data) is tuple);
def isDict(data): return (type(data) is dict);
def isString(data): return (type(data) in [bytes, str]);
def isInt(data): return (type(data) is int);
