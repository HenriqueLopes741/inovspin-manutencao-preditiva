def calcular_roi(risco: float) -> str:
    custo_manutencao_preventiva = 500
    custo_falha_catastrofica = 15000
    
    if risco > 70:
        economia = custo_falha_catastrofica - custo_manutencao_preventiva
        return f"Ação imediata pode poupar até R$ {economia},00 em custos corretivos."
    return "Equipamento a operar dentro dos parâmetros normais. Não há custos iminentes."

def determinar_status(risco: float) -> tuple:
    if risco > 70:
        return "🔴 CRÍTICO", "Manutenção recomendada em menos de 24h!"
    elif risco > 40:
        return "🟡 ATENÇÃO", "Agendar inspeção para os próximos 7 dias."
    else:
        return "🟢 NORMAL", "Continuar monitorização padrão."