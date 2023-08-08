box.cfg{
  listen = 3301,
  replication = {'replicator:password@localhost:3301',  -- URI мастера
                 'replicator:password@localhost:3302'}, -- URI реплики
  read_only = false
}
box.once("schema", function()
  box.schema.user.create('replicator', {password = 'password'})
  box.schema.user.grant('replicator', 'replication') -- настроить роль для репликации
  box.schema.space.create("test")
  box.space.test:create_index("primary")
  print('box.once executed on master')
end)

require('console').start() os.exit(0)
