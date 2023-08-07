package = "graphql"
version = "0.2.0-1"
source = {
   url = "git+https://github.com/tarantool/graphql.git",
   tag = "0.2.0"
}
description = {
   summary = "GraphQL implementation for Tarantool",
   homepage = "https://github.com/tarantool/graphql",
   license = "MIT",
   maintainer = "https://github.com/tarantool"
}
dependencies = {
   "lua >= 5.1",
   "luagraphqlparser == 0.2.0-1"
}
build = {
   type = "builtin",
   modules = {
      ["graphql.execute"] = "graphql/execute.lua",
      ["graphql.init"] = "graphql/init.lua",
      ["graphql.introspection"] = "graphql/introspection.lua",
      ["graphql.parse"] = "graphql/parse.lua",
      ["graphql.query_util"] = "graphql/query_util.lua",
      ["graphql.rules"] = "graphql/rules.lua",
      ["graphql.schema"] = "graphql/schema.lua",
      ["graphql.types"] = "graphql/types.lua",
      ["graphql.util"] = "graphql/util.lua",
      ["graphql.validate"] = "graphql/validate.lua",
      ["graphql.validate_variables"] = "graphql/validate_variables.lua"
   }
}
