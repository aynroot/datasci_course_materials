import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    seq_id, nucleotides = record
    mr.emit_intermediate('', nucleotides[:-10])

def reducer(dummy_key, nucleotides_list):
    for nucleotides in set(nucleotides_list):
        mr.emit(nucleotides)

inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
