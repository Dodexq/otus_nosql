import redis
import time

def test_string_time(r):

    # Создание pipeline
    pipe = r.pipeline()

    # Генерация и передача данных string 
    print("Генерация string ~20мб...")
    for i in range(300000):
        key = f'my_string:{i}'
        value = f'value{i}'
        pipe.set(key, value)

    # Выполнение pipe на запись и подсчет времени
    start_time = time.time()
    pipe.execute()
    end_time = time.time()
    write_time_string = end_time - start_time
    print(f'Время записи string: {write_time_string:.3f} секунд')

    # Чтение данных
    start_time = time.time()
    my_string = r.keys('my_string:*')
    end_time = time.time()
    read_time_string = end_time - start_time
    print(f'Время чтения string: {read_time_string:.3f} секунд')
    print("3 строки", my_string[:3], "\n##########")

def test_hset_time(r):

    # Создание pipeline
    pipe = r.pipeline()

    # Генерация и передача данных для HSET
    print("Генерация hset ~20мб...")
    for i in range(200000):
        key = f'my_hset'
        field = f'field{i}'
        value = f'value{i}'
        pipe.hset(key, field, value)

    # Выполнение pipe на запись и подсчет времени
    start_time = time.time()
    pipe.execute()
    end_time = time.time()
    write_time_hset = end_time - start_time
    print(f'Время записи hset: {write_time_hset:.3f} секунд')

    # Чтение данных
    start_time = time.time()
    my_datata = dict(r.hgetall("my_hset"))
    end_time = time.time()
    read_time_hset = end_time - start_time
    print(f'Время чтения hset: {read_time_hset:.3f} секунд')
    print("3 пары ключ:значение", list(my_datata.items())[:3], "\n##########")

def test_zset_time(r):

    # Создание pipeline
    pipe = r.pipeline()

    # Генерация и передача данных для ZSET
    print("Генерация zset ~20мб...")
    for i in range(180000):
        key = f'my_zset'
        member = f'field{i}'
        score = i
        pipe.zadd(key, {member: score})

    # Выполнение pipe на запись и подсчет времени
    start_time = time.time()
    pipe.execute()
    end_time = time.time()
    write_time_zset = end_time - start_time
    print(f'Время записи hset: {write_time_zset:.3f} секунд')

    # Чтение данных
    key_zset = 'my_zset'
    start_time = time.time()
    data_zset = r.zrange(key_zset, 0, -1, withscores=True)
    end_time = time.time()
    read_time_zset = end_time - start_time
    print(f'Время чтения zset: {read_time_zset:.3f} секунд')
    print("3 пары ключ:score", data_zset[:3], "\n##########")

def test_list_time(r):
    
    # Создание pipeline
    pipe = r.pipeline()
    
    print("Генерация list ~20мб...")
    # Генерация и передача данных для List
    for i in range(1500000):
        key = f'my_list'
        value = f'value{i}'
        pipe.rpush(key, value)

    # Выполнение pipe на запись и подсчет времени
    start_time = time.time()
    pipe.execute()
    end_time = time.time()
    write_time_list = end_time - start_time
    print(f'Время записи list: {write_time_list:.3f} секунд')

    # Чтение данных
    key_list = 'my_list'
    start_time = time.time()
    data_list = r.lrange(key_list, 0, -1)
    end_time = time.time()
    read_time_list = end_time - start_time
    print(f'Время чтения list: {read_time_list:.3f} секунд')
    print("3 элемента list", data_list[:3], "\n##########")

def main():
    # Подключение к Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    # Выполнение функций записи чтения для 4 типов данных
    test_string_time(r)
    test_hset_time(r)
    test_zset_time(r)
    test_list_time(r)
    
    r.close()

main()
