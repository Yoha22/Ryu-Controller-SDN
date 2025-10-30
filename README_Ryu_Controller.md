# 🧠 Controlador SDN Ryu — Guía Completa de Instalación y Pruebas con Mininet

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

### 2️⃣ Instalar dependencias
```bash
sudo apt install -y python3 python3-pip python3-venv git mininet
```

### 3️⃣ Crear entorno virtual
```bash
mkdir ~/ryu
cd ~/ryu
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Instalar Ryu y dependencias compatibles
```bash
pip install eventlet==0.33.3 dnspython==2.6.1
pip install ryu
```

> 💡 **Nota:** Eventlet y dnspython deben instalarse antes de Ryu para evitar errores de compatibilidad con Python 3.12.

### 5️⃣ Verificar instalación
```bash
ryu-manager --version
```
Debe mostrar:
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

### 2️⃣ Comprobar conectividad
```bash
mininet> pingall
```

Debe mostrar un **100% de éxito**.

### 3️⃣ Probar conexión HTTP con `curl`
```bash
mininet> h1 python3 -m http.server 80 &
mininet> h2 curl http://10.0.0.1
```

---

## 🔥 Ejemplo práctico: Controlador REST Firewall

Ryu incluye un ejemplo de **firewall con interfaz REST**, el cual permite crear, listar y eliminar reglas dinámicamente.

### 1️⃣ Ejecutar el controlador
```bash
ryu-manager ryu.app.rest_firewall
```

### 2️⃣ Iniciar Mininet con un switch remoto
```bash
sudo mn --topo single,3 --controller remote --mac --switch ovsk
```

### 3️⃣ Probar conectividad inicial
```bash
mininet> pingall
```

### 4️⃣ Consultar estado del firewall
En otra terminal:
```bash
curl http://127.0.0.1:8080/firewall/module/status
```

### 5️⃣ Agregar una regla (bloquear h1 → h2)
```bash
curl -X POST -d '{"nw_src":"10.0.0.1","nw_dst":"10.0.0.2","actions":"DENY"}' http://127.0.0.1:8080/firewall/rules/all
```

### 6️⃣ Verificar nuevamente la conectividad
```bash
mininet> pingall
```
Ahora h1 no podrá comunicarse con h2.

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

## 🧠 Recursos adicionales

- 📄 [Documentación oficial de Ryu](https://ryu.readthedocs.io/)
- 🧩 [Repositorio GitHub de Ryu](https://github.com/faucetsdn/ryu)
- 🧪 [Mininet](http://mininet.org/)
- 📘 RFC 7426 — *Software-Defined Networking (SDN) Layers and Architecture Terminology*

---

## 🏁 Conclusión

Ryu es una herramienta poderosa y flexible para **experimentar con redes SDN** en entornos controlados.  
Su facilidad de uso, modularidad y compatibilidad con **OpenFlow** lo convierten en la opción ideal para **aprender, investigar y desarrollar prototipos** de controladores inteligentes.

---

**Autor:** _Yohan David Morelo Julio_  
**Versión del documento:** 1.0  
**Última actualización:** Octubre 2025
