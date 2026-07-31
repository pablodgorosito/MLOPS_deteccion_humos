import os
import io
import time
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from PIL import Image
import numpy as np
# Decomentar cuando tengas el modelo entrenado cargado
# from ultralytics import YOLO 

app = FastAPI(
    title="Aluar - API de Inferencia para Detección de Emisiones",
    version="1.0.0",
    description="API MLOps para la detección y cuantificación de humo/polución en tiempo real."
)

# Configuración de base de datos tomada del entorno
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://mlops_user:mlops_password@postgres:5432/mlops_db"
)

def get_db_connection():
    """Establece conexión con PostgreSQL."""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Error conectando a la BD: {e}")
        return None

# Carga del modelo (Mock inicial / Placeholder)
# model = YOLO("models/best.pt")

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Endpoint para verificar el estado del servicio y la conexión a la BD."""
    conn = get_db_connection()
    db_status = "connected" if conn else "disconnected"
    if conn:
        conn.close()
    return {
        "status": "online",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/predict")
async def predict_emissions(
    camera_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Procesa un frame recibido de una cámara, calcula el nivel de emisión y guarda en PostgreSQL.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo enviado no es una imagen válida.")

    try:
        # 1. Leer imagen enviada por la cámara
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        img_np = np.array(image)

        # 2. Ejecutar Inferencia (Mock/Simulación temporal hasta enganchar los pesos de MLflow)
        start_time = time.time()
        
        # --- SUSTITUIR POR INFERENCIA REAL DE YOLO ---
        # results = model(img_np)
        # porcentaje_polucion = float(results[0].probs) ...
        
        # Simulación de inferencia:
        porcentaje_polucion = round(float(np.random.uniform(5.0, 85.0)), 2)
        confidence_score = 0.94
        model_version = "v1.0.0-yolov8"
        # ---------------------------------------------

        # Determinar nivel de alerta
        if porcentaje_polucion < 30.0:
            nivel_alerta = "NORMAL"
        elif porcentaje_polucion < 60.0:
            nivel_alerta = "PREALERTA"
        else:
            nivel_alerta = "ALERTA"

        # 3. Persistir resultado en la Base de Datos para consumo de Power BI
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO detecciones_emisiones (camera_id, porcentaje_polucion, nivel_alerta, model_version, confidence_score)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, timestamp;
            """
            cursor.execute(query, (camera_id, porcentaje_polucion, nivel_alerta, model_version, confidence_score))
            record = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()
            
            record_id = record['id']
            timestamp = record['timestamp'].isoformat()
        else:
            record_id = None
            timestamp = datetime.utcnow().isoformat()

        return {
            "id_registro": record_id,
            "camera_id": camera_id,
            "timestamp": timestamp,
            "porcentaje_polucion": porcentaje_polucion,
            "nivel_alerta": nivel_alerta,
            "confidence_score": confidence_score,
            "model_version": model_version,
            "inference_time_ms": round((time.time() - start_time) * 1000, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {str(e)}")