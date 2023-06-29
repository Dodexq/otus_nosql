import fdb

fdb.api_version(630)
db = fdb.open()

## fdbcli - set counter1 10, set counter2 20, set counter3 30
keys = [b'counter1', b'counter2', b'counter3']

@fdb.transactional
def watch_keys(tr):
    return [tr.watch(k) for k in keys]

while True:
    k = fdb.Future.wait_for_any(*watch_keys(db))
    print('Изменился ключ: ', str(keys[k]))