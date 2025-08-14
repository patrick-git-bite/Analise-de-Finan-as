"""
Sistema Principal de Análise Financeira
Versão melhorada com arquitetura modular, tratamento de erros e funcionalidades avançadas
"""

import sys
import os
from pathlib import Path
import argparse
from typing import Optional

# Importar módulos locais
from config import CONFIG, validate_config
from utils import setup_logging, open_file_system_specific, create_backup
from data_processor import FinancialDataProcessor
from chart_generator import ChartGenerator

class FinancialAnalyzer:
    """Classe principal para análise financeira"""
    
    def __init__(self, config_override: Optional[dict] = None):
        """Inicializa o analisador financeiro"""
        # Configuração
        self.config = CONFIG.copy()
        if config_override:
            self.config.update(config_override)
        
        # Validar configuração
        validate_config()
        
        # Setup logging
        self.logger = setup_logging()
        
        # Inicializar componentes
        self.data_processor = FinancialDataProcessor(self.config)
        self.chart_generator = ChartGenerator(self.config)
        
        self.logger.info("Financial Analyzer inicializado com sucesso")
    
    def run_analysis(self, input_file: Optional[str] = None, 
                    sheet_name: Optional[str] = None,
                    output_xlsx: Optional[str] = None,
                    output_pdf: Optional[str] = None) -> bool:
        """Executa análise completa"""
        try:
            # Usar configurações padrão se não fornecidas
            input_file = input_file or self.config["input_file"]
            sheet_name = sheet_name or self.config["sheet_name"]
            output_xlsx = output_xlsx or self.config["output_xlsx"]
            output_pdf = output_pdf or self.config["output_pdf"]
            
            self.logger.info(f"Iniciando análise de {input_file}")
            
            # Criar backups se os arquivos de saída já existirem
            create_backup(output_xlsx)
            create_backup(output_pdf)
            
            # 1. Processar dados
            self.logger.info("Etapa 1: Processamento de dados")
            df = self.data_processor.process_complete_pipeline(input_file, sheet_name)
            
            if df.empty:
                raise ValueError("Nenhum dado válido encontrado após processamento")
            
            # 2. Gerar estatísticas
            self.logger.info("Etapa 2: Geração de estatísticas")
            summary_stats = self.data_processor.get_summary_statistics(df)
            self._print_summary(summary_stats)
            
            # 3. Salvar planilha Excel
            self.logger.info("Etapa 3: Salvamento da planilha Excel")
            if not self.data_processor.save_excel(df, output_xlsx):
                self.logger.warning("Falha ao salvar arquivo Excel")
            
            # 4. Gerar relatório PDF
            self.logger.info("Etapa 4: Geração do relatório PDF")
            if not self.chart_generator.generate_complete_report(df, output_pdf):
                self.logger.warning("Falha ao gerar relatório PDF")
            
            # 5. Abrir arquivos (opcional)
            self.logger.info("Etapa 5: Abertura dos arquivos gerados")
            if os.path.exists(output_xlsx):
                open_file_system_specific(output_xlsx)
            if os.path.exists(output_pdf):
                open_file_system_specific(output_pdf)
            
            self.logger.info("✅ Análise concluída com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro durante a análise: {e}")
            return False
    
    def _print_summary(self, summary_stats: dict) -> None:
        """Imprime resumo das estatísticas"""
        print("\n" + "="*60)
        print("RESUMO DA ANÁLISE FINANCEIRA")
        print("="*60)
        print(f"📊 Total de contas analisadas: {summary_stats.get('total_accounts', 0):,}")
        print(f"💰 Total 2024: R$ {summary_stats.get('total_2024', 0):,.2f}")
        print(f"💰 Total 2025: R$ {summary_stats.get('total_2025', 0):,.2f}")
        print(f"📈 Diferença total: R$ {summary_stats.get('total_difference', 0):,.2f}")
        print(f"📊 Crescimento médio: {summary_stats.get('average_growth', 0):.2f}%")
        print(f"✅ Variações positivas: {summary_stats.get('positive_variations', 0)}")
        print(f"❌ Variações negativas: {summary_stats.get('negative_variations', 0)}")
        print(f"➖ Variações estáveis: {summary_stats.get('stable_variations', 0)}")
        
        if summary_stats.get('max_growth_account'):
            print(f"🏆 Maior crescimento: {summary_stats['max_growth_account']} "
                  f"({summary_stats.get('max_growth_percentage', 0):.2f}%)")
        
        if summary_stats.get('max_decline_account'):
            print(f"⚠️  Maior declínio: {summary_stats['max_decline_account']} "
                  f"({summary_stats.get('max_decline_percentage', 0):.2f}%)")
        
        print("="*60 + "\n")
    
    def validate_input_file(self, filepath: str) -> bool:
        """Valida se o arquivo de entrada existe e é válido"""
        try:
            if not os.path.exists(filepath):
                self.logger.error(f"Arquivo não encontrado: {filepath}")
                return False
            
            # Verificar se é um arquivo Excel
            if not filepath.lower().endswith(('.xlsx', '.xls')):
                self.logger.error("Arquivo deve ser uma planilha Excel (.xlsx ou .xls)")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro na validação do arquivo: {e}")
            return False

def main():
    """Função principal com interface de linha de comando"""
    parser = argparse.ArgumentParser(
        description="Sistema de Análise Financeira Comparativa",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py                                    # Usar configurações padrão
  python main.py -i dados.xlsx -s Planilha1        # Especificar arquivo e aba
  python main.py -o relatorio.xlsx -p graficos.pdf # Especificar arquivos de saída
  python main.py --validate                        # Apenas validar arquivo de entrada
        """
    )
    
    parser.add_argument('-i', '--input', 
                       help=f'Arquivo Excel de entrada (padrão: {CONFIG["input_file"]})')
    parser.add_argument('-s', '--sheet', 
                       help=f'Nome da aba (padrão: {CONFIG["sheet_name"]})')
    parser.add_argument('-o', '--output-xlsx', 
                       help=f'Arquivo Excel de saída (padrão: {CONFIG["output_xlsx"]})')
    parser.add_argument('-p', '--output-pdf', 
                       help=f'Arquivo PDF de saída (padrão: {CONFIG["output_pdf"]})')
    parser.add_argument('--validate', action='store_true',
                       help='Apenas validar o arquivo de entrada')
    parser.add_argument('--no-open', action='store_true',
                       help='Não abrir arquivos automaticamente')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Nível de log (padrão: INFO)')
    
    args = parser.parse_args()
    
    try:
        # Configurar logging com nível especificado
        logger = setup_logging(args.log_level)
        
        # Criar instância do analisador
        config_override = {}
        if args.no_open:
            config_override['auto_open'] = False
        
        analyzer = FinancialAnalyzer(config_override)
        
        # Obter parâmetros
        input_file = args.input or CONFIG["input_file"]
        
        # Validação apenas
        if args.validate:
            if analyzer.validate_input_file(input_file):
                print(f"✅ Arquivo {input_file} é válido")
                return 0
            else:
                print(f"❌ Arquivo {input_file} não é válido")
                return 1
        
        # Executar análise completa
        success = analyzer.run_analysis(
            input_file=args.input,
            sheet_name=args.sheet,
            output_xlsx=args.output_xlsx,
            output_pdf=args.output_pdf
        )
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Operação cancelada pelo usuário")
        return 1
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())