server = true
bootstrap_expect = 3

bind_addr = "192.168.0.201"
client_addr = "0.0.0.0"
ui = true

performance {
  raft_multiplier = 1
}

retry_join = ["192.168.0.202", "192.168.0.203"]