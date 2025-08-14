"""
Exemplo de uso do Sistema de Análise Financeira
Demonstra diferentes formas de utilizar o sistema
"""

from main import FinancialAnalyzer
from config import CONFIG
import pandas as pd
import os

def exemplo_uso_basico():
    """Exemplo de uso básico com configurações padrão"""
    print("=== EXEMPLO 1: USO BÁSICO ===")
    
    # Criar instância do analisador
    analyzer = FinancialAnalyzer()
    
    # Executar análise com configurações padrão
    success = analyzer.run_analysis()
    
    if success:
        print("✅ Análise básica concluída com sucesso!")
    else:
        print("❌ Erro na análise básica")

def exemplo_uso_customizado():
    """Exemplo de uso com parâmetros customizados"""
    print("\n=== EXEMPLO 2: USO CUSTOMIZADO ===")
    
    # Configurações customizadas
    config_custom = {
        "input_file": "dados_customizados.xlsx",
        "sheet_name": "Dados2025",
        "output_xlsx": "relatorio_customizado.xlsx",
        "output_pdf": "graficos_customizados.pdf",
        "chart_config": {
            "figsize": (12, 8),
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
            "title_fontsize": 16
        }
    }
    
    # Criar analisador com configuração customizada
    analyzer = FinancialAnalyzer(config_custom)
    
    # Executar análise
    success = analyzer.run_analysis(
        input_file="meus_dados.xlsx",
        sheet_name="MinhaAba",
        output_xlsx="meu_relatorio.xlsx",
        output_pdf="meus_graficos.pdf"
    )
    
    if success:
        print("✅ Análise customizada concluída!")
    else:
        print("❌ Erro na análise customizada")

def exemplo_validacao():
    """Exemplo de validação de arquivos"""
    print("\n=== EXEMPLO 3: VALIDAÇÃO DE ARQUIVOS ===")
    
    analyzer = FinancialAnalyzer()
    
    # Lista de arquivos para testar
    arquivos_teste = [
        "Pasta1.xlsx",
        "dados_inexistentes.xlsx",
        "arquivo_texto.txt"
    ]
    
    for arquivo in arquivos_teste:
        print(f"Testando: {arquivo}")
        if analyzer.validate_input_file(arquivo):
            print(f"  ✅ {arquivo} é válido")
        else:
            print(f"  ❌ {arquivo} não é válido")

def exemplo_analise_dados_simulados():
    """Exemplo criando dados simulados para teste"""
    print("\n=== EXEMPLO 4: DADOS SIMULADOS ===")
    
    # Criar dados simulados
    dados_simulados = {
        'Conta': [
            'Receita de Vendas',
            'Custos de Produtos',
            'Despesas Administrativas',
            'Despesas de Marketing',
            'Resultado Financeiro'
        ],
        'Valor_2024': [1000000, -600000, -150000, -80000, -20000],
        'Perc_2024': [100, -60, -15, -8, -2],
        'Valor_2025': [1200000, -720000, -160000, -100000, 10000],
        'Perc_2025': [100, -60, -13.3, -8.3, 0.8]
    }
    
    # Criar DataFrame
    df = pd.DataFrame(dados_simulados)
    
    # Salvar como Excel temporário
    arquivo_temp = "dados_simulados_temp.xlsx"
    df.to_excel(arquivo_temp, index=False, sheet_name="DadosSimulados")
    
    try:
        # Analisar dados simulados
        analyzer = FinancialAnalyzer()
        success = analyzer.run_analysis(
            input_file=arquivo_temp,
            sheet_name="DadosSimulados",
            output_xlsx="resultado_simulados.xlsx",
            output_pdf="graficos_simulados.pdf"
        )
        
        if success:
            print("✅ Análise de dados simulados concluída!")
        else:
            print("❌ Erro na análise de dados simulados")
            
    finally:
        # Limpar arquivo temporário
        if os.path.exists(arquivo_temp):
            os.remove(arquivo_temp)
            print(f"Arquivo temporário {arquivo_temp} removido")

def exemplo_tratamento_erros():
    """Exemplo de tratamento de erros"""
    print("\n=== EXEMPLO 5: TRATAMENTO DE ERROS ===")
    
    analyzer = FinancialAnalyzer()
    
    # Tentar analisar arquivo inexistente
    try:
        success = analyzer.run_analysis(
            input_file="arquivo_que_nao_existe.xlsx"
        )
    except Exception as e:
        print(f"Erro capturado: {e}")
    
    # Tentar analisar arquivo com formato inválido
    try:
        success = analyzer.run_analysis(
            input_file="README.md"  # Arquivo texto em vez de Excel
        )
    except Exception as e:
        print(f"Erro de formato capturado: {e}")

def exemplo_analise_multiplos_arquivos():
    """Exemplo de análise de múltiplos arquivos"""
    print("\n=== EXEMPLO 6: MÚLTIPLOS ARQUIVOS ===")
    
    arquivos = [
        ("dados_q1.xlsx", "Q1", "relatorio_q1.xlsx", "graficos_q1.pdf"),
        ("dados_q2.xlsx", "Q2", "relatorio_q2.xlsx", "graficos_q2.pdf"),
        ("dados_q3.xlsx", "Q3", "relatorio_q3.xlsx", "graficos_q3.pdf"),
        ("dados_q4.xlsx", "Q4", "relatorio_q4.xlsx", "graficos_q4.pdf")
    ]
    
    analyzer = FinancialAnalyzer()
    resultados = []
    
    for input_file, sheet, output_xlsx, output_pdf in arquivos:
        print(f"Processando: {input_file}")
        
        try:
            if analyzer.validate_input_file(input_file):
                success = analyzer.run_analysis(
                    input_file=input_file,
                    sheet_name=sheet,
                    output_xlsx=output_xlsx,
                    output_pdf=output_pdf
                )
                resultados.append((input_file, success))
            else:
                print(f"  ⚠️  Arquivo {input_file} não encontrado, pulando...")
                resultados.append((input_file, False))
                
        except Exception as e:
            print(f"  ❌ Erro ao processar {input_file}: {e}")
            resultados.append((input_file, False))
    
    # Resumo dos resultados
    print("\n📊 RESUMO DOS PROCESSAMENTOS:")
    sucessos = 0
    for arquivo, sucesso in resultados:
        status = "✅" if sucesso else "❌"
        print(f"  {status} {arquivo}")
        if sucesso:
            sucessos += 1
    
    print(f"\n📈 Total: {sucessos}/{len(arquivos)} arquivos processados com sucesso")

def main():
    """Executa todos os exemplos"""
    print("🚀 DEMONSTRAÇÃO DO SISTEMA DE ANÁLISE FINANCEIRA")
    print("=" * 60)
    
    # Executar exemplos
    try:
        # exemplo_uso_basico()  # Comentado pois precisa do arquivo original
        # exemplo_uso_customizado()  # Comentado pois precisa de arquivos específicos
        exemplo_validacao()
        exemplo_analise_dados_simulados()
        exemplo_tratamento_erros()
        # exemplo_analise_multiplos_arquivos()  # Comentado pois precisa de múltiplos arquivos
        
    except KeyboardInterrupt:
        print("\n⚠️  Demonstração interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
    
    print("\n🏁 Demonstração concluída!")
    print("Para usar o sistema, execute: python main.py")

if __name__ == "__main__":
    main()