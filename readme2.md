# 🚨 SmokeGuard AI: Sistema Embebido de Detección y Clasificación de Humo

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-CUDA%20Accelerated-orange.svg)](https://pytorch.org/)
[![NVIDIA Jetson](https://img.shields.io/badge/Hardware-NVIDIA%20Jetson%20Nano-76B900.svg)](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)

Un sistema de visión por computadora y Edge AI diseñado para la captura de video en tiempo real desde una cámara RGB, filtrado liviano de movimiento y clasificación por **Deep Learning** con evaluación de umbrales multicriterio para alertas de incendio.

---

## 📋 Tabla de Contenidos

- [Visión General del Sistema](#-visión-general-del-sistema)
- [Arquitectura por Etapas](#-arquitectura-por-etapas)
- [Requisitos de Hardware y Software](#-requisitos-de-hardware-y-software)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso](#-uso)
- [Lógica de Umbrales y Alertas](#-lógica-de-umbrales-y-alertas)
- [Optimizaciones para Edge Computing](#-optimizaciones-para-edge-computing)

---

## 🔍 Visión General del Sistema

El objetivo de este sistema es procesar la transmisión de una cámara de manera eficiente en dispositivos embebidos (como una **NVIDIA Jetson Nano**). Para no saturar la GPU procesando fotogramas estáticos o vacíos, el flujo se divide en un **filtro de movimiento básico** en CPU y una **fase de clasificación por IA** en GPU que solo se activa al detectar cambios significativos en la escena.

## 🛠️ Arquitectura por Etapas

### 1. Captura y Filtrado por Movimiento (CPU)
* **Técnica:** Sustracción de Fondo (*Background Subtraction*) mediante el algoritmo `MOG2` de OpenCV.
* **Propósito:** Filtra cambios insignificantes (luz constante, objetos estáticos) para evitar sobrecalentar el chip y reducir consumo eléctrico.

### 2. Preprocesamiento e Inferencia (GPU)
* **Preprocesamiento:** Reordenamiento de canales de **BGR a RGB**, redimensionado de imagen y normalización de píxeles al rango $[0, 1]$.
* **Carga en GPU:** Envío de tensores a CUDA (`tensor.to('cuda')`).
* **Clases de Salida:**
  - `0`: Sin Humo / Vapor de Agua (Riesgo Bajo)
  - `1`: Humo Claro / Blanco (Combustión inicial)
  - `2`: Humo Denso / Negro (Plásticos, sintéticos, hidrocarburos - **Peligro Alto**)
  - `3`: Fuego / Llama Directa (**Peligro Crítico**)

### 3. Lógica de Umbral Multicriterio
* Evita falsos positivos mediante tres filtros combinados:
  1. **Umbral de Confianza:** Certeza del modelo $\ge 75\%$.
  2. **Persistencia Temporal:** Detección sostenida durante $N$ fotogramas consecutivos.
  3. **Severidad:** Prioridad de respuesta rápida ante humo denso o fuego.

---

## 💻 Requisitos de Hardware y Software

### Hardware
* **Dispositivo Embebido:** NVIDIA Jetson Nano (o PC/Laptop con GPU NVIDIA).
* **Cámara:** Cámara USB 2.0/3.0 o módulo de cinta de video MIPI CSI (ej. Raspberry Pi Cam v2).

### Software
* **Sistema Operativo:** Ubuntu 18.04 LTS / 20.04 LTS (JetPack SDK para Jetson).
* **Entorno Python:** Python 3.8+
* **Librerías Principales:**
  - `opencv-python`
  - `numpy`
  - `torch` / `torchvision` (con soporte CUDA habilitado)

---

## 📁 Estructura del Proyecto

```text
smoke-detection-system/
├── assets/                  # Capturas, diagramas y referencias
├── models/                  # Pesos del modelo (.pth, .onnx, .engine)
├── src/
│   ├── __init__.py
│   ├── capture.py           # Módulo de lectura de cámara (Multithreading)
│   ├── detector.py          # Lógica de detección MOG2 e Inferencia PyTorch
│   └── threshold_engine.py  # Evaluación de reglas de peligro
├── main.py                  # Script principal de ejecución
├── requirements.txt         # Dependencias
└── README.md                # Documentación del proyecto
