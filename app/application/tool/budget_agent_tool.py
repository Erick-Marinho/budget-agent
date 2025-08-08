import requests
from langchain_core.tools import tool
import logging
from typing import Dict, Any, List, Optional
import json

logger = logging.getLogger(__name__)

# Configurações da API
API_BASE_URL = "https://homolog.doutorsofa.franchisefactory.com.br"
API_ENDPOINT = "/index.php/api/atendimento/busca_tabela_precos_franquia"
AUTHORIZATION_TOKEN = "02a283a5-6170-492f-9d00-461baa5f01eb"
DEFAULT_FRANCHISE_ID = 1

@tool
def get_budget_info(query: str) -> str:
    """
    Busca informações sobre serviços e preços da franquia Dr. Sofá.
    
    Args:
        query: Consulta sobre serviços (ex: "sofá 2 lugares", "limpeza colchão", "impermeabilização")
    
    Returns:
        String com informações dos serviços encontrados e seus preços
    """
    
    logger.info(f"Buscando informações sobre orçamentos para a consulta: {query}")
    
    try:
        # Buscar dados da API
        services_data = _fetch_franchise_services()
        
        if not services_data:
            return "Erro ao buscar informações dos serviços. Tente novamente."
        
        # Filtrar serviços baseado na consulta
        filtered_services = _filter_services_by_query(services_data, query)
        
        if not filtered_services:
            return f"Nenhum serviço encontrado para '{query}'. Tente termos como: sofá, colchão, poltrona, limpeza, impermeabilização."
        
        # Formatar resposta
        return _format_services_response(filtered_services, query)
        
    except Exception as e:
        logger.error(f"Erro ao buscar informações de orçamento: {str(e)}")
        return f"Erro interno ao buscar informações: {str(e)}"


def _fetch_franchise_services() -> Optional[List[Dict[str, Any]]]:
    """Busca dados dos serviços da franquia na API"""
    
    url = f"{API_BASE_URL}{API_ENDPOINT}"
    headers = {
        "Authorization": AUTHORIZATION_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {"franquia_id": DEFAULT_FRANCHISE_ID}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("success") and data.get("code") == 200:
            return data.get("data", [])
        else:
            logger.error(f"API retornou erro: {data.get('message', 'Erro desconhecido')}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição para API: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar resposta JSON: {str(e)}")
        return None


def _filter_services_by_query(services: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Filtra serviços baseado na consulta do usuário"""
    
    query_lower = query.lower()
    filtered = []
    
    for service in services:
        service_name = service.get("servico_nome", "").lower()
        
        # Busca por palavras-chave na consulta
        if any(word in service_name for word in query_lower.split()):
            filtered.append(service)
    
    # Se não encontrou nada, tenta busca mais ampla
    if not filtered:
        for service in services:
            service_name = service.get("servico_nome", "").lower()
            if query_lower in service_name:
                filtered.append(service)
    
    return filtered


def _format_services_response(services: List[Dict[str, Any]], query: str) -> str:
    """Formata a resposta com os serviços encontrados"""
    
    response_lines = [f"📋 Serviços encontrados para '{query}':\n"]
    
    for service in services:
        service_name = service.get("servico_nome", "N/A")
        valor_padrao = service.get("valor_padrao_franquia", 0)
        valor_minimo = service.get("valor_minimo_franquia", 0)
        categoria_id = service.get("servicoscategoria_id", 0)
        
        # Determinar tipo de serviço baseado na categoria
        tipo_servico = "Limpeza" if categoria_id == 2 else "Impermeabilização" if categoria_id == 3 else "Outro"
        
        response_lines.append(
            f"🔹 {service_name}\n"
            f"   💰 Valor padrão: R$ {valor_padrao:.2f}\n"
            f"   💸 Valor mínimo: R$ {valor_minimo:.2f}\n"
            f"   🏷️ Categoria: {tipo_servico}\n"
        )
    
    response_lines.append(f"\n✅ Total de {len(services)} serviço(s) encontrado(s)")
    
    return "".join(response_lines)
    
    