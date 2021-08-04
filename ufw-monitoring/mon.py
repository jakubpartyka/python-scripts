#!/usr/bin/python2.7
from datetime import date
from prometheus_client import start_http_server, Gauge
import re
import time

# date 
t = date.today().strftime("%b %e.*")

# match patterns
p = re.compile(t)
p1 = re.compile('.*255.255.255.255.*')

# create prometheus gauge
g = Gauge('blocked_connections', 'Numbers of connections blocked by the firewall')


def monitor():
    # open ufw log
    f = open('/var/log/ufw.log','r')
    counter = 0

    for line in f.readlines():
        if p.match(line) and not p1.match(line):
            counter += 1
    f.close()
    g.set(counter)

    time.sleep(20)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8080)
    # Generate some requests.
    while True:
        monitor()
