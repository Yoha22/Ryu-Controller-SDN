# 🧠 Controlador SDN Ryu — Guía Completa de Instalación y Pruebas con Mininet

**Autores:** _Yohan David Morelo Julio_ _y_ _Nayelys Ocampo_                                                                              
**Versión del documento:** 1.2  
**Última actualización:** Octubre 2025

---

## Tabla de Contenido
- [📘 Introducción Teórica](#📘-introducción-teórica)
- [💡 ¿Qué es Ryu?](#💡-qué-es-ryu)
- [⚙️ Cuándo usar y cuándo no usar Ryu](#⚙️-cuándo-usar-y-cuándo-no-usar-ryu)
- [📋 Requerimientos](#📋-requerimientos)
- [🧩 Instalación paso a paso](#🧩-instalación-paso-a-paso)
- [🧪 Entorno de pruebas con Mininet](#🧪-entorno-de-pruebas-con-mininet)
- [🔥 Ejemplo práctico: Controlador REST Firewall](#🔥-ejemplo-práctico-controlador-rest-firewall)
- [🧑‍💻 Topologías avanzadas en Mininet usando Python](#🧑‍💻-topologías-avanzadas-en-mininet-usando-python)
- [💻 Tips para Windows y Virtualización](#💻-tips-para-windows-y-virtualización)
- [📊 Análisis de tráfico de red en el laboratorio](#📊-análisis-de-tráfico-de-red-en-el-laboratorio)
- [🧱 Diagrama conceptual del flujo SDN con Ryu y Mininet](#🧱-diagrama-conceptual-del-flujo-sdn-con-ryu-y-mininet)
- [⚠️ Problemas comunes y soluciones](#⚠️-problemas-comunes-y-soluciones)
- [📂 Estructura recomendada del proyecto](#📂-estructura-recomendada-del-proyecto)
- [🛠 Troubleshooting avanzado y FAQ](#🛠-troubleshooting-avanzado-y-faq)
- [🏁 Flujo típico de laboratorio SDN](#🏁-flujo-típico-de-laboratorio-sdn)
- [📚 Referencias útiles](#📚-referencias-útiles)
- [🏁 Conclusión](#🏁-conclusión)

---

## 📘 Introducción Teórica

### ¿Qué es SDN (Software Defined Networking)?

Las **Redes Definidas por Software (SDN)** separan el **plano de control** (decisiones sobre cómo manejar el tráfico) del **plano de datos** (encargado de reenviar los paquetes).  
Esto permite una **mayor flexibilidad**, **automatización** y **centralización** en la gestión de la red.

```
           ┌───────────────────────────────┐
           │        Controlador SDN        │
           │ (Plano de control centralizado)│
           └──────────────┬────────────────┘
                          │ OpenFlow
                          ▼
┌──────────────┬──────────────┬──────────────┐
│   Switch 1   │   Switch 2   │   Switch 3   │
│(Plano de datos)│(Plano de datos)│(Plano de datos)│
└──────────────┴──────────────┴──────────────┘
```

El **controlador SDN** es el cerebro de la red: recibe información de los switches y decide cómo deben fluir los paquetes.

---

## 💡 ¿Qué es Ryu?

**Ryu** es un **framework de código abierto** escrito en **Python** para desarrollar aplicaciones SDN.  
Proporciona una API sencilla para interactuar con dispositivos OpenFlow y controlar dinámicamente el comportamiento de la red.

### 🔍 Características principales

- Compatible con **OpenFlow 1.0 - 1.5**
- Escrito completamente en **Python**
- API REST integrada para desarrollo rápido
- Extensible mediante módulos
- Ideal para **experimentación, docencia e investigación**

### 🧩 Principales controladores y aplicaciones integradas en Ryu

Ryu incluye varios controladores y aplicaciones listos para ser usados o adaptados en laboratorios SDN, cada uno con una funcionalidad diferente:

| Nombre (app)                       | Funcionalidad principal                                                                          |
|-------------------------------------|--------------------------------------------------------------------------------------------------|
| simple_switch                      | Switch L2 de reenvío básico (OpenFlow 1.0).                                                      |
| simple_switch_13                   | Switch L2 para OpenFlow 1.3, mayor flexibilidad e inspección.                                    |
| simple_hub                         | Funcionamiento tipo hub: reenvía todo a todos los puertos (excepto el de entrada).               |
| l2_multi_switch                    | Múltiples switches, reenvío Capa 2 básico.                                                       |
| l3_switch                          | Enrutador simple de Capa 3 para varias subredes.                                                 |
| ofctl_rest                         | API RESTful para gestionar y consultar flujos OpenFlow de forma sencilla.                        |
| topology                           | API REST de consulta de topología de red controlada por Ryu.                                     |
| rest_firewall                      | Firewall REST: permite crear, modificar o borrar reglas de filtrado en tiempo real vía HTTP.     |
| rest_qos                           | Gestiona reglas de Calidad de Servicio (QoS) vía REST.                                           |
| rest_loadbalancer                  | Reglas y balanceo de carga simple vía REST.                                                      |
| rest_router                        | Router SDN gestionable por REST API.                                                             |
| rest_conf_switch                   | Configuración dinámica de switches vía REST.                                                     |
| rest_topology                      | Consulta y vista de topología OpenFlow vía REST.                                                 |
| rest                         | Ejemplo de servidor REST genérico para interacciones básicas.                                       |
| ofctl_rest                         | Ejemplo avanzado de servidor REST para administrar flujos y grupos.                               |

> Existen más ejemplos y aplicaciones, estos son los más usados en pruebas docencia/laboratorio. Todos se encuentran en el paquete `ryu.app` o la documentación oficial.

---

## ⚙️ Cuándo usar y cuándo no usar Ryu

### ✅ Recomendado para:

- Laboratorios SDN y proyectos universitarios.
- Investigación sobre enrutamiento, QoS, balanceo de carga, etc.
- Prototipado rápido de controladores OpenFlow.
- Integración con **Mininet** para simulaciones.

### ❌ No recomendado para:

- Entornos de **producción a gran escala**.
- Redes de alto rendimiento con miles de flujos por segundo.
- Aplicaciones que requieran **baja latencia extrema** o escalabilidad horizontal inmediata.

---

## 📋 Requerimientos

| Componente | Versión recomendada | Descripción |
|-------------|--------------------|--------------|
| Ubuntu | 22.04 LTS o 24.04 LTS | Sistema base |
| Python | 3.10 – 3.12 | Lenguaje de programación |
| Mininet | ≥ 2.3.0 | Simulador de red |
| Ryu | 4.34 | Controlador SDN |
| Eventlet | 0.33.3 | Librería de concurrencia compatible |
| dnspython | 2.6.1 | Requerido por Ryu |
| git | Última versión | Control de versiones |

---

## 🧩 Instalación paso a paso

### 1️⃣ Actualizar el sistema
```bash
sudo apt update && sudo apt upgrade -y
```

**Salida esperada:**
```
...
Fetched 2,456 kB in 3s (818 kB/s)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
```

### 2️⃣ Instalar dependencias
```bash
sudo apt install -y python3 python3-pip python3-venv git mininet
```

**Salida esperada:**
```
Reading package lists... Done
Building dependency tree... Done
...
Setting up mininet (2.3.0+dfsg-4ubuntu1) ...
Setting up python3-venv (3.10.12-1~22.04) ...
done.
```

### 3️⃣ Crear entorno virtual
```bash
mkdir ~/ryu
cd ~/ryu
python3 -m venv venv
source venv/bin/activate
```

**Salida esperada:**
```
(venv) user@ubuntu:~/ryu$
```

> 💡 **Nota:** El prompt cambia a `(venv)` indicando que el entorno virtual está activo.

### 4️⃣ Instalar Ryu y dependencias compatibles
```bash
pip install eventlet==0.33.3 dnspython==2.6.1
pip install ryu
```

**Salida esperada:**
```
Collecting eventlet==0.33.3
  Downloading eventlet-0.33.3-py3-none-any.whl (220 kB)
Successfully installed eventlet-0.33.3 dnspython-2.6.1
Collecting ryu
  Downloading ryu-4.34-py3-none-any.whl (1.2 MB)
Successfully installed ryu-4.34 ...
```

> 💡 **Nota:** Eventlet y dnspython deben instalarse antes de Ryu para evitar errores de compatibilidad con Python 3.12.

### 5️⃣ Verificar instalación
```bash
ryu-manager --version
```

**Salida esperada:**
```
ryu-manager 4.34
```

---

## 🧪 Entorno de pruebas con Mininet

### 1️⃣ Iniciar topología de prueba
Ejemplo: 3 hosts y 1 switch.
```bash
sudo mn --topo single,3 --controller remote --mac --switch ovsk
```

**Salida esperada:**
```
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 h3
*** Adding switches:
s1
*** Adding links:
(h1, s1) (h2, s1) (h3, s1)
*** Configuring hosts
h1 h2 h3
*** Starting controller
c0
*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet>
```

### 2️⃣ Comprobar conectividad
```bash
mininet> pingall
```

**Salida esperada:**
```
*** Ping: testing ping reachability between hosts
h1 -> h2 h3
h2 -> h1 h3
h3 -> h1 h2
*** Results: 0% dropped (6/6 received)
```

### 3️⃣ Probar conexión HTTP con `curl`
```bash
mininet> h1 python3 -m http.server 80 &
mininet> h2 curl http://10.0.0.1
```

**Salida esperada:**
```
[1] 12345
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
...
</head>
<body>
Directory listing for /
</body>
</html>
```

---

## 🔥 Ejemplo práctico: Controlador REST Firewall

Ryu incluye un ejemplo de **firewall con interfaz REST**, el cual permite crear, listar y eliminar reglas dinámicamente.

### 1️⃣ Ejecutar el controlador
```bash
ryu-manager ryu.app.rest_firewall
```

**Salida esperada:**
```
loading app ryu.app.rest_firewall
loading app ryu.controller.ofp_handler
instantiating app ryu.app.rest_firewall of RestFirewall
instantiating app ryu.controller.ofp_handler of OFPHandler
BRICK rest_firewall
  PROVIDES:
    rest_firewall
  CONSUMES:
    ofp_event
BRICK ofp_handler
  PROVIDES:
    ofp_event
  CONSUMES:
    main
(15823) wsgi starting up on http://0.0.0.0:8080/
```

### 2️⃣ Iniciar Mininet con un switch remoto
```bash
sudo mn --topo single,3 --controller remote --mac --switch ovsk
```

**Salida esperada:**
```
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 h3
*** Adding switches:
s1
*** Adding links:
(h1, s1) (h2, s1) (h3, s1)
*** Configuring hosts
h1 h2 h3
*** Starting controller
c0
*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet>
```

### 3️⃣ Probar conectividad inicial
```bash
mininet> pingall
```

**Salida esperada:**
```
*** Ping: testing ping reachability between hosts
h1 -> X X
h2 -> X X
h3 -> X X
*** Results: 100% dropped (0/6 received)
```

> ⚠️ **Nota:** El firewall bloquea todo el tráfico por defecto, por eso todos los pings fallan inicialmente.

### 4️⃣ Consultar estado del firewall
En otra terminal:
```bash
curl http://127.0.0.1:8080/firewall/module/status
```

**Salida esperada:**
```json
{
  "status": "enabled",
  "switches": [
    {
      "dpid": "0000000000000001",
      "status": "enabled"
    }
  ]
}
```

### 5️⃣ Agregar una regla (bloquear h1 → h2)
```bash
curl -X POST -d '{"nw_src":"10.0.0.1","nw_dst":"10.0.0.2","actions":"DENY"}' http://127.0.0.1:8080/firewall/rules/all
```

**Salida esperada:**
```json
{
  "0000000000000001": [
    {
      "rule_id": 1,
      "nw_src": "10.0.0.1",
      "nw_dst": "10.0.0.2",
      "actions": "DENY"
    }
  ]
}
```

### 6️⃣ Verificar nuevamente la conectividad
```bash
mininet> pingall
```

**Salida esperada:**
```
*** Ping: testing ping reachability between hosts
h1 -> X h3
h2 -> h1 h3
h3 -> h1 h2
*** Results: 16% dropped (5/6 received)
```

Ahora h1 no podrá comunicarse con h2 (X indica fallo).

---

### 🧰 Ejemplos de uso del firewall REST con Ryu

> ⚠️ **Por defecto, Ryu rest_firewall bloquea todo el tráfico. Debes crear reglas ALLOW explícitas para permitir la conectividad.**

- **Permitir TODO el tráfico IPv4 entre todos los hosts:**
```bash
curl -X POST -d '{"dl_type": "IPv4", "nw_src": "10.0.0.0/24", "nw_dst": "10.0.0.0/24", "actions": "ALLOW"}' http://127.0.0.1:8080/firewall/rules/all
```

**Salida esperada:**
```json
{
  "0000000000000001": [
    {
      "rule_id": 1,
      "dl_type": "IPv4",
      "nw_src": "10.0.0.0/24",
      "nw_dst": "10.0.0.0/24",
      "actions": "ALLOW"
    }
  ]
}
```

- **Bloquear el tráfico de un host origen a uno destino:**
```bash
curl -X POST -d '{"nw_src":"10.0.0.1","nw_dst":"10.0.0.2","actions":"DENY"}' http://127.0.0.1:8080/firewall/rules/all
```

**Salida esperada:**
```json
{
  "0000000000000001": [
    {
      "rule_id": 2,
      "nw_src": "10.0.0.1",
      "nw_dst": "10.0.0.2",
      "actions": "DENY"
    }
  ]
}
```

- **Permitir SOLO el tráfico de h1 a h4 (bloqueando el resto):**
(Paso 1, elimina todas las reglas previas)
```bash
# Primero, elimina todas las reglas del firewall
# Obtén los rule_id y switch_id con: curl http://127.0.0.1:8080/firewall/rules/all
curl -X DELETE http://127.0.0.1:8080/firewall/rules/<switch_id>/<rule_id>
```

**Salida esperada:**
```
Rule deleted successfully
```

(Paso 2, agrega la regla ALLOW)
```bash
curl -X POST -d '{"nw_src":"10.0.0.1","nw_dst":"10.0.0.4","actions":"ALLOW"}' http://127.0.0.1:8080/firewall/rules/all
```

**Salida esperada:**
```json
{
  "0000000000000001": [
    {
      "rule_id": 1,
      "nw_src": "10.0.0.1",
      "nw_dst": "10.0.0.4",
      "actions": "ALLOW"
    }
  ]
}
```

- **Ver todas las reglas (y su orden/prioridad):**
```bash
curl http://127.0.0.1:8080/firewall/rules/all
```

**Salida esperada:**
```json
{
  "0000000000000001": [
    {
      "rule_id": 1,
      "nw_src": "10.0.0.1",
      "nw_dst": "10.0.0.2",
      "actions": "DENY"
    },
    {
      "rule_id": 2,
      "dl_type": "IPv4",
      "nw_src": "10.0.0.0/24",
      "nw_dst": "10.0.0.0/24",
      "actions": "ALLOW"
    }
  ]
}
```

- **Habilitar el firewall en un switch (imprescindible que esté "enable"):**
```bash
curl -X PUT -d '{"status":"enable"}' http://127.0.0.1:8080/firewall/module/enable/<dpid>
# Por ejemplo, para s1:
curl -X PUT -d '{"status":"enable"}' http://127.0.0.1:8080/firewall/module/enable/0000000000000001
```

**Salida esperada:**
```json
{
  "status": "enabled",
  "dpid": "0000000000000001"
}
```

---

## 🧑‍💻 Topologías avanzadas en Mininet usando Python

Puedes diseñar topologías personalizadas usando scripts Python. Ejemplo: `topo_test_hard.py` del repositorio.

### Ejecución típica con Ryu remoto
```bash
# En una terminal: lanza Ryu con un controlador (por ejemplo, el switch 13)
ryu-manager ryu.app.simple_switch_13
```

**Salida esperada:**
```
loading app ryu.app.simple_switch_13
instantiating app ryu.app.simple_switch_13 of SimpleSwitch13
BRICK simple_switch_13
  PROVIDES:
    simple_switch
  CONSUMES:
    ofp_event
```

```bash
# En otra terminal, ejecuta la topología avanzada:
sudo python3 topo_test_hard.py
```

**Salida esperada:**
```
=== Configuracion de topoloia personalizada ===
Ingrese el numero de switches (default=5): 3
Ingrese el numero de hosts (default=8): 4

*** Creando red...
*** Agregando controlador REMOTO para Ryu...
Se crearon los switches: ['s1', 's2', 's3']
Se crearon los hosts: ['h1', 'h2', 'h3', 'h4']

*** Conectando switches manualmente...

Con que switches quieres conectar s1? (ej: s2,s3 o Enter para ninguno): s2,s3
  Enlace creado: s1 s2
  Enlace creado: s1 s3

*** Conectando hosts a los switches finales...
¿A ue switch final conectaras h1? (ej: s5): s1
  Enlace creado: h1  s1
...

=== Resumen de topologia creada ===
Enlaces entre switches:
  s1 s2
  s1 s3
...

¿Deseas iniciar la red con esta configuracon? (s/n): s

*** Construyendo red...
*** Iniciando CLI de Mininet...
mininet>
```
- Puedes elegir el número de switches, hosts y cómo conectarlos.
- Los switches buscarán automáticamente a Ryu en 127.0.0.1:6633.
- Para usar otro IP o puerto (por ejemplo, en entorno distribuido):
```python
c0 = net.addController('c0', controller=RemoteController, ip='192.168.56.103', port=6633)
```

---

## 💻 Tips para Windows y Virtualización
- Si estás en Windows, se recomienda usar Mininet/Ubuntu en VirtualBox.
- Usa Xming para soporte gráfico (ej. wireshark/xterm) y PuTTY para conexión por SSH.
- Asegúrate de habilitar "Forwarding X11" en PuTTY y tener Xming encendido en tu máquina Windows.
  - Edita `/etc/ssh/sshd_config` para que incluya:
    - `X11Forwarding yes`
    - `X11UseLocalhost yes`
    - `XAuthLocation /usr/bin/X11/xauth`

---

## 📊 Análisis de tráfico de red en el laboratorio
- Para capturar tráfico con `tcpdump`:
```bash
mininet> h1 tcpdump -i h1-eth0
```

**Salida esperada:**
```
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on h1-eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
12:34:56.789012 IP 10.0.0.2 > 10.0.0.1: ICMP echo request, id 1, seq 1, length 64
12:34:56.789123 IP 10.0.0.1 > 10.0.0.2: ICMP echo reply, id 1, seq 1, length 64
...
```
- Para análisis gráfico, abre Wireshark en la VM y selecciona la interfaz deseada (ejemplo: `h1-eth0`).

---

## 🧱 Diagrama conceptual del flujo SDN con Ryu y Mininet

```
                   ┌──────────────────────────────┐
                   │       Controlador Ryu        │
                   │   (Plano de Control SDN)     │
                   └──────────────┬───────────────┘
                                  │ OpenFlow
                                  ▼
                       ┌──────────────────────┐
                       │       Switch OVS     │
                       │ (Plano de Datos)     │
                       └───────┬───────┬──────┘
                               │       │
                          ┌────┘       └────┐
                          ▼                 ▼
                   ┌────────────┐    ┌────────────┐
                   │ Host h1    │    │ Host h2    │
                   │10.0.0.1    │    │10.0.0.2    │
                   └────────────┘    └────────────┘
```

---

## ⚠️ Problemas comunes y soluciones

| Error | Causa | Solución |
|-------|--------|-----------|
| `AttributeError: module 'collections' has no attribute 'MutableMapping'` | Incompatibilidad de `dnspython` con Python 3.12 | `pip install dnspython==2.6.1` |
| `AttributeError: 'eventlet.green.thread' has no attribute 'daemon_threads_allowed'` | `eventlet` no actualizado para Python 3.12 | `pip install eventlet==0.33.3` |
| `ryu-manager: command not found` | El entorno virtual no está activado | `source venv/bin/activate` |
| Fallo en `pingall` | Controlador no iniciado o mal configurado | Revisar que `ryu-manager` esté en ejecución |
| `curl: (7) Failed to connect` | Puerto REST no disponible | Verificar que el controlador exponga el puerto 8080 |

---

## 📂 Estructura recomendada del proyecto

```
/home/usuario/ryu/
├── venv/
├── firewall_rules/
│   └── rules.json
├── logs/
│   └── ryu.log
├── README_Ryu_Controller.md
└── pruebas/
    └── topo_test.py
```

---

## 🛠 Troubleshooting avanzado y FAQ
- Si algún switch muestra "Unable to contact the remote controller...":
  - Verifica que Ryu esté corriendo.
  - Checa que la IP/puerto coincidan y no haya firewalls bloqueando.
  - Usa el comando `sudo mn -c` para limpiar redes previas.
- ¿No hay conectividad/flows?:
  - Asegura que tu app de Ryu funciona (ver logs en consola).
  - Verifica que el pipeline de tu script Python no tenga hosts "colgados".

---

## 🏁 Flujo típico de laboratorio SDN
1. Arranca la VM o tu entorno.
2. Activa entorno virtual si aplica: `source venv/bin/activate`
3. Levanta Ryu manager con tu app o ejemplo.
4. Ejecuta tu topología en Mininet.
5. Haz pruebas (ping, http, reglas REST, captura de tráfico, etc).
6. Finaliza y limpia la red: `exit` y `sudo mn -c`.

---

## 📚 Referencias útiles
- [Documentación oficial Mininet](http://mininet.org/walkthrough/)
- [Ejemplos de apps Ryu](https://ryu.readthedocs.io/en/latest/app.html)

---

## 🏁 Conclusión

Ryu es una herramienta poderosa y flexible para **experimentar con redes SDN** en entornos controlados.  
Su facilidad de uso, modularidad y compatibilidad con **OpenFlow** lo convierten en la opción ideal para **aprender, investigar y desarrollar prototipos** de controladores inteligentes.

---