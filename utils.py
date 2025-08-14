"""
Utilitários gerais para o sistema de análise financeira
"""

import os
import platform
import logging
from typing import Optional, Union
import pandas as pd

# === CONFIGURAÇÃO DE LOGGING ===
def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('financial_analysis.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# === VALIDAÇÕES ===
def validate_file_exists(filepath: str) -> bool:
    """Verifica se o arquivo existe"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    return True

def validate_dataframe(df: pd.DataFrame, required_columns: list) -> bool:
    """Valida se o DataFrame possui as colunas necessárias"""
    if df.empty:
        raise ValueError("DataFrame está vazio")
    
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Colunas faltando no DataFrame: {missing_columns}")
    
    return True

# === FORMATAÇÃO ===
def format_currency(value: Union[float, int], symbol: str = "R$") -> str:
    """Formata valor como moeda"""
    try:
        return f"{symbol} {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return f"{symbol} 0,00"

def format_percentage(value: Union[float, int]) -> str:
    """Formata valor como percentual"""
    try:
        return f"{value:.2f}%"
    except (ValueError, TypeError):
        return "0,00%"

# === SISTEMA OPERACIONAL ===
def open_file_system_specific(filepath: str) -> None:
    """Abre arquivo de acordo com o sistema operacional"""
    system = platform.system().lower()
    
    try:
        if system == "windows":
            os.startfile(filepath)
        elif system == "darwin":  # macOS
            os.system(f"open '{filepath}'")
        elif system == "linux":
            os.system(f"xdg-open '{filepath}'")
        else:
            logging.warning(f"Sistema operacional {system} não suportado para abertura automática")
    except Exception as e:
        logging.error(f"Erro ao abrir arquivo {filepath}: {e}")

# === BACKUP ===
def create_backup(filepath: str) -> Optional[str]:
    """Cria backup de um arquivo existente"""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.backup"
        try:
            import shutil
            shutil.copy2(filepath, backup_path)
            logging.info(f"Backup criado: {backup_path}")
            return backup_path
        except Exception as e:
            logging.error(f"Erro ao criar backup: {e}")
            return None
    return None