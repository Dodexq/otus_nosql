wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt-get install -y mongodb-org
sudo cp /vagrant/mongodb-keyfile /home/vagrant
sudo chown mongodb:mongodb /home/vagrant/mongodb-keyfile
sudo chmod 400 /home/vagrant/mongodb-keyfile
sudo cp /vagrant/etc/mongod-a.conf /etc/mongod.conf
sudo systemctl restart mongod.service