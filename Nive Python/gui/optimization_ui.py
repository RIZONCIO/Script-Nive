# gui/optimization_ui.py - Interface de usuário para otimização

import tkinter as tk
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *


class OptimizationUI:
    """Classe responsável pela interface de usuário da aba de otimização"""

    def __init__(self, optimization_tab):
        """Inicializar UI da otimização"""
        self.parent = optimization_tab

    def create_optimization_tab(self, notebook):
        """Criar aba de otimização com todas as 11 opções do NiveBoost"""
        optimization_tab = ttk_bs.Frame(notebook)
        notebook.add(
            optimization_tab, text=f"{self.parent.config.get_icon('zap')} Otimização"
        )

        # Container principal com scroll
        main_container = ttk_bs.Frame(optimization_tab)
        main_container.pack(fill=BOTH, expand=True)

        # Canvas e scrollbar para scroll vertical
        canvas = tk.Canvas(main_container)
        scrollbar = ttk_bs.Scrollbar(
            main_container, orient="vertical", command=canvas.yview
        )
        scrollable_frame = ttk_bs.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Container de conteúdo
        container = ttk_bs.Frame(scrollable_frame, padding=20)
        container.pack(fill=BOTH, expand=True)

        # Título da seção
        title_label = ttk_bs.Label(
            container,
            text="NiveBoost - Ferramentas de Otimização",
            font=("Arial", 18, "bold"),
            bootstyle="primary",
        )
        title_label.pack(pady=(0, 10))

        # Versão
        version_label = ttk_bs.Label(
            container,
            text="Versão 1.1.0",
            font=("Arial", 12),
            bootstyle="secondary",
        )
        version_label.pack(pady=(0, 20))

        # Menu Principal de Otimização
        optimization_frame = ttk_bs.LabelFrame(
            container, text="Menu de Otimização", padding=15
        )
        optimization_frame.pack(fill=BOTH, expand=True, pady=(0, 20))

        # Criar botões de otimização
        self._create_optimization_buttons(optimization_frame)

        # Aviso importante
        self._create_warning_section(container)

        return optimization_tab

    def _create_optimization_buttons(self, parent_frame):
        """Criar botões de otimização"""
        # Lista das 11 opções de otimização do NiveBoost
        optimization_options = [
            (
                "🔧 Desabilitar Alguns Serviços do Windows",
                self.parent.disable_windows_services,
                "warning",
                "Desabilita serviços desnecessários para melhorar performance",
            ),
            (
                "📅 Desabilitar Tweaks de Tarefas Agendadas",
                self.parent.disable_scheduled_tasks,
                "warning",
                "Remove tarefas agendadas que consomem recursos",
            ),
            (
                "💾 Desabilitar Alguns Softwares do Windows",
                self.parent.disable_windows_software,
                "warning",
                "Desabilita aplicativos e recursos desnecessários",
            ),
            (
                "🕵️ Remover Telemetria e Coleta de Dados",
                self.parent.remove_telemetry,
                "danger",
                "Remove sistemas de coleta de dados e telemetria",
            ),
            (
                "🗑️ Remover Features Não Usadas",
                self.parent.remove_unused_features,
                "warning",
                "Remove recursos e funcionalidades não utilizadas",
            ),
            (
                "🎨 Remover Animações Inúteis",
                self.parent.remove_animations,
                "info",
                "Remove animações para melhorar a responsividade",
            ),
            (
                "🔍 Desabilitar Busca Web na Barra de Pesquisa",
                self.parent.disable_web_search,
                "info",
                "Desabilita busca online na barra de pesquisa do Windows",
            ),
            (
                "🌐 Desabilitar Cache de Navegadores e Streaming",
                self.parent.disable_browser_cache,
                "warning",
                "Otimiza cache de navegadores e serviços de streaming",
            ),
            (
                "🔒 Desabilitar Propagandas na Tela de Bloqueio",
                self.parent.disable_lock_screen_ads,
                "success",
                "Remove propagandas e sugestões da tela de bloqueio",
            ),
            (
                "🌍 Otimizar o Edge",
                self.parent.optimize_edge,
                "primary",
                "Aplica otimizações específicas para o Microsoft Edge",
            ),
            (
                "⚡Acelerar Windows",
                self.parent.accelerate_windows,
                "success",
                "Aplicação geral de otimizações para acelerar o sistema",
            ),
        ]

        # Criar botões em lista vertical
        for i, (text, command, style, description) in enumerate(optimization_options):
            # Frame para cada opção
            option_frame = ttk_bs.Frame(parent_frame)
            option_frame.pack(fill=X, pady=5)

            # Botão principal
            btn = ttk_bs.Button(
                option_frame, text=text, command=command, bootstyle=style, width=45
            )
            btn.pack(side=LEFT, padx=(0, 10))

            # Descrição
            desc_label = ttk_bs.Label(
                option_frame,
                text=description,
                font=("Arial", 9),
                bootstyle="secondary",
                wraplength=300,
            )
            desc_label.pack(side=LEFT, anchor="w")

    def _create_warning_section(self, container):
        """Criar seção de aviso"""
        warning_frame = ttk_bs.LabelFrame(
            container,
            text="⚠️ IMPORTANTE - LEIA ANTES DE USAR",
            bootstyle="danger",
            padding=15,
        )
        warning_frame.pack(fill=X, pady=(20, 0))

        warning_text = """🔴 ATENÇÃO: Estas funções são IRREVERSÍVEIS a não ser que tenha criado um ponto de restauração!

📋 RECOMENDAÇÕES OBRIGATÓRIAS:
• Crie um ponto de restauração ANTES de usar qualquer função
• Leia as informações sobre cada otimização antes de aplicar
• Não execute mais de uma otimização por vez
• Execute como Administrador para melhores resultados
• Reinicie o sistema após aplicar as otimizações

⚠️ Use por sua conta e risco. Sempre faça backup do seu sistema!"""

        warning_label = ttk_bs.Label(
            warning_frame,
            text=warning_text,
            font=("Arial", 10),
            foreground="red",
            justify="left",
        )
        warning_label.pack(anchor="w")

    def show_progress_dialog(self, title="Executando Otimização"):
        """Criar janela de progresso"""
        progress_window = tk.Toplevel(self.parent.parent.root)
        progress_window.title(title)
        progress_window.geometry("400x200")
        progress_window.transient(self.parent.parent.root)
        progress_window.grab_set()

        # Centralizar janela
        progress_window.geometry(
            "+%d+%d"
            % (
                progress_window.winfo_screenwidth() // 2 - 200,
                progress_window.winfo_screenheight() // 2 - 100,
            )
        )

        # Label de status
        status_label = ttk_bs.Label(
            progress_window, text="Executando otimizações...", font=("Arial", 12)
        )
        status_label.pack(pady=20)

        # Barra de progresso indeterminada
        progress_bar = ttk_bs.Progressbar(
            progress_window, mode="indeterminate", length=300
        )
        progress_bar.pack(pady=10)
        progress_bar.start()

        # Texto de log (scrollable)
        log_frame = ttk_bs.Frame(progress_window)
        log_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        log_text = tk.Text(log_frame, height=6, wrap=tk.WORD)
        log_scrollbar = ttk_bs.Scrollbar(
            log_frame, orient="vertical", command=log_text.yview
        )
        log_text.configure(yscrollcommand=log_scrollbar.set)

        log_scrollbar.pack(side="right", fill="y")
        log_text.pack(side="left", fill="both", expand=True)

        return progress_window, status_label, progress_bar, log_text
