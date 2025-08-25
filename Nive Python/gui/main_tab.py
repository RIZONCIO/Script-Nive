# gui/main_tab.py - Aba principal com tarefas mais comuns

import subprocess
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *


class MainTab:
    """Classe responsável pela aba principal com tarefas mais comuns"""

    def __init__(self, parent_interface):
        """Inicializar aba principal"""
        self.parent = parent_interface
        self.system_commands = parent_interface.system_commands
        self.config = parent_interface.config
        self.logger = parent_interface.logger

    def create_main_tab(self, notebook):
        """Criar aba principal com as tarefas mais comuns"""
        main_tab = ttk_bs.Frame(notebook)
        notebook.add(main_tab, text=f"{self.config.get_icon('home')} Principal")

        # Container para os botões
        buttons_frame = ttk_bs.Frame(main_tab, padding=10)
        buttons_frame.pack(fill=BOTH, expand=True)

        # Lista de tarefas principais
        main_tasks = [
            (
                f"{self.config.get_icon('trash')} Esvaziar Lixeira",
                self.system_commands.empty_recycle_bin,
                "success",
            ),
            (
                f"{self.config.get_icon('zap')} Ativar GodMode",
                self.system_commands.activate_godmode,
                "info",
            ),
            (
                f"{self.config.get_icon('hard_drive')} Verificar HD/SSD",
                self.system_commands.check_disk_errors,
                "warning",
            ),
            (
                f"{self.config.get_icon('cpu')} Verificar RAM",
                self.system_commands.check_ram,
                "primary",
            ),
            (
                f"{self.config.get_icon('wrench')} Reparar Sistema",
                self.system_commands.repair_system,
                "danger",
            ),
            (
                f"{self.config.get_icon('broom')} Limpar Arquivos Temporários",
                self.system_commands.clean_temp_files,
                "success",
            ),
            (
                f"{self.config.get_icon('wifi')} Limpar Cache DNS",
                self.system_commands.clean_dns_cache,
                "info",
            ),
            (
                f"{self.config.get_icon('control_panel')} Painel de Controle",
                self.open_control_panel,
                "secondary",
            ),
        ]

        # Criar botões em grid
        for i, (text, command, style) in enumerate(main_tasks):
            row = i // 2
            col = i % 2

            btn = ttk_bs.Button(
                buttons_frame, text=text, command=command, bootstyle=style, width=35
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        # Configurar colunas para expandir
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        return main_tab

    def open_control_panel(self):
        """Abrir painel de controle"""
        subprocess.Popen("control.exe")
        self.parent.update_status("Painel de Controle aberto")
