wget -q -O - https://packages.grafana.com/gpg.key | apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
echo "updating apt"
apt update
echo "installing grafana"
apt install -y grafana
systemctl enable grafana-server
systemctl start grafana-server
