#!/usr/bin/env python3
"""
topo_test.py
----------------------------------------
Topología de prueba para Ryu Controller (REST Firewall)

Crea una topología simple:
    3 hosts (h1, h2, h3)
    1 switch (s1)
Conecta el switch a un controlador remoto Ryu.
----------------------------------------
Uso:
    sudo python3 topo_test.py
"""

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info


def run_topology():
    """Define y ejecuta la topología de prueba."""
    setLogLevel('info')

    info('*** Iniciando red...\n')
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSSwitch)

    info('*** Agregando controlador remoto (Ryu)...\n')
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    info('*** Agregando switch...\n')
    s1 = net.addSwitch('s1')

    info('*** Agregando hosts...\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')

    info('*** Creando enlaces...\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)

    info('*** Iniciando red...\n')
    net.start()

    info('*** Probando conectividad inicial (pingall)...\n')
    net.pingAll()

    # ------- PRUEBA DE FIREWALL: Bloqueo de h2 a h3 -------
    info('\n*** Probando política de firewall: h2 -> h3 (debería estar bloqueado si el firewall está activo)...\n')
    ping_result = h2.cmd('ping -c1 10.0.0.3')
    info(ping_result)
    if '0% packet loss' in ping_result:
        info('ADVERTENCIA: El firewall NO está bloqueando el tráfico entre h2 y h3.\n')
    else:
        info('Correcto: El firewall está bloqueando el tráfico entre h2 y h3.\n')

    # ------- PRUEBA TCP ENTRE HOSTS -------
    info('\n*** Probando conexión TCP: h2 -> h1:1234\n')
    h1.cmd('nc -l -p 1234 &')  # levantar servidor TCP en h1
    tcp_out = h2.cmd('echo "Hola Firewall" | nc 10.0.0.1 1234')
    if 'Hola Firewall' in tcp_out:
        info('Correcto: Tráfico TCP permitido de h2 a h1\n')
    else:
        info('ERROR: El tráfico TCP fue bloqueado (o netcat no está instalado)\n')

    info('*** Ejemplo: iniciar servidor HTTP en h1 y probar desde h2...\n')
    h1.cmd('python3 -m http.server 80 &')
    info(h2.cmd('curl http://10.0.0.1'))

    info('*** Red lista. Abriendo CLI...\n')
    CLI(net)

    info('*** Deteniendo red...\n')
    net.stop()


if __name__ == '__main__':
    run_topology()
