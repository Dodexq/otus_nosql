package = "http"
version = "1.4.0-1"
source = {
   url = "git+https://github.com/tarantool/http.git",
   tag = "1.4.0",
   branch = "master"
}
description = {
   summary = "HTTP server for Tarantool",
   homepage = "https://github.com/tarantool/http/",
   license = "BSD"
}
dependencies = {
   "lua >= 5.1"
}
external_dependencies = {
   TARANTOOL = {
      header = "tarantool/module.h"
   }
}
build = {
   type = "builtin",
   modules = {
      ["http.codes"] = "http/codes.lua",
      ["http.lib"] = {
         incdirs = {
            "$(TARANTOOL_INCDIR)"
         },
         sources = "http/lib.c"
      },
      ["http.mime_types"] = "http/mime_types.lua",
      ["http.server"] = "http/server.lua"
   }
}
