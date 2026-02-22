import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

def train_and_save_model():
    # Caminhos absolutos para não ter erro de pasta
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "../data/dados_manutencao_preditiva.csv")
    MODEL_DIR = os.path.join(BASE_DIR, "../models")
    MODEL_PATH = os.path.join(MODEL_DIR, "random_forest.pkl")

    # Verifica se o CSV existe
    if not os.path.exists(DATA_PATH):
        print("Erro: Arquivo CSV não encontrado! Rode o generate_data.py primeiro.")
        return

    # Carrega os dados
    df = pd.read_csv(DATA_PATH)
    
    # Separa X (features) e y (alvo/target)
    X = df.drop('falha', axis=1)
    y = df['falha']
    
    # Divide em treino e teste (80% treino, 20% teste)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Inicializa e treina o modelo
    print("Treinando o modelo de Inteligência Artificial...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Avalia a acurácia
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {accuracy * 100:.2f}%")
    
    # Cria a pasta models se não existir e salva o modelo
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Modelo salvo com sucesso em: {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()