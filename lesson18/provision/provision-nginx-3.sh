wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update 
sudo apt install consul -y

sudo apt update
sudo apt install nginx -y

sudo mkdir -p /etc/consul.d/certs
sudo cp /vagrant/vm_deploy/etc/certs/* /etc/consul.d/certs
sudo cp /vagrant/vm_deploy/etc/nginx3/* /etc/consul.d/
sudo chown --recursive consul:consul /etc/consul.d
sudo chmod 640 /etc/consul.d/client.hcl

sudo systemctl enable consul
sudo systemctl start consul