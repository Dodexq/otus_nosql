## Теоретическое занятие 23

### Цели занятия
* конфигурировать rabbitMQ кластер

### Краткое содержание
* протокол AMPQ;
* задача и функциональность брокера сообщений;
* особенности кластера rabbitMQ;
* запуск кластера;
* проверка отказоустойчивости.

#

Развернуть оба инстанса с провижином (уже установлен rabbit на 2 вм) `vagrant up`

`(1..2).each do |i|` 2 машины и переменная `i`

`server.vbguest.auto_update = false if Vagrant.has_plugin?('vagrant-vbguest')` - отключает обновление (перекомпиляцию) vbguest vbox, если в vagrant установлен плагин `vagrant-vbguest`

`server.vm.network "public_network", ip: "192.168.0.15#{i}", bridge: "wlo1"` - ip машин, по дефолту мост с линком `wlo1`

#

* Добавление пользователей

```
sudo rabbitmqctl list_users

sudo rabbitmqctl add_user test Passwd321$

sudo rabbitmqctl set_user_tags test administrator

sudo rabbitmqctl set_permissions -p / test ".*" ".*" ".*"
```

* Включить веб интерфейс `sudo rabbitmq-plugins enable rabbitmq_management` доступен на порту `<hostname>:15672`


### Кластеризация

* Информация о кластере `sudo rabbitmqctl cluster_status`

* Посмотреть "печеньку" (должна быть одинакова на всех инстансах кластера) `sudo cat /var/lib/rabbitmq/.erlang.cookie`

* Менять cookie только на остановленном инстансе rabbit `sudo rabbitmqctl stop_app`

* Джойн в кластер `sudo rabbitmqctl join_cluster rabbit@<hostname>`

* Включение зеркалирования очередей 
```
sudo rabbitmqctl set_policy ha-all ".*" '{"ha-mode":"all","ha-sync-mode":"automatic"}'
```