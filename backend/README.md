# InovSpin PRO - Monitoramento Preditivo de Motores Industriais

Este projeto é uma solução de **Manutenção Preditiva** voltada para a Indústria 4.0, focada no monitoramento de **Motores de Indução Trifásicos (ex: WEG W22 50CV)**. O sistema utiliza uma abordagem de **IA Híbrida**, combinando Machine Learning com normas técnicas internacionais de engenharia para garantir máxima confiabilidade.

## 🚀 Funcionalidades
- **Diagnóstico em Tempo Real:** Análise instantânea de Temperatura, Vibração, Corrente e Fator de Potência.
- **IA de Predição:** Modelo *Random Forest* treinado para identificar padrões de falha antes que ocorram.
- **Motor Especialista (ISO 10816):** Validação rigorosa dos dados de vibração conforme normas técnicas globais de severidade.
- **Cálculo de ROI:** Demonstração clara da economia financeira gerada pela prevenção de paradas não planejadas.
- **Histórico de Tendências:** Interface visual para acompanhamento da evolução da saúde do ativo ao longo do tempo.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python, FastAPI, Scikit-learn, Joblib.
- **Frontend:** React.js, Vite, Recharts (Gráficos), Tailwind CSS.
- **Banco de Dados:** SQLite para armazenamento persistente do histórico de análises.

## 📋 Normas Técnicas Aplicadas
O sistema utiliza os limites da **ISO 10816-3** para classificar a severidade da vibração e garantir a integridade do motor:
- **🟢 Bom (< 2.8 mm/s):** Operação segura e otimizada.
- **🟡 Alerta (2.8 - 4.5 mm/s):** Necessidade de agendamento de inspeção preventiva.
- **🔴 Crítico (> 4.5 mm/s):** Risco de falha iminente e recomendação de parada obrigatória.

## 🔧 Como Executar

### Backend
1. Navegue até a pasta `backend`.
2. Ative seu ambiente virtual (`venv`).
3. Instale as dependências: `pip install -r requirements.txt`.
4. Inicie o servidor: `python main.py`.

### Frontend
1. Navegue até a pasta `frontend`.
2. Instale as dependências: `npm install`.
3. Inicie a aplicação: `npm run dev`.

---
*Este projeto demonstra a integração de sistemas Full Stack com Inteligência Artificial aplicada a problemas reais da engenharia industrial.*