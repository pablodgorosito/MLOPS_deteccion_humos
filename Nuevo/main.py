import cv2
import numpy as np
import torch

# 1. Configuración de Dispositivo y Umbrales
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Sistema corriendo en: {device}")

# Parámetros para la Etapa 1 (Detección de Movimiento)
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=25, detectShadows=False)
MIN_CHANGED_PIXELS = 4000 

# Parámetros para la Etapa 3 (Umbral de Peligro)
CONFIDENCE_THRESHOLD = 0.75
TEMPORAL_THRESHOLD = 5  # Fotogramas consecutivos
smoke_counter = 0

# 2. Captura de Cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("No se pudo acceder a la cámara RGB.")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # --- ETAPA 1: Sustracción de Fondo (CPU) ---
        fg_mask = bg_subtractor.apply(frame)
        changed_pixels = cv2.countNonZero(fg_mask)

        # Si hay cambio relevante en la escena
        if changed_pixels > MIN_CHANGED_PIXELS:
            
            # --- ETAPA 2: Preprocesamiento e Inferencia (GPU) ---
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized = cv2.resize(rgb, (224, 224))
            
            tensor = torch.from_numpy(resized).permute(2, 0, 1).unsqueeze(0).float() / 255.0
            tensor = tensor.to(device)

            # Simulación de inferencia del modelo
            detected_class = "Humo Negro"  # Clases: ["Vapor", "Humo Blanco", "Humo Negro", "Fuego"]
            confidence = 0.89

            # --- ETAPA 3: Lógica de Umbral de Peligro ---
            is_dangerous = detected_class in ["Humo Blanco", "Humo Negro", "Fuego"]
            
            if is_dangerous and confidence >= CONFIDENCE_THRESHOLD:
                smoke_counter += 1
            else:
                smoke_counter = max(0, smoke_counter - 1)

            # Disparo de alerta por persistencia temporal
            if smoke_counter >= TEMPORAL_THRESHOLD:
                if detected_class in ["Humo Negro", "Fuego"]:
                    print(f"🚨 ALERTA CRÍTICA: {detected_class} detectado. Confianza: {confidence:.2f}")
                else:
                    print(f"⚠️ ADVERTENCIA: {detected_class} en observación.")
        else:
            smoke_counter = max(0, smoke_counter - 1)

        cv2.imshow("Monitoreo de Humo - RGB", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
