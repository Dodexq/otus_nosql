package = "ddl"
version = "1.6.2-1"
source = {
   url = "git+https://github.com/tarantool/ddl.git",
   tag = "1.6.2",
   branch = "master"
}
description = {
   summary = "Tarantool opensource DDL module",
   detailed = [[
        A ready-to-use Lua module ddl for tarantool.
        ]],
   homepage = "https://github.com/tarantool/ddl"
}
dependencies = {
   "lua >= 5.1",
   "tarantool"
}
external_dependencies = {
   TARANTOOL = {
      header = "tarantool/module.h"
   }
}
build = {
   type = "cmake",
   variables = {
      TARANTOOL_DIR = "$(TARANTOOL_DIR)",
      TARANTOOL_INSTALL_LIBDIR = "$(LIBDIR)",
      TARANTOOL_INSTALL_LUADIR = "$(LUADIR)"
   }
}
