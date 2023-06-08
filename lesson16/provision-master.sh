curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis -y
sudo cp /vagrant/etc/master/redis.conf /etc/redis
sudo systemctl restart redis-server.service
sudo cp /vagrant/etc/sentinel.conf /etc/redis/

sudo chown redis:redis /etc/redis/sentinel.conf
sudo touch /var/log/redis/sentinel.log
sudo chown redis:redis /var/log/redis/sentinel.log
sudo chmod 640 /etc/redis/sentinel.conf
sudo chmod 660 /var/log/redis/sentinel.log