Vagrant.configure("2") do |config|

  (1..3).each do |i|
    config.vm.define "consul#{i}" do |server|
      server.vbguest.auto_update = false if Vagrant.has_plugin?('vagrant-vbguest')
      server.vm.box = "geerlingguy/ubuntu2004"
      server.vm.hostname = "consul#{i}"
      server.vm.network "public_network", ip: "192.168.0.20#{i}", bridge: "wlo1"
      server.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.name = "consul#{i}"
        vb.cpus = "2"
      end
      server.vm.provision "shell", inline: <<-SHELL
      sudo mkdir /root/.ssh
      sudo cp /vagrant/provision/authorized_keys /root/.ssh
      SHELL
    end
  end

  (1..3).each do |i|
    config.vm.define "nginx#{i}" do |server|
      server.vbguest.auto_update = false if Vagrant.has_plugin?('vagrant-vbguest')
      server.vm.box = "geerlingguy/ubuntu2004"
      server.vm.hostname = "nginx#{i}"
      server.vm.network "public_network", ip: "192.168.0.21#{i}", bridge: "wlo1"
      server.vm.provider "virtualbox" do |vb|
        vb.memory = "1024"
        vb.name = "nginx#{i}"
        vb.cpus = "1"
      end
      server.vm.provision "shell", inline: <<-SHELL
      sudo mkdir /root/.ssh
      sudo cp /vagrant/provision/authorized_keys /root/.ssh
      SHELL
    end
  end
end