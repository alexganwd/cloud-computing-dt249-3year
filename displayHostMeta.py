from flask import Flask
import socket
from netifaces import interfaces, ifaddresses, AF_INET
import multiprocessing
from psutil import virtual_memory
import json

app = Flask(__name__)
@app.route('/status')
def get_local_node_info():
    """ Decorated function, return json.dump with azure metadata """
    return json.dumps(generate_payload())



def generate_payload():
    """ Return payload with local node information as python object """
    return {
        'hostname': str(get_local_hostname()),
        'ip_address': str(get_local_ip_addresses()),
        'cpus': str(get_cpu_count()),
        'memory': str(get_physical_memory()) + 'GB'
    }


def get_local_hostname():
    """ Use socket info to get the hostname where this app is running on  """
    return socket.getfqdn()


def get_local_ip_addresses():
    """ Return a list of all the local IP addresses, ignoring loopback ofc """
    local_ip_addresses = list()
    for interface in interfaces():
        # AF_INET will return the Ip address which is on Network layer. To avoid non iterable objects, setting those to a dictonary with a null value.
        for ip_address in ifaddresses(interface).setdefault(AF_INET, [{'addr': ''}]):
            if ip_address['addr'] != '127.0.0.1' and ip_address['addr'] != '':
                local_ip_addresses.append(ip_address['addr'])

    return local_ip_addresses


def get_cpu_count():
    """ Return an int with the number of cpu in the system """
    return multiprocessing.cpu_count()


def get_physical_memory():
    """  Return a float with the total memory available in the system. Unit is GB """
    mem = virtual_memory()
    return mem.total/1024/1024/1024


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
