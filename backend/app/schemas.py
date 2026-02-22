from pydantic import BaseModel

class SensorData(BaseModel):
    horas_uso: float
    temperatura_c: float
    vibracao_mms: float
    corrente_a: float
    fator_potencia: float

class PredictionResponse(BaseModel):
    risco_falha_percentagem: float
    status: str
    recomendacao: str
    roi_estimado: str