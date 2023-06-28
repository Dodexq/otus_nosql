import fdb

fdb.api_version(630)
db = fdb.open()

key = b'test'
value = b'10'

db.set(key, value)

x = db.get(key)

print(x)