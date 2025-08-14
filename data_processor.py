"""
Módulo responsável pelo processamento de dados financeiros
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from utils import validate_file_exists, validate_dataframe, format_currency, format_percentage

class FinancialDataProcessor:
    """Classe para processamento de dados financeiros"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.df: Optional[pd.DataFrame] = None
        
    def load_data(self, filepath: str, sheet_name: str) -> pd.DataFrame:
        """Carrega dados do arquivo Excel"""
        try:
            validate_file_exists(filepath)
            
            self.logger.info(f"Carregando dados de: {filepath}, aba: {sheet_name}")
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            
            if df.empty:
                raise ValueError("Planilha está vazia")
                
            self.logger.info(f"Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
            return df
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpa e prepara os dados"""
        try:
            self.logger.info("Iniciando limpeza dos dados...")
            
            # Remover linhas completamente vazias
            df_clean = df.dropna(how="all").copy()
            
            # Renomear colunas
            if len(df_clean.columns) >= len(self.config["column_names"]):
                df_clean.columns = self.config["column_names"] + list(df_clean.columns[len(self.config["column_names"]):])
            
            # Converter colunas de valor para numérico
            for col in self.config["value_columns"]:
                if col in df_clean.columns:
                    # Remover símbolos de moeda e converter para float
                    df_clean[col] = pd.to_numeric(
                        df_clean[col].astype(str).str.replace('[R$.,\s]', '', regex=True),
                        errors='coerce'
                    )
            
            # Remover linhas com valores não numéricos nas colunas principais
            for col in self.config["value_columns"]:
                if col in df_clean.columns:
                    df_clean = df_clean[df_clean[col].notna()]
            
            # Remover linhas onde todos os valores são zero
            value_cols = [col for col in self.config["value_columns"] if col in df_clean.columns]
            df_clean = df_clean[~(df_clean[value_cols] == 0).all(axis=1)]
            
            self.logger.info(f"Limpeza concluída: {len(df_clean)} linhas restantes")
            return df_clean
            
        except Exception as e:
            self.logger.error(f"Erro na limpeza dos dados: {e}")
            raise
    
    def calculate_differences(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula diferenças entre os anos"""
        try:
            self.logger.info("Calculando diferenças...")
            
            df_calc = df.copy()
            
            # Calcular diferença em valores absolutos
            df_calc["Diferença_R$"] = df_calc["Valor_2025"] - df_calc["Valor_2024"]
            
            # Calcular diferença percentual (evitar divisão por zero)
            df_calc["Diferença_%"] = np.where(
                df_calc["Valor_2024"] != 0,
                ((df_calc["Diferença_R$"]) / df_calc["Valor_2024"]) * 100,
                0
            )
            
            # Adicionar classificação da variação
            df_calc["Classificação"] = df_calc["Diferença_%"].apply(self._classify_variation)
            
            # Adicionar colunas formatadas para exibição
            df_calc["Valor_2024_Formatado"] = df_calc["Valor_2024"].apply(format_currency)
            df_calc["Valor_2025_Formatado"] = df_calc["Valor_2025"].apply(format_currency)
            df_calc["Diferença_R$_Formatado"] = df_calc["Diferença_R$"].apply(format_currency)
            df_calc["Diferença_%_Formatado"] = df_calc["Diferença_%"].apply(format_percentage)
            
            self.logger.info("Cálculos concluídos com sucesso")
            return df_calc
            
        except Exception as e:
            self.logger.error(f"Erro no cálculo das diferenças: {e}")
            raise
    
    def _classify_variation(self, percentage: float) -> str:
        """Classifica a variação percentual"""
        if percentage > 20:
            return "Alto Crescimento"
        elif percentage > 5:
            return "Crescimento Moderado"
        elif percentage > -5:
            return "Estável"
        elif percentage > -20:
            return "Declínio Moderado"
        else:
            return "Alto Declínio"
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict:
        """Gera estatísticas resumidas dos dados"""
        try:
            summary = {
                "total_accounts": len(df),
                "total_2024": df["Valor_2024"].sum(),
                "total_2025": df["Valor_2025"].sum(),
                "total_difference": df["Diferença_R$"].sum(),
                "average_growth": df["Diferença_%"].mean(),
                "positive_variations": len(df[df["Diferença_R$"] > 0]),
                "negative_variations": len(df[df["Diferença_R$"] < 0]),
                "stable_variations": len(df[df["Diferença_R$"] == 0]),
                "max_growth_account": df.loc[df["Diferença_%"].idxmax(), "Conta"] if not df.empty else "",
                "max_growth_percentage": df["Diferença_%"].max(),
                "max_decline_account": df.loc[df["Diferença_%"].idxmin(), "Conta"] if not df.empty else "",
                "max_decline_percentage": df["Diferença_%"].min()
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular estatísticas: {e}")
            return {}
    
    def save_excel(self, df: pd.DataFrame, filepath: str) -> bool:
        """Salva DataFrame em arquivo Excel"""
        try:
            # Criar múltiplas abas
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Aba principal com dados completos
                df.to_excel(writer, sheet_name='Dados_Completos', index=False)
                
                # Aba com resumo estatístico
                summary = self.get_summary_statistics(df)
                summary_df = pd.DataFrame(list(summary.items()), columns=['Métrica', 'Valor'])
                summary_df.to_excel(writer, sheet_name='Resumo', index=False)
                
                # Aba com top variações positivas
                top_positive = df.nlargest(10, 'Diferença_%')[['Conta', 'Valor_2024_Formatado', 'Valor_2025_Formatado', 'Diferença_%_Formatado']]
                top_positive.to_excel(writer, sheet_name='Top_Crescimento', index=False)
                
                # Aba com top variações negativas
                top_negative = df.nsmallest(10, 'Diferença_%')[['Conta', 'Valor_2024_Formatado', 'Valor_2025_Formatado', 'Diferença_%_Formatado']]
                top_negative.to_excel(writer, sheet_name='Top_Declinio', index=False)
            
            self.logger.info(f"Arquivo Excel salvo: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar Excel: {e}")
            return False
    
    def process_complete_pipeline(self, input_file: str, sheet_name: str) -> pd.DataFrame:
        """Executa o pipeline completo de processamento"""
        try:
            # Carregar dados
            raw_data = self.load_data(input_file, sheet_name)
            
            # Limpar dados
            clean_data = self.clean_data(raw_data)
            
            # Calcular diferenças
            processed_data = self.calculate_differences(clean_data)
            
            # Armazenar resultado
            self.df = processed_data
            
            self.logger.info("Pipeline de processamento concluído com sucesso")
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Erro no pipeline de processamento: {e}")
            raise