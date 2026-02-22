import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import GaugeChart from 'react-gauge-chart';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css'; 

function App() {
  const [formData, setFormData] = useState({
    horas_uso: 5000,
    temperatura_c: 60.0,
    vibracao_mms: 3.0,
    corrente_a: 15.0,
    fator_potencia: 0.90
  });

  const [resultado, setResultado] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [historico, setHistorico] = useState([]);

  const carregarHistorico = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/historico');
      if (response.data && response.data.historico) {
        setHistorico(response.data.historico.reverse());
      }
    } catch (error) {
      console.error("Erro ao carregar histórico:", error);
    }
  }, []);

  useEffect(() => {
    carregarHistorico();
  }, [carregarHistorico]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value)
    });
  };

  const preverFalha = async (e) => {
    e.preventDefault();
    setCarregando(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', formData);
      setResultado(response.data);
      carregarHistorico();
    } catch (error) {
      alert("Erro de conexão com o servidor.");
    }
    setCarregando(false);
  };

  const getStatusClass = (status) => {
    if (status.includes('CRÍTICO')) return 'status-critico';
    if (status.includes('ALERTA')) return 'status-alerta';
    return 'status-normal';
  };

  return (
    <div className="container">
      <header className="header">
        <h1>⚙️ InovSpin</h1>
        <p>Painel Inteligente de Manutenção Preditiva</p>
      </header>

      <div className="dashboard">
        
        {/* CARD DE ENTRADA (VOLTOU AO ORIGINAL) */}
        <div className="card">
          <h2>Parâmetros do Motor</h2>
          <form onSubmit={preverFalha}>
            <div className="form-group">
              <label>Horas de Uso:</label>
              <input type="number" name="horas_uso" value={formData.horas_uso} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Temperatura (°C):</label>
              <input type="number" step="0.1" name="temperatura_c" value={formData.temperatura_c} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Vibração (mm/s):</label>
              <input type="number" step="0.1" name="vibracao_mms" value={formData.vibracao_mms} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Corrente (A):</label>
              <input type="number" step="0.1" name="corrente_a" value={formData.corrente_a} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Fator de Potência:</label>
              <input type="number" step="0.01" name="fator_potencia" value={formData.fator_potencia} onChange={handleChange} required />
            </div>
            <button type="submit" className="btn-submit" disabled={carregando}>
              {carregando ? 'Processando IA...' : 'Analisar com IA'}
            </button>
          </form>
        </div>

        {/* CARD DE DIAGNÓSTICO (VOLTOU AO ORIGINAL) */}
        <div className="card">
          <h2>Diagnóstico do Sistema</h2>
          {resultado ? (
            <div className={`status-box ${getStatusClass(resultado.status)}`}>
              <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
                <div style={{ width: '80%' }}>
                  <GaugeChart id="gauge-chart" 
                    nrOfLevels={3} 
                    colors={["#48bb78", "#ecc94b", "#f56565"]} 
                    arcWidth={0.3} 
                    percent={resultado.risco_falha_percentagem / 100} 
                    textColor="#2d3748"
                    formatTextValue={() => `${resultado.risco_falha_percentagem}%`}
                  />
                </div>
              </div>
              <div className="result-item">
                <strong>Status de Operação:</strong> <br/>
                <span style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>{resultado.status}</span>
              </div>
              <hr />
              <div className="result-item">
                <strong>🔍 Causa Raiz Detectada:</strong> <br/>
                <span style={{ color: resultado.status.includes('NORMAL') ? '#48bb78' : '#e53e3e', fontWeight: 'bold' }}>
                  {resultado.causa_raiz}
                </span>
              </div>
              <hr />
              <div className="result-item"><strong>Recomendação Técnica:</strong> <br/> {resultado.recomendacao} </div>
              <div className="result-item"><strong>Impacto Financeiro (ROI):</strong> <br/> {resultado.roi_estimado} </div>
            </div>
          ) : (
            <div className="status-vazio">Aguardando dados para análise...</div>
          )}
        </div>
      </div>

      {/* GRÁFICO (MANTIDO NO FINAL) */}
      {historico.length > 0 && (
        <div className="card" style={{ marginTop: '30px', width: '100%' }}>
          <h2>📈 Evolução do Comportamento</h2>
          <div style={{ width: '100%', height: 300, marginTop: '20px' }}>
            <ResponsiveContainer>
              <LineChart data={historico}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hora" tick={{fontSize: 12}} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="temperatura" name="Temp °C" stroke="#e53e3e" strokeWidth={3} />
                <Line type="monotone" dataKey="vibracao" name="Vib mm/s" stroke="#3182ce" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;