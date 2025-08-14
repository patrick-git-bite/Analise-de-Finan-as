"""
Configurações do sistema de análise financeira
"""

import os
from typing import Dict, Any

# === CONFIGURAÇÕES DO ARQUIVO ===
CONFIG: Dict[str, Any] = {
    # Arquivos de entrada
    "input_file": "Pasta1.xlsx",
    "sheet_name": "Plan1",
    
    # Arquivos de saída
    "output_xlsx": "comparativo.xlsx",
    "output_pdf": "comparativo.pdf",
    
    # Configurações de colunas
    "column_names": ["Conta", "Valor_2024", "Perc_2024", "Valor_2025", "Perc_2025"],
    "value_columns": ["Valor_2024", "Valor_2025"],
    
    # Configurações de gráfico
    "chart_config": {
        "figsize": (10, 6),
        "colors": ["#2E86AB", "#A23B72", "#F18F01"],
        "grid_alpha": 0.3,
        "title_fontsize": 14,
        "label_fontsize": 12
    },
    
    # Configurações de formato
    "number_format": {
        "decimal_places": 2,
        "currency_symbol": "R$",
        "thousands_separator": "."
    }
}

# === VALIDAÇÕES ===
def validate_config() -> bool:
    """Valida se as configurações estão corretas"""
    required_keys = ["input_file", "sheet_name", "output_xlsx", "output_pdf"]
    
    for key in required_keys:
        if not CONFIG.get(key):
            raise ValueError(f"Configuração obrigatória '{key}' não encontrada")
    
    return True

# === CAMINHOS ===
def get_file_path(filename: str) -> str:
    """Retorna o caminho completo do arquivo"""
    return os.path.join(os.getcwd(), filename)