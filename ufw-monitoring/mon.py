#!/usr/bin/python2.7

# export number of connections blocked by UFW as a prometheus metric
# v.0.3

from datetime import date
from prometheus_client import start_http_server, Gauge
import re
import time

# config
delay=10    # delay between measurments
port=50028  # metrics expose port

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


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(port)
    # Generate some requests.
    while True:
        monitor()
        time.sleep(delay)
