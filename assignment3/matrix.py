import MapReduce
import sys

mr = MapReduce.MapReduce()
A_DIM = 5
B_DIM = 5

def mapper(record):
    # we assume to know dimensions of both matrices
    name, row, col, value = record
    if name == "a":
        for i in xrange(B_DIM):
            mr.emit_intermediate((row, i), (name, col, value))
    elif name == 'b':
        for i in xrange(A_DIM):
            mr.emit_intermediate((i, col), (name, row, value))

def reducer(key, values):
    a_dict = dict([(i, value) for name, i, value in values if name == 'a'])
    b_dict = dict([(i, value) for name, i, value in values if name == 'b'])
    result = 0
    for i in xrange(A_DIM):
        result += a_dict.get(i, 0) * b_dict.get(i, 0)
    mr.emit((key[0], key[1], result))

inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
