from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import sqlite3
from contextlib import asynccontextmanager

# Caminho do modelo e do Banco de Dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/random_forest.pkl")
DB_PATH = os.path.join(BASE_DIR, "historico.db")
modelo = None

# Função para criar o Banco de Dados se ele não existir
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
    iniciar_banco() # Cria a tabela quando o servidor liga
    yield

app = FastAPI(title="InovSpin API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
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
    
    entrada = [[
        dados.horas_uso, 
        dados.temperatura_c, 
        dados.vibracao_mms, 
        dados.corrente_a, 
        dados.fator_potencia
    ]]
    
    probabilidade = float(modelo.predict_proba(entrada)[0][1] * 100)
    previsao = modelo.predict(entrada)[0]
    
    causa_raiz = "Parâmetros normais."
    if probabilidade > 30:
        causas = []
        if dados.temperatura_c >= 75.0:
            causas.append(f"Temperatura excessiva ({dados.temperatura_c}°C)")
        if dados.vibracao_mms >= 5.0:
            causas.append(f"Vibração anormal ({dados.vibracao_mms} mm/s)")
        if dados.corrente_a >= 18.0:
            causas.append(f"Sobrecarga ({dados.corrente_a} A)")
            
        if causas:
            causa_raiz = " | ".join(causas)
        else:
            causa_raiz = "Desgaste geral por tempo de uso/fadiga."

    if previsao == 1 or probabilidade > 70:
        status = "🔴 RISCO CRÍTICO"
        recomendacao = "Pare o motor IMEDIATAMENTE. Troque rolamentos e verifique o alinhamento."
        roi = "Economia estimada de R$ 15.000,00 (evitando parada não programada)."
    elif probabilidade > 30:
        status = "🟡 ALERTA"
        recomendacao = "Agende manutenção preventiva. Monitore a temperatura de perto."
        roi = "Manutenção preventiva (R$ 1.500,00) recomendada para evitar custos."
    else:
        status = "🟢 NORMAL"
        recomendacao = "Motor operando dentro dos padrões ideais. Nenhuma ação necessária."
        roi = "Produção otimizada. Zero custos adicionais no momento."

    # --- SALVANDO NO BANCO DE DADOS ---
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analises (temperatura, vibracao, risco, status)
        VALUES (?, ?, ?, ?)
    ''', (dados.temperatura_c, dados.vibracao_mms, probabilidade, status))
    conn.commit()
    conn.close()
        
    return {
        "risco_falha_percentagem": round(probabilidade, 1),
        "status": status,
        "recomendacao": recomendacao,
        "roi_estimado": roi,
        "causa_raiz": causa_raiz
    }

# --- NOVO ENDPOINT: PEGAR O HISTÓRICO ---
@app.get("/historico")
def pegar_historico():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Pega as últimas 10 análises
    cursor.execute('SELECT temperatura, vibracao, risco, status, data_hora FROM analises ORDER BY id DESC LIMIT 10')
    linhas = cursor.fetchall()
    conn.close()
    
    historico = []
    for linha in linhas:
        historico.append({
            "temperatura": linha[0],
            "vibracao": linha[1],
            "risco": round(linha[2], 1),
            "status": linha[3],
            "hora": linha[4]
        })
    return {"historico": historico}