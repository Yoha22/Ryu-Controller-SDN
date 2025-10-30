#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info


def run_topology():
    setLogLevel('info')

    print("\n=== Configuracion de topoloia personalizada ===")

    # === Entradas ===
    num_switches = int(input("Ingrese el numero de switches (default=5): ") or 5)
    num_hosts = int(input("Ingrese el numero de hosts (default=8): ") or 8)

    info('\n*** Creando red...\n')
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink, build=False)

    # === Agregar controlador ===
    info('*** Agregando controlador REMOTO para Ryu...\n')
    # Este controlador buscará un Ryu en 127.0.0.1:6633
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # === Crear switches ===
    switches = []
    for i in range(num_switches):
        sw = net.addSwitch(f's{i + 1}')
        switches.append(sw)
    info(f'Se crearon los switches: {[s.name for s in switches]}\n')

    # === Crear hosts ===
    hosts = []
    for i in range(num_hosts):
        h = net.addHost(f'h{i + 1}', ip=f'10.0.0.{i + 1}')
        hosts.append(h)
    info(f'Se crearon los hosts: {[h.name for h in hosts]}\n')

    # === Conexión manual de switches ===
    info('\n*** Conectando switches manualmente...\n')
    enlaces_sw = []

    for sw in switches:
        conectar = input(f"\nCon que switches quieres conectar {sw.name}? (ej: s2,s3 o Enter para ninguno): ").replace(" ", "")
        if conectar:
            for target_name in conectar.split(','):
                target = next((s for s in switches if s.name == target_name), None)
                if target and target != sw:
                    # Evita enlaces duplicados
                    if not net.linksBetween(sw, target):
                        net.addLink(sw, target)
                        enlaces_sw.append((sw.name, target.name))
                        print(f"  Enlace creado: {sw.name} {target.name}")
                else:
                    print(f"   Switch {target_name} no existe o es el mismo")

    # === Seleccionar switches finales (hojas) para conectar hosts ===
    info('\n*** Conectando hosts a los switches finales...\n')
    print("Puedes asignar varios hosts a un mismo switch final.")

    enlaces_hosts = []
    for h in hosts:
        destino = input(f"¿A ue switch final conectaras {h.name}? (ej: s5): ").strip()
        if destino:
            sw = next((s for s in switches if s.name == destino), None)
            if sw:
                net.addLink(h, sw)
                enlaces_hosts.append((h.name, sw.name))
                print(f"  Enlace creado: {h.name}  {sw.name}")
            else:
                print(f"  Switch {destino} no existe, omitiendo {h.name}")
        else:
            print(f"   {h.name} no fue conectado a ninun switch")

    # === Mostrar resumen de la topología creada ===
    print("\n=== Resumen de topologia creada ===")
    print("Enlaces entre switches:")
    for e in enlaces_sw:
        print(f"  {e[0]} {e[1]}")

    print("\nEnlaces entre hosts y switches:")
    for e in enlaces_hosts:
        print(f"  {e[0]} {e[1]}")

    confirmar = input("\n¿Deseas iniciar la red con esta configuracon? (s/n): ").lower()
    if confirmar != 's':
        print("Topologia cancelada.")
        return

    # === Construir e iniciar red ===
    info('\n*** Construyendo red...\n')
    net.build()
    c0.start()
    for s in switches:
        s.start([c0])

    info('\n*** Iniciando CLI de Mininet...\n')
    CLI(net)

    info('*** Deteniendo red...\n')
    net.stop()


if __name__ == '__main__':
    run_topology()