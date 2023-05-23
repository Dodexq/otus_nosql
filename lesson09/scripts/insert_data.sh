for i in *; do
    if [ "${i:0:4}" = "taxi" ];then
        echo "Вставляем данные из файла  $i"
        cat $i | clickhouse-client --password=passwd --query 'INSERT INTO taxi.taxi_trips FORMAT CSVWithNames'
    fi
done
