wget -qO- https://repos.influxdata.com/influxdb.key | apt-key add -
echo "deb https://repos.influxdata.com/debian buster stable" | tee /etc/apt/sources.list.d/influxdb.list
echo "updating apt"
apt update
echo "installing influxdb"
apt install -y influxdb
systemctl unmask influxdb
systemctl enable influxdb
systemctl start influxdb