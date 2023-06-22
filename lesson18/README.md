## Домашнее задание к уроку 17 и 18

* Разворачиваем кластер Consul любым способом. Проверяем отказоустойчивость
* Разворачиваем кластер Etcd любым способом. Проверяем отказоустойчивость

### Consul
1. Написаны роли Ansible для автоматической генерации TLS (если директория `./ansible/certs` отсутствует) и инсталяции Сервера + Агента + Сервиса nginx к Consul
```
cd ./ansible
ansible-playbook -i inventories/dev/hosts main.yml
```
2. Развернут Кластер Consul Server (3 ноды) + Agent (3 ноды), подключение TLS, деплой сервиса Nginx. 

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson18/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson18/screenshots/1.png" alt="" width="500" /></a>
</p>

#

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson18/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson18/screenshots/2.png" alt="" width="500" /></a>
</p>

#

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson18/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson18/screenshots/3.png" alt="" width="500" /></a>
</p>

3. Убиваем мастера, смотрим, что мастер перевыбрался

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson18/screenshots/4.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson18/screenshots/4.png" alt="" width="500" /></a>
</p>

### Etcd
* Синтаксис добавления ноды в кластер (на slave) в конфиг `/etc/default/etcd`

```
ETCD_NAME="$(hostname)"
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379"
ETCD_ADVERTISE_CLIENT_URLS="http://$(hostname):2379"
ETCD_LISTEN_PEER_URLS="http://0.0.0.0:2380"
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://$(hostname):2380"
ETCD_INITIAL_CLUSTER_TOKEN="PatroniCluster"
ETCD_INITIAL_CLUSTER="etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380"
ETCD_INITIAL_CLUSTER_STATE="new"
ETCD_DATA_DIR="/var/lib/etcd"
```

* `etcdctl cluster-health`

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson17/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson17/screenshots/1.png" alt="" width="500" /></a>
</p>

* Обращение к api v3 etcdctl `export ETCDCTL_API=3`

* Добавляем 4 ноду в кластер `etcdctl member add etcd4 --peer-urls=http://etcd4:2380`
```
7c39e817a80a80b2, started, etcd4, http://etcd4:2380, http://etcd4:2379
9a1f33941721f94d, started, etcd1, http://etcd1:2380, http://etcd1:2379
9df0146dd9068bd2, started, etcd3, http://etcd3:2380, http://etcd3:2379
f2aeb69aaf7ffcbf, started, etcd2, http://etcd2:2380, http://etcd2:2379
```

* Сделать снапшот `etcdctl snapshot save /var/tmp/etcd.backup`
* Восстановить снапшот 
```
etcdctl snapshot restore /var/tmp/etcd.backup \
  --name etcd2 \
  --initial-cluster etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380 \
  --initial-cluster-token PatroniCluster \
  --initial-advertise-peer-urls http://etcd2:2380
```