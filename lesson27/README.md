## Домашнее задание к уроку 27

### Цели занятия
* использовать возможности Tarantool;

### Краткое содержание
* архитектура ядра Tarantool;
* Tarantool как БД и Сервер приложений;
* сравнение с другими БД;
* кейсы использования;
* установка и процесс запуска Tarantool;
* основные операции с данными.

### Задание

* Установить Tarantool Cartridge CLI
* Создать шаблон приложения командой:
* cartridge create --name myapp
* Собрать и запустить приложение:
* cartridge build
* cartridge start
* Задать любую топологию кластера в UI и сделать bootstrap

#

За основу взят гайд: https://www.tarantool.io/en/doc/latest/how-to/getting_started_cartridge/

1. Создание приложения
```
cartridge create --name myapp
```

2. Кастомизируем роль `app/roles/hello-world.lua` и добавляем ее в `./init.lua`

```
local cartridge = require('cartridge')

local function init(opts) -- luacheck: no unused args
    -- if opts.is_master then
    -- end

    local httpd = cartridge.service_get('httpd')
    httpd:route({method = 'GET', path = '/hello'}, function()
        return {body = 'Hello world!'}
    end)
    
    local log = require('log')
    log.info('Hello world!')
			
    return true
end

local function stop()
    return true
end

local function validate_config(conf_new, conf_old) -- luacheck: no unused args
    return true
end

local function apply_config(conf, opts) -- luacheck: no unused args
    -- if opts.is_master then
    -- end

    return true
end

return {
    role_name = 'hello world!',
    init = init,
    stop = stop,
    validate_config = validate_config,
    apply_config = apply_config,
    -- dependencies = {'cartridge.roles.vshard-router'},
}
```

3. Билд и старт приложения

```
cartridge build
cartridge start
```

4. На порту http://<ip_or_host>:8081/ web ui, собираем кластер

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson27/screenshots/1.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson27/screenshots/1.png" alt="" width="500" /></a>
</p>

#

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson27/screenshots/2.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson27/screenshots/2.png" alt="" width="500" /></a>
</p>

#

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson27/screenshots/3.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson27/screenshots/3.png" alt="" width="500" /></a>
</p>

#

5. Обратимся к http://<ip_or_host>:8081/hello

<p align="center"> 
<a href="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson27/screenshots/4.png" rel="some text"><img src="https://raw.githubusercontent.com/Dodexq/otus_nosql/main/lesson27/screenshots/4.png" alt="" width="500" /></a>
</p>

