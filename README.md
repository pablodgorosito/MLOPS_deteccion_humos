# MLOPS_deteccion_humos

# 🏭 Sistema MLOps de Monitoreo de Emisiones y Polución (ALUAR)

> **Arquitectura On-Premise para Detección, Segmentación y Cuantificación de Humo/Vapor en Planta Industrial.**

---

## 📌 Visión General del Proyecto

Este proyecto tiene como objetivo implementar una solución integral de **MLOps (Machine Learning Operations)** totalmente **On-Premise** para la supervisión continua y detección automática de emisiones (humo y vapor) en las instalaciones de la planta. 

Utilizando un enfoque de **Visión por Computadora (Computer Vision)**, el sistema segmenta las plumas de emisión en tiempo real, calcula métricas de polución/densidad y disponibiliza los datos para tableros de control operativo en **Power BI**.

---

## 🏗️ Arquitectura del Sistema

La solución adopta las mejores prácticas de MLOps moderno para garantizar reproductibilidad, monitoreo continuo y baja latencia de respuesta en entorno local.

| Componente | Tecnología | Rol en la Arquitectura | Enlace de Documentación |
| :--- | :--- | :--- | :--- |
| **Data Lake Local** | **MinIO** | Almacenamiento S3 On-Premise para datasets de imágenes, clips y artefactos del modelo. | [Docs MinIO](https://min.io/docs/minio/container/index.html) |
| **Base de Datos** | **PostgreSQL** | Metadatos de MLflow/Airflow e historial operacional de inferencias para Power BI. | [Docs PostgreSQL](https://www.postgresql.org/docs/) |
| **Experiment Tracking** | **MLflow** | Registro de hiperparámetros, métricas de entrenamiento ($mAP$, Loss) y *Model Registry*. | [Docs MLflow](https://mlflow.org/docs/latest/index.html) |
| **Orquestación** | **Apache Airflow** | Pipelines automatizados para ingesta de datos, limpieza y reentrenamiento de modelos. | [Docs Apache Airflow](https://airflow.apache.org/docs/) |
| **Servicio de Inferencia**| **FastAPI** | API REST en Python que procesa imágenes/videos y retorna los porcentajes de polución. | [Docs FastAPI](https://fastapi.tiangolo.com/) |
| **Visualización** | **Power BI** | Tableros ejecutivos conectándose directo a la base de datos PostgreSQL. | [Docs Power BI](https://learn.microsoft.com/power-bi/) |

---

## 🎯 Estrategia de Modelado de Visión por Computadora

1. **Fase 1 (Línea Base) — YOLO-Segmentation (`YOLOv8-seg` / `YOLOv11-seg`):**
   * Se descarta el bounding box clásico en favor de **segmentación de instancias** para delimitar el contorno exacto de la columna de humo o vapor.
   * Permite calcular el área de cobertura porcentual respecto al campo de visión de la cámara.
2. **Fase 2 (Análisis Temporal):**
   * En caso de falsos positivos por dinámicas ambientales (polvo, luz), se evaluará incorporar memoria temporal vía secuencias de video (**YOLO + ConvLSTM** o **Video-Swin Transformers**).

---

## 🔗 Enlaces para Ampliar el Conocimiento Técnico

### A. MLOps y Despliegue On-Premise
* [MLOps Org - Principios y Arquitectura MLOps](https://ml-ops.org/)
* [Docker Compose Overview para Entornos On-Premise](https://docs.docker.com/compose/)

### B. Modelos de Visión por Computadora (YOLO & Segmentación)
* [Ultralytics Docs (YOLOv8 / YOLOv11)](https://docs.ultralytics.com/)
* [YOLO Instance Segmentation Guide](https://docs.ultralytics.com/tasks/segment/)
* [CVAT - Computer Vision Annotation Tool (Etiquetado)](https://cvat.ai/docs/)

### C. Tracking y Orquestación de Pipelines
* [MLflow Tracking & Model Registry Tutorial](https://mlflow.org/docs/latest/tracking.html)
* [Apache Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)

---

## 📂 Estructura Sugerida del Repositorio

```text
.
├── docker-compose.yml          # Configuración On-Premise (Postgres, MinIO, MLflow, Airflow)
├── README.md                   # Documentación principal del proyecto
├── data/                       # Scripts de descarga y preparación de datasets
├── models/                     # Arquitecturas, entrenamiento y exportación a ONNX
├── pipelines/                  # DAGs de Apache Airflow para orquestación
├── src_api/                    # Servicio REST con FastAPI para inferencias
│   ├── main.py
│   └── utils/
├── tests/                      # Pruebas unitarias e integración
└── notebooks/                  # Experimentos iniciales y EDA
