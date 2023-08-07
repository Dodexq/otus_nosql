package = "frontend-core"
version = "8.2.1-1"
source = {
   url = "git+https://github.com/tarantool/frontend-core.git",
   tag = "8.2.1",
}
dependencies = {
   "lua >= 5.1"
}
build = {
   type = "make",
   install = {
      lua = {
         ["frontend-core"] = "frontend-core.lua"
      }
   },
   install_variables = {
      INST_LUADIR = "$(LUADIR)"
   }
}
