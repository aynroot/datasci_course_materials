import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    person, friend = record
    mr.emit_intermediate(person, friend)

def reducer(person, friends):
    friends_cnt = len(set(friends))
    mr.emit((person, friends_cnt))

inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
