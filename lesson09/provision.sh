sudo apt-get install curl gnupg2 apt-transport-https ca-certificates
sudo sh -c 'mkdir -p /usr/share/keyrings && curl -s https://builds.altinity.cloud/apt-repo/pubkey.gpg | gpg --dearmor > /usr/share/keyrings/altinity-dev-archive-keyring.gpg'
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/altinity-dev-archive-keyring.gpg] https://builds.altinity.cloud/apt-repo stable main" > /etc/apt/sources.list.d/altinity-dev.list'
sudo apt-get update