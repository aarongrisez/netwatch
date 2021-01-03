import subprocess
import os
import time

MAX_RETRIES = 5
INFLUX_DB_HOST = os.environ.get("NETWATCH_INFLUX_DB_HOST")
INFLUX_DB_ADMIN_USER = os.environ.get("NETWATCH_INFLUX_DB_ADMIN_USER")
INFLUX_DB_ADMIN_PASS = os.environ.get("NETWATCH_INFLUX_DB_ADMIN_PASS")
INFLUX_DB_USER = os.environ.get("NETWATCH_INFLUX_DB_USER")
INFLUX_DB_PASS = os.environ.get("NETWATCH_INFLUX_DB_PASS")

cmds = [
    ['pip', 'install', '-r', 'requirements.txt'],
    ['bash', './scripts/init.sh'],
    ['bash', './scripts/install_influx.sh'],
    ['bash', './scripts/install_grafana.sh'],
]

for cmd in cmds:
    subprocess.run(cmd)

from influxdb import InfluxDBClient

i = 0
while i < MAX_RETRIES:
    try:
        client = InfluxDBClient(
            host='localhost',
            port=8086,
            username=INFLUX_DB_ADMIN_USER,
            password=INFLUX_DB_ADMIN_PASS
        )
        client.create_database("internet_speed")
        break
    except Exception as e:
        print(f"Connection failed, retrying in {i ** 2 + 1} seconds")
        time.sleep(i ** 2 + 1)
        i += 1

client.create_user(
    INFLUX_DB_USER,
    INFLUX_DB_PASS,
    admin=False
)
client.grant_privilage("all", "internet_speed", INFLUX_DB_USER)


