import MapReduce
import sys


mr = MapReduce.MapReduce()

def mapper(record):
    # key: document identifier
    # value: document contents
    key, value = record
    words = value.split()
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_doc_ids):
    # key: word
    # value: list of document identifiers
    mr.emit((key, list(set(list_of_doc_ids))))

inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
