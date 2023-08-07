package = "cartridge"
version = "2.7.9-1"
source = {
   url = "git+https://github.com/tarantool/cartridge.git",
   tag = "2.7.9",
   branch = "master"
}
dependencies = {
   "lua >= 5.1",
   "ddl == 1.6.2-1",
   "http == 1.4.0-1",
   "checks == 3.2.0-1",
   "errors == 2.2.1-1",
   "vshard == 0.1.23-1",
   "membership == 2.4.0-1",
   "frontend-core == 8.2.1-1",
   "graphql == 0.2.0-1"
}
external_dependencies = {
   TARANTOOL = {
      header = "tarantool/module.h"
   }
}
build = {
   type = "cmake",
   copy_directories = {
      "doc"
   },
   variables = {
      TARANTOOL_DIR = "$(TARANTOOL_DIR)",
      TARANTOOL_INSTALL_BINDIR = "$(BINDIR)",
      TARANTOOL_INSTALL_LIBDIR = "$(LIBDIR)",
      TARANTOOL_INSTALL_LUADIR = "$(LUADIR)"
   }
}
