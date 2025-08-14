"""
Módulo responsável pela geração de gráficos e relatórios visuais
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import seaborn as sns
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

class ChartGenerator:
    """Classe para geração de gráficos financeiros"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.chart_config = config.get("chart_config", {})
        self.logger = logging.getLogger(__name__)
        
        # Configurar estilo dos gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette(self.chart_config.get("colors", ["#2E86AB", "#A23B72", "#F18F01"]))
    
    def create_comparison_chart(self, data: pd.Series, title: str) -> plt.Figure:
        """Cria gráfico de comparação individual"""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.chart_config.get("figsize", (12, 6)))
            
            # Gráfico de barras
            categories = ["2024", "2025"]
            values = [data["Valor_2024"], data["Valor_2025"]]
            colors = self.chart_config.get("colors", ["#2E86AB", "#A23B72"])[:2]
            
            bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
            ax1.set_title(f"{data['Conta']}", fontsize=self.chart_config.get("title_fontsize", 14), pad=20)
            ax1.set_ylabel("Valor (R$)", fontsize=self.chart_config.get("label_fontsize", 12))
            ax1.grid(axis="y", linestyle="--", alpha=self.chart_config.get("grid_alpha", 0.3))
            
            # Adicionar valores nas barras
            for bar, value in zip(bars, values):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                        f'R$ {value:,.2f}', ha='center', va='bottom', fontweight='bold')
            
            # Gráfico de pizza da variação
            if data["Diferença_R$"] != 0:
                sizes = [abs(data["Valor_2024"]), abs(data["Diferença_R$"])]
                labels = ["Base 2024", f"Variação ({data['Diferença_%']:.1f}%)"]
                colors_pie = [colors[0], colors[1] if data["Diferença_R$"] > 0 else '#FF6B6B']
                
                wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie, 
                                                  autopct='%1.1f%%', startangle=90)
                ax2.set_title("Composição da Variação", fontsize=self.chart_config.get("title_fontsize", 14))
            else:
                ax2.text(0.5, 0.5, 'Sem Variação', transform=ax2.transAxes, 
                        ha='center', va='center', fontsize=16)
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
            
            # Adicionar informações adicionais
            info_text = f"Diferença: R$ {data['Diferença_R$']:,.2f}\nVariação: {data['Diferença_%']:.2f}%\nClassificação: {data['Classificação']}"
            fig.text(0.02, 0.02, info_text, fontsize=10, 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            self.logger.error(f"Erro ao criar gráfico de comparação: {e}")
            raise
    
    def create_overview_chart(self, df: pd.DataFrame) -> plt.Figure:
        """Cria gráfico geral de overview"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # 1. Gráfico de barras - Top 10 contas por valor 2025
            top_accounts = df.nlargest(10, 'Valor_2025')
            ax1.barh(top_accounts['Conta'], top_accounts['Valor_2025'], color=self.chart_config.get("colors", ["#2E86AB"])[0])
            ax1.set_title('Top 10 Contas por Valor (2025)', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Valor (R$)')
            ax1.grid(axis='x', alpha=0.3)
            
            # 2. Histograma de variações percentuais
            ax2.hist(df['Diferença_%'], bins=20, color=self.chart_config.get("colors", ["#A23B72"])[1], 
                    alpha=0.7, edgecolor='black')
            ax2.set_title('Distribuição das Variações (%)', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Variação (%)')
            ax2.set_ylabel('Frequência')
            ax2.grid(axis='y', alpha=0.3)
            
            # 3. Scatter plot - Valor 2024 vs 2025
            scatter = ax3.scatter(df['Valor_2024'], df['Valor_2025'], 
                                c=df['Diferença_%'], cmap='RdYlGn', alpha=0.7, s=60)
            ax3.plot([df['Valor_2024'].min(), df['Valor_2024'].max()], 
                    [df['Valor_2024'].min(), df['Valor_2024'].max()], 'r--', alpha=0.5)
            ax3.set_title('Comparação 2024 vs 2025', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Valor 2024 (R$)')
            ax3.set_ylabel('Valor 2025 (R$)')
            ax3.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax3, label='Variação (%)')
            
            # 4. Gráfico de pizza - Classificações
            classification_counts = df['Classificação'].value_counts()
            colors_pie = plt.cm.Set3(np.linspace(0, 1, len(classification_counts)))
            ax4.pie(classification_counts.values, labels=classification_counts.index, 
                   autopct='%1.1f%%', colors=colors_pie, startangle=90)
            ax4.set_title('Distribuição por Classificação', fontsize=14, fontweight='bold')
            
            plt.suptitle('Análise Comparativa 2024-2025 - Visão Geral', fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Erro ao criar gráfico de overview: {e}")
            raise
    
    def create_trend_analysis(self, df: pd.DataFrame) -> plt.Figure:
        """Cria análise de tendências"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            
            # 1. Top crescimentos
            top_growth = df.nlargest(10, 'Diferença_%')
            bars1 = ax1.bar(range(len(top_growth)), top_growth['Diferença_%'], 
                           color='green', alpha=0.7)
            ax1.set_title('Top 10 Maiores Crescimentos (%)', fontweight='bold')
            ax1.set_ylabel('Variação (%)')
            ax1.set_xticks(range(len(top_growth)))
            ax1.set_xticklabels(top_growth['Conta'], rotation=45, ha='right')
            ax1.grid(axis='y', alpha=0.3)
            
            # Adicionar valores nas barras
            for bar, value in zip(bars1, top_growth['Diferença_%']):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            # 2. Top declínios
            top_decline = df.nsmallest(10, 'Diferença_%')
            bars2 = ax2.bar(range(len(top_decline)), top_decline['Diferença_%'], 
                           color='red', alpha=0.7)
            ax2.set_title('Top 10 Maiores Declínios (%)', fontweight='bold')
            ax2.set_ylabel('Variação (%)')
            ax2.set_xticks(range(len(top_decline)))
            ax2.set_xticklabels(top_decline['Conta'], rotation=45, ha='right')
            ax2.grid(axis='y', alpha=0.3)
            
            # Adicionar valores nas barras
            for bar, value in zip(bars2, top_decline['Diferença_%']):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 1,
                        f'{value:.1f}%', ha='center', va='top', fontweight='bold')
            
            # 3. Análise de correlação valor vs variação
            ax3.scatter(df['Valor_2024'], df['Diferença_%'], alpha=0.6, color='blue')
            ax3.set_title('Correlação: Valor Base vs Variação', fontweight='bold')
            ax3.set_xlabel('Valor 2024 (R$)')
            ax3.set_ylabel('Variação (%)')
            ax3.grid(True, alpha=0.3)
            
            # Linha de tendência
            z = np.polyfit(df['Valor_2024'], df['Diferença_%'], 1)
            p = np.poly1d(z)
            ax3.plot(df['Valor_2024'], p(df['Valor_2024']), "r--", alpha=0.8)
            
            # 4. Box plot por classificação
            classifications = df['Classificação'].unique()
            box_data = [df[df['Classificação'] == cls]['Diferença_%'].values for cls in classifications]
            bp = ax4.boxplot(box_data, labels=classifications, patch_artist=True)
            ax4.set_title('Distribuição de Variações por Classificação', fontweight='bold')
            ax4.set_ylabel('Variação (%)')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(axis='y', alpha=0.3)
            
            # Colorir os box plots
            colors = plt.cm.Set2(np.linspace(0, 1, len(bp['boxes'])))
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            plt.suptitle('Análise de Tendências e Correlações', fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Erro ao criar análise de tendências: {e}")
            raise
    
    def generate_complete_report(self, df: pd.DataFrame, output_file: str) -> bool:
        """Gera relatório completo em PDF"""
        try:
            self.logger.info(f"Gerando relatório PDF: {output_file}")
            
            with PdfPages(output_file) as pdf:
                # Página 1: Overview geral
                overview_fig = self.create_overview_chart(df)
                pdf.savefig(overview_fig, bbox_inches='tight', dpi=300)
                plt.close(overview_fig)
                
                # Página 2: Análise de tendências
                trend_fig = self.create_trend_analysis(df)
                pdf.savefig(trend_fig, bbox_inches='tight', dpi=300)
                plt.close(trend_fig)
                
                # Páginas individuais para cada conta (limitado a top 20 por performance)
                top_accounts = df.nlargest(20, 'Valor_2025')
                
                for _, account_data in top_accounts.iterrows():
                    try:
                        account_fig = self.create_comparison_chart(account_data, account_data['Conta'])
                        pdf.savefig(account_fig, bbox_inches='tight', dpi=200)
                        plt.close(account_fig)
                    except Exception as e:
                        self.logger.warning(f"Erro ao gerar gráfico para conta {account_data['Conta']}: {e}")
                        continue
                
                # Adicionar metadados ao PDF
                pdf_info = pdf.infodict()
                pdf_info['Title'] = 'Relatório Comparativo Financeiro 2024-2025'
                pdf_info['Author'] = 'Sistema de Análise Financeira'
                pdf_info['Subject'] = 'Análise comparativa de contas financeiras'
                pdf_info['Creator'] = 'Financial Data Analyzer v2.0'
            
            self.logger.info(f"Relatório PDF gerado com sucesso: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório PDF: {e}")
            return False
    
    def create_summary_chart(self, summary_stats: Dict) -> plt.Figure:
        """Cria gráfico resumo com estatísticas principais"""
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
            
            # 1. Comparação de totais
            totals = [summary_stats['total_2024'], summary_stats['total_2025']]
            ax1.bar(['2024', '2025'], totals, color=self.chart_config.get("colors", ["#2E86AB", "#A23B72"])[:2])
            ax1.set_title('Total Geral por Ano', fontweight='bold')
            ax1.set_ylabel('Valor Total (R$)')
            for i, v in enumerate(totals):
                ax1.text(i, v + max(totals)*0.01, f'R$ {v:,.0f}', ha='center', va='bottom', fontweight='bold')
            
            # 2. Distribuição de variações
            variations = [summary_stats['positive_variations'], 
                         summary_stats['negative_variations'], 
                         summary_stats['stable_variations']]
            labels = ['Positivas', 'Negativas', 'Estáveis']
            colors = ['green', 'red', 'gray']
            ax2.pie(variations, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Distribuição de Variações', fontweight='bold')
            
            # 3. Extremos
            extremes = ['Maior Crescimento', 'Maior Declínio']
            extreme_values = [summary_stats['max_growth_percentage'], summary_stats['max_decline_percentage']]
            colors_extreme = ['green' if v > 0 else 'red' for v in extreme_values]
            bars = ax3.bar(extremes, extreme_values, color=colors_extreme, alpha=0.7)
            ax3.set_title('Variações Extremas', fontweight='bold')
            ax3.set_ylabel('Variação (%)')
            ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            
            # Adicionar valores e nomes das contas
            for bar, value, account in zip(bars, extreme_values, 
                                         [summary_stats['max_growth_account'], summary_stats['max_decline_account']]):
                ax3.text(bar.get_x() + bar.get_width()/2, 
                        value + (5 if value > 0 else -5),
                        f'{value:.1f}%\n{account[:15]}...', 
                        ha='center', va='bottom' if value > 0 else 'top', 
                        fontweight='bold', fontsize=9)
            
            # 4. Métricas resumidas
            ax4.axis('off')
            metrics_text = f"""
            RESUMO EXECUTIVO
            
            Total de Contas Analisadas: {summary_stats['total_accounts']:,}
            
            Crescimento Médio: {summary_stats['average_growth']:.2f}%
            
            Variação Total: R$ {summary_stats['total_difference']:,.2f}
            
            Contas em Crescimento: {summary_stats['positive_variations']} 
            ({(summary_stats['positive_variations']/summary_stats['total_accounts']*100):.1f}%)
            
            Contas em Declínio: {summary_stats['negative_variations']} 
            ({(summary_stats['negative_variations']/summary_stats['total_accounts']*100):.1f}%)
            
            Melhor Performance: 
            {summary_stats['max_growth_account']} 
            ({summary_stats['max_growth_percentage']:.2f}%)
            
            Pior Performance: 
            {summary_stats['max_decline_account']} 
            ({summary_stats['max_decline_percentage']:.2f}%)
            """
            
            ax4.text(0.05, 0.95, metrics_text, transform=ax4.transAxes, 
                    fontsize=12, verticalalignment='top', fontfamily='monospace',
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
            
            plt.suptitle('Resumo Executivo - Análise Comparativa 2024-2025', 
                        fontsize=16, fontweight='bold', y=0.98)
            plt.tight_layout()
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Erro ao criar gráfico resumo: {e}")
            raise