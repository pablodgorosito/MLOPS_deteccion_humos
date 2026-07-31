-- Tabla para registrar cada inferencia realizada por las cámaras
CREATE TABLE IF NOT EXISTS detecciones_emisiones (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    porcentaje_polucion FLOAT NOT NULL,
    nivel_alerta VARCHAR(20) NOT NULL, -- Ej: 'NORMAL', 'PREALERTA', 'ALERTA'
    model_version VARCHAR(50),
    confidence_score FLOAT
);

-- Índice para acelerar las consultas de Power BI por rango de tiempo
CREATE INDEX IF NOT EXISTS idx_timestamp ON detecciones_emisiones(timestamp);