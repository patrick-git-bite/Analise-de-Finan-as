# Sistema de Análise Financeira Comparativa

Sistema modular e robusto para análise comparativa de dados financeiros entre dois períodos, com geração automática de relatórios em Excel e PDF.

## 🚀 Características Principais

- **Arquitetura Modular**: Código organizado em módulos especializados
- **Tratamento de Erros**: Validações robustas e logging detalhado
- **Relatórios Avançados**: Gráficos interativos e análises estatísticas
- **Multi-plataforma**: Funciona em Windows, macOS e Linux
- **Interface CLI**: Linha de comando com múltiplas opções
- **Backup Automático**: Proteção de dados existentes

## 📋 Funcionalidades

### Processamento de Dados
- ✅ Limpeza automática de dados
- ✅ Validação de integridade
- ✅ Cálculos de diferenças absolutas e percentuais
- ✅ Classificação automática de variações
- ✅ Estatísticas resumidas

### Geração de Relatórios
- ✅ Planilha Excel com múltiplas abas
- ✅ Relatório PDF com gráficos avançados
- ✅ Visão geral e análise de tendências
- ✅ Gráficos individuais por conta
- ✅ Análise de correlações

### Visualizações
- 📊 Gráficos de barras comparativos
- 📈 Análise de tendências
- 🥧 Gráficos de pizza
- 📦 Box plots por classificação
- 🔍 Scatter plots de correlação

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes)

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

### Dependências Principais
- pandas: Processamento de dados
- matplotlib: Geração de gráficos
- seaborn: Visualizações estatísticas
- openpyxl: Manipulação de arquivos Excel

## 📖 Como Usar

### Uso Básico
```bash
python main.py
```

### Opções Avançadas
```bash
# Especificar arquivo de entrada e aba
python main.py -i meus_dados.xlsx -s MinhaAba

# Definir arquivos de saída
python main.py -o relatorio_custom.xlsx -p graficos_custom.pdf

# Apenas validar arquivo
python main.py --validate -i dados.xlsx

# Não abrir arquivos automaticamente
python main.py --no-open

# Definir nível de log
python main.py --log-level DEBUG
```

### Parâmetros Disponíveis
- `-i, --input`: Arquivo Excel de entrada
- `-s, --sheet`: Nome da aba
- `-o, --output-xlsx`: Arquivo Excel de saída
- `-p, --output-pdf`: Arquivo PDF de saída
- `--validate`: Apenas validar entrada
- `--no-open`: Não abrir arquivos automaticamente
- `--log-level`: Nível de log (DEBUG/INFO/WARNING/ERROR)

## 📁 Estrutura do Projeto

```
sistema-analise-financeira/
├── main.py              # Arquivo principal
├── config.py            # Configurações do sistema
├── data_processor.py    # Processamento de dados
├── chart_generator.py   # Geração de gráficos
├── utils.py             # Utilitários gerais
├── requirements.txt     # Dependências
├── README.md           # Documentação
└── logs/               # Arquivos de log
```

## ⚙️ Configuração

Edite o arquivo `config.py` para personalizar:

```python
CONFIG = {
    "input_file": "Pasta1.xlsx",
    "sheet_name": "Plan1",
    "output_xlsx": "comparativo.xlsx",
    "output_pdf": "comparativo.pdf",
    # ... outras configurações
}
```

## 📊 Formato dos Dados de Entrada

O arquivo Excel deve conter as seguintes colunas:
- **Coluna A**: Nome da conta
- **Coluna B**: Valor 2024
- **Coluna C**: Percentual 2024 (opcional)
- **Coluna D**: Valor 2025
- **Coluna E**: Percentual 2025 (opcional)

## 📈 Relatórios Gerados

### Arquivo Excel (`comparativo.xlsx`)
- **Dados_Completos**: Dados processados com cálculos
- **Resumo**: Estatísticas gerais
- **Top_Crescimento**: Maiores crescimentos
- **Top_Declinio**: Maiores declínios

### Arquivo PDF (`comparativo.pdf`)
- **Página 1**: Visão geral com múltiplos gráficos
- **Página 2**: Análise de tendências e correlações
- **Páginas 3+**: Gráficos individuais por conta

## 🔧 Personalização

### Cores dos Gráficos
```python
"chart_config": {
    "colors": ["#2E86AB", "#A23B72", "#F18F01"],
    "figsize": (10, 6),
}
```

### Classificações de Variação
- **Alto Crescimento**: > 20%
- **Crescimento Moderado**: 5% a 20%
- **Estável**: -5% a 5%
- **Declínio Moderado**: -20% a -5%
- **Alto Declínio**: < -20%

## 📝 Log e Depuração

O sistema gera logs detalhados em:
- Console (saída padrão)
- Arquivo `financial_analysis.log`

Níveis de log disponíveis:
- **DEBUG**: Informações detalhadas
- **INFO**: Progresso normal (padrão)
- **WARNING**: Avisos não críticos
- **ERROR**: Erros críticos

## 🚨 Tratamento de Erros

- ✅ Validação de arquivos de entrada
- ✅ Verificação de integridade dos dados
- ✅ Backup automático de arquivos existentes
- ✅ Logging detalhado de erros
- ✅ Recuperação graceful de falhas

## 🔄 Backup Automático

O sistema automaticamente:
- Cria backup de arquivos existentes (`.backup`)
- Preserva dados anteriores antes de sobrescrever
- Registra operações de backup no log

## 🆘 Solução de Problemas

### Arquivo não encontrado
```bash
python main.py --validate -i seu_arquivo.xlsx
```

### Problemas de encoding
Certifique-se de que o arquivo Excel está em formato válido (xlsx/xls)

### Erro de memória
Para arquivos muito grandes, considere processar em lotes menores

### Gráficos não aparecem
Verifique se todas as dependências de matplotlib estão instaladas

## 📞 Suporte

Para problemas ou sugestões:
1. Verifique os logs em `financial_analysis.log`
2. Execute com `--log-level DEBUG` para mais detalhes
3. Valide o arquivo de entrada com `--validate`

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:
1. Fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📈 Versioning

- **v1.0**: Versão original (monolítica)
- **v2.0**: Arquitetura modular atual

---

**Sistema de Análise Financeira v2.0** - Desenvolvido para análise profissional de dados financeiros