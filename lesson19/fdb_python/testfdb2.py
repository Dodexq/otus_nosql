import fdb

fdb.api_version(630)
db = fdb.open()

tuple0 = ('my_array', '0')
tuple1 = ('my_array', '1')
tuple9 = ('my_array', '9')

packed0 = fdb.tuple.pack(tuple0)
packed1 = fdb.tuple.pack(tuple1)
packed9 = fdb.tuple.pack(tuple9)

db.set(packed0, b'15')
db.set(packed1, b'20')
db.set(packed9, b'25')

@fdb.transactional
def load_array(tr):
    range_tuple = fdb.tuple.range(('my_array',))
    return [(fdb.tuple.unpack(k), v) for k, v in tr[range_tuple]]

result = load_array(db)
print(result)