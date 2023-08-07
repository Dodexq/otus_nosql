package = "membership"
version = "2.4.0-1"
source = {
   url = "git+https://github.com/tarantool/membership.git",
   tag = "2.4.0",
   branch = "master"
}
dependencies = {
   "lua >= 5.1",
   "checks ~> 3"
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
   install = {
      lua = {
         membership = "membership.lua",
         ["membership.events"] = "membership/events.lua",
         ["membership.members"] = "membership/members.lua",
         ["membership.network"] = "membership/network.lua",
         ["membership.options"] = "membership/options.lua",
         ["membership.stash"] = "membership/stash.lua"
      }
   },
   variables = {
      TARANTOOL_DIR = "$(TARANTOOL_DIR)",
      TARANTOOL_INSTALL_LIBDIR = "$(LIBDIR)",
      TARANTOOL_INSTALL_LUADIR = "$(LUADIR)"
   }
}
