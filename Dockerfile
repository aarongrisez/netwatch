FROM python
WORKDIR /home/pi
COPY . /home/pi
RUN apt-get update && apt-get install -y systemd