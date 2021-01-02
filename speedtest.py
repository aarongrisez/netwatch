import os
import schedule
import time
import re
import subprocess
from influxdb import InfluxDBClient

INFLUX_DB_HOST = os.environ.get("NETWATCH_INFLUX_DB_HOST", None)
INFLUX_DB_PASS = os.environ.get("NETWATCH_INFLUX_DB_PASS", None)

if INFLUX_DB_PASS is None:
    raise ValueError("Environment variable for NETWATCH_INFLUX_DB_PASS not set")
if INFLUX_DB_HOST is None:
    raise ValueError("Environment variable for NETWATCH_INFLUX_DB_HOST not set")

response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')

client = InfluxDBClient(INFLUX_DB_HOST, 8086, 'speedmonitor', INFLUX_DB_PASS, 'internetspeed')

def record():
    speed_data = [
        {
            "measurement" : "internet_speed",
            "fields" : {
                "download": float(download),
                "upload": float(upload),
                "ping": float(ping)
            }
        }
    ]
    client.write_points(speed_data)

schedule.every(3).seconds.do(record)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)