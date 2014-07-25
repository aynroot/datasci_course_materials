import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # key: table name
    # value: table record contents, starts with order_id
    tablename = record[0]
    order_id = record[1]
    mr.emit_intermediate(order_id, (tablename, record))

def reducer(order_id, tablenames_and_values):
    order_items = []
    line_items = []
    for tablename, values in tablenames_and_values:
        if tablename == 'order':
            order_items.append(values)
        elif tablename == 'line_item':
            line_items.append(values)
    for order in order_items:
        for line_item in line_items:
            mr.emit(order + line_item)

inputdata = open(sys.argv[1])
mr.execute(inputdata, mapper, reducer)
