import os
import tkinter as tk
from datetime import datetime
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *


class BaseInterface:
    """Classe base para a interface principal do ScriptNive"""

    def __init__(self, root, system_commands, logger, config):
        """Inicializar interface base"""
        self.root = root
        self.system_commands = system_commands
        self.logger = logger
        self.config = config

        # Status da aplicação
        self.status_var = tk.StringVar(value="Pronto")

        # Referências para widgets importantes
        self.notebook = None
        self.status_label = None
        self.progress = None
        self.log_text = None

        # Configurar logger para usar o widget de texto (será definido em tools_tab)
        # self.logger.set_widget(self.log_text)  # Movido para depois da criação das abas

    def setup_base_widgets(self):
        """Criar estrutura básica da interface"""
        # Frame principal
        main_frame = ttk_bs.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # Cabeçalho
        self.create_header(main_frame)

        # Notebook para organizar as abas
        self.notebook = ttk_bs.Notebook(main_frame)
        self.notebook.pack(fill=BOTH, expand=True, pady=(10, 0))

        # Barra de status
        self.create_status_bar(main_frame)

        return main_frame

    def create_header(self, parent):
        """Criar cabeçalho com informações do sistema"""
        header_frame = ttk_bs.Frame(parent)
        header_frame.pack(fill=X, pady=(0, 10))

        # Título principal
        title_label = ttk_bs.Label(
            header_frame,
            text=f"ScriptNive {self.config.version}",
            font=("Arial", 20, "bold"),
            bootstyle="info",
        )
        title_label.pack()

        # Subtítulo
        subtitle_label = ttk_bs.Label(
            header_frame,
            text="Ferramenta Completa de Manutenção do Windows",
            font=("Arial", 10),
            bootstyle="secondary",
        )
        subtitle_label.pack()

        # Informações do sistema
        info_frame = ttk_bs.Frame(header_frame)
        info_frame.pack(fill=X, pady=(5, 0))

        try:
            computer_name = os.environ.get("COMPUTERNAME", "N/A")
            username = os.environ.get("USERNAME", "N/A")
            now = datetime.now()

            info_text = (
                f"Computador: {computer_name} | Usuário: {username} | "
                f"Data: {now.strftime('%d/%m/%Y %H:%M')}"
            )

            info_label = ttk_bs.Label(
                info_frame, text=info_text, font=("Arial", 9), bootstyle="light"
            )
            info_label.pack()
        except Exception:
            pass

    def create_status_bar(self, parent):
        """Criar barra de status"""
        status_frame = ttk_bs.Frame(parent)
        status_frame.pack(fill=X, side=BOTTOM, pady=(10, 0))

        self.status_label = ttk_bs.Label(
            status_frame, textvariable=self.status_var, bootstyle="secondary"
        )
        self.status_label.pack(side=LEFT)

        # Barra de progresso
        self.progress = ttk_bs.Progressbar(
            status_frame, mode="indeterminate", bootstyle="info"
        )
        self.progress.pack(side=RIGHT, padx=(10, 0))

    def update_status(self, message):
        """Atualizar mensagem de status"""
        self.status_var.set(message)
        self.logger.log(message)
        self.root.update_idletasks()

    def log_activity(self, message):
        """Registrar atividade no log"""
        if hasattr(self, "logger") and self.logger:
            self.logger.log(message)
