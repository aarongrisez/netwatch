import os
import schedule
import time
import re
import subprocess
import socket
import shutil
import psutil
from influxdb import InfluxDBClient

INFLUX_DB_HOST = os.environ.get("NETWATCH_INFLUX_DB_HOST")
INFLUX_DB_PASS = os.environ.get("NETWATCH_INFLUX_DB_PASS")

client = InfluxDBClient(INFLUX_DB_HOST, 8086, 'speedmonitor', INFLUX_DB_PASS, 'internetspeed')

def record_speed():
    response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
    download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
    upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

    ping = ping[0].replace(',', '.')
    download = download[0].replace(',', '.')
    upload = upload[0].replace(',', '.')

    speed_data = [
        {
            "measurement" : "internet_speed",
            "tags": {
                "host": socket.gethostname()
            },
            "fields" : {
                "download": float(download),
                "upload": float(upload),
                "ping": float(ping)
            }
        }
    ]
    client.write_points(speed_data)

def record_system_data():
    total, used, free = shutil.disk_usage("/")
    data = [
        {
            "measurement" : "system_data",
            "tags": {
                "host": socket.gethostname()
            },
            "fields" : {
                "percent_used_disk_space": float(round(used / total * 100.0, 2)),
                "percent_used_ram":  float(psutil.virtual_memory().percent),
                "percent_used_cpu": float(psutil.cpu_percent())
            }
        }
    ]
    client.write_points(data)

schedule.every(1).minute.do(record_speed)
schedule.every(10).minutes.do(record_system_data)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)