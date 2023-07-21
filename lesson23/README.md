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