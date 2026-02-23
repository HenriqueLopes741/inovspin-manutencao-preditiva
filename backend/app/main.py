from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import sqlite3
from datetime import datetime
from contextlib import asynccontextmanager

# Configurações de Caminho
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/random_forest.pkl")
DB_PATH = os.path.join(BASE_DIR, "historico.db")
modelo = None

def iniciar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL,
            vibracao REAL,
            risco REAL,
            status TEXT,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global modelo
    if os.path.exists(MODEL_PATH):
        modelo = joblib.load(MODEL_PATH)
    iniciar_banco()
    yield

app = FastAPI(title="InovSpin API v2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DadosMotor(BaseModel):
    horas_uso: float
    temperatura_c: float
    vibracao_mms: float
    corrente_a: float
    fator_potencia: float

@app.post("/predict")
def prever_falha(dados: DadosMotor):
    if modelo is None:
        raise HTTPException(status_code=500, detail="Modelo não carregado.")
    
    # 1. Predição da IA
    entrada = [[dados.horas_uso, dados.temperatura_c, dados.vibracao_mms, dados.corrente_a, dados.fator_potencia]]
    prob_ia = float(modelo.predict_proba(entrada)[0][1] * 100)

    # 2. MOTOR ESPECIALISTA (Define tudo de uma vez para evitar bugs)
    t, v, c, fp = dados.temperatura_c, dados.vibracao_mms, dados.corrente_a, dados.fator_potencia

    # Caso 1: CRÍTICO (Prioridade máxima)
    if v >= 4.5 or t >= 85.0 or c >= 22.0:
        res = {
            "status": "🔴 RISCO CRÍTICO",
            "risco": max(prob_ia, 95.0),
            "causa": f"Severidade Técnica: {'Vibração' if v>=4.5 else 'Calor'} acima do limite ISO.",
            "recomenda": "PARADA IMEDIATA. Realizar análise de vibração e check de isolamento térmico.",
            "roi": "Evita quebra catastrófica. Economia estimada: R$ 15.000,00."
        }
    
    # Caso 2: ALERTA
    elif v >= 2.8 or t >= 70.0 or fp < 0.85:
        res = {
            "status": "🟡 ALERTA",
            "risco": max(prob_ia, 55.0),
            "causa": "Desvio de performance detectado (Baixa eficiência ou desgaste mecânico).",
            "recomenda": "Agendar inspeção visual e lubrificação dos mancais em até 48h.",
            "roi": "Prevenção de danos secundários. Economia estimada: R$ 1.500,00."
        }

    # Caso 3: NORMAL
    else:
        res = {
            "status": "🟢 NORMAL",
            "risco": prob_ia,
            "causa": "Parâmetros operacionais dentro da normalidade (ISO 10816).",
            "recomenda": "Motor operando conforme o planejado. Nenhuma ação necessária.",
            "roi": "Disponibilidade de ativo em 100%. Zero custos adicionais."
        }

    # 3. Salvar no Banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO analises (temperatura, vibracao, risco, status) VALUES (?, ?, ?, ?)',
                   (t, v, res["risco"], res["status"]))
    conn.commit()
    conn.close()
        
    return {
        "risco_falha_percentagem": round(res["risco"], 1),
        "status": res["status"],
        "recomendacao": res["recomenda"],
        "roi_estimado": res["roi"],
        "causa_raiz": res["causa"]
    }

@app.get("/historico")
def pegar_historico():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT temperatura, vibracao, risco, status, data_hora FROM analises ORDER BY id DESC LIMIT 10')
    linhas = cursor.fetchall()
    conn.close()
    return {"historico": [{"temperatura": l[0], "vibracao": l[1], "risco": l[2], "status": l[3], "hora": l[4]} for l in linhas]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)