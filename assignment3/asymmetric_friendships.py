import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    person, friend = record
    mr.emit_intermediate('\t'.join(sorted([person, friend])), (person, friend))

def reducer(person, friendships_list):
    # if a particular friendship is mutual,
    # we will see two records in a list
    if len(friendships_list) == 1:
        p1, p2 = friendships_list[0]
        mr.emit((p1, p2))
        mr.emit((p2, p1))

inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
