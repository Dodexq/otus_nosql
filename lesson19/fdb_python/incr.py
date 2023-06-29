import struct
import fdb

fdb.api_version(630)
db = fdb.open()

tr = db.create_transaction()
value_to_add = struct.pack('<i', 1)
tr.add(b'counter', value_to_add)
tr.commit().wait()