import pandas as pd
import numpy as np
import os

def generate_sensor_data(num_samples=1000):
    # Caminhos absolutos para evitar erros
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "dados_manutencao_preditiva.csv")

    np.random.seed(42)
    horas_uso = np.random.randint(100, 10000, num_samples)
    temperatura = np.random.normal(45, 5, num_samples)
    vibracao = np.random.normal(2.0, 0.5, num_samples)
    corrente = np.random.normal(15, 2, num_samples)
    fator_potencia = np.random.normal(0.92, 0.02, num_samples)
    falha = np.zeros(num_samples)

    for i in range(num_samples):
        prob_falha = 0.01
        if horas_uso[i] > 8000: prob_falha += 0.2
        if temperatura[i] > 65: prob_falha += 0.4
        if vibracao[i] > 4.5: prob_falha += 0.3
        if fator_potencia[i] < 0.85: prob_falha += 0.2

        if np.random.rand() < prob_falha:
            falha[i] = 1
            temperatura[i] += np.random.normal(20, 5)
            vibracao[i] += np.random.normal(3, 1)
            corrente[i] += np.random.normal(10, 3)
            fator_potencia[i] -= np.random.normal(0.1, 0.02)

    df = pd.DataFrame({
        'horas_uso': horas_uso, 'temperatura_c': temperatura,
        'vibracao_mms': vibracao, 'corrente_a': corrente,
        'fator_potencia': fator_potencia, 'falha': falha.astype(int)
    })

    df.to_csv(DATA_PATH, index=False)
    print(f"Dataset gerado com sucesso com {num_samples} motores em: {DATA_PATH}")

if __name__ == "__main__":
    generate_sensor_data()