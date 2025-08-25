# gui/tools_tab.py - Aba de ferramentas e diagnóstico

import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
from core.system_info import get_pc_info_formatted


class ToolsTab:
    """Classe responsável pela aba de ferramentas adicionais"""

    def __init__(self, parent_interface):
        """Inicializar aba de ferramentas"""
        self.parent = parent_interface
        self.system_commands = parent_interface.system_commands
        self.config = parent_interface.config
        self.logger = parent_interface.logger
        self.log_text = None  # Será definido em create_tools_tab

    def create_tools_tab(self, notebook):
        """Criar aba de ferramentas adicionais"""
        tools_tab = ttk_bs.Frame(notebook)
        notebook.add(tools_tab, text=f"{self.config.get_icon('tools')} Ferramentas")

        tools_frame = ttk_bs.Frame(tools_tab, padding=10)
        tools_frame.pack(fill=BOTH, expand=True)

        # Seção de diagnóstico
        diag_label = ttk_bs.Label(
            tools_frame, text="Diagnóstico", font=("Arial", 12, "bold")
        )
        diag_label.pack(anchor=W, pady=(0, 5))

        diag_frame = ttk_bs.LabelFrame(
            tools_frame, text="Ferramentas de Diagnóstico", padding=10
        )
        diag_frame.pack(fill=X, pady=(0, 10))

        ttk_bs.Button(
            diag_frame,
            text=f"{self.config.get_icon('clipboard')} Verificar Diagnóstico de Erro",
            command=self.check_diagnostics,
            bootstyle="info",
        ).pack(side=LEFT, padx=5)

        ttk_bs.Button(
            diag_frame,
            text=f"{self.config.get_icon('info')} Informações do PC",
            command=self.show_pc_info,
            bootstyle="primary",
        ).pack(side=LEFT, padx=5)

        # Log de atividades
        log_label = ttk_bs.Label(
            tools_frame, text="Log de Atividades", font=("Arial", 12, "bold")
        )
        log_label.pack(anchor=W, pady=(10, 5))

        log_frame = ttk_bs.LabelFrame(
            tools_frame, text="Histórico de Operações", padding=10
        )
        log_frame.pack(fill=BOTH, expand=True)

        # Texto do log com scrollbar
        log_text_frame = ttk_bs.Frame(log_frame)
        log_text_frame.pack(fill=BOTH, expand=True)

        self.log_text = tk.Text(log_text_frame, height=10, wrap=tk.WORD)
        log_scrollbar = ttk_bs.Scrollbar(
            log_text_frame, orient=VERTICAL, command=self.log_text.yview
        )
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)
        log_scrollbar.pack(side=RIGHT, fill=Y)

        # Botões do log
        log_buttons = ttk_bs.Frame(log_frame)
        log_buttons.pack(fill=X, pady=(5, 0))

        ttk_bs.Button(
            log_buttons,
            text=f"{self.config.get_icon('trash')} Limpar Log",
            command=self.clear_log,
            bootstyle="secondary",
        ).pack(side=LEFT, padx=5)

        ttk_bs.Button(
            log_buttons,
            text=f"{self.config.get_icon('save')} Salvar Log",
            command=self.save_log,
            bootstyle="info",
        ).pack(side=LEFT, padx=5)

        return tools_tab

    def check_diagnostics(self):
        """Verificar diagnóstico de erro - Abrir Monitor de Confiabilidade"""
        try:
            import subprocess

            diag_command = self.config.get_command("diagnostics")
            subprocess.run(diag_command, shell=True, check=True)
            self.parent.update_status("Monitor de Confiabilidade aberto com sucesso")
            self.logger.log("Monitor de Confiabilidade (perfmon /rel) executado")
        except subprocess.CalledProcessError as e:
            error_msg = f"Erro ao abrir Monitor de Confiabilidade: {str(e)}"
            self.logger.log(error_msg)
            messagebox.showerror("Erro", error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado ao abrir Monitor de Confiabilidade: {str(e)}"
            self.logger.log(error_msg)
            messagebox.showerror("Erro", error_msg)

    def show_pc_info(self):
        """Mostrar informações do PC"""
        try:
            # Criar uma nova janela para mostrar as informações
            info_window = tk.Toplevel(self.parent.root)
            info_window.title("Informações do Sistema")
            info_window.geometry("800x600")
            info_window.resizable(True, True)

            # Criar um widget de texto com scrollbar
            text_frame = tk.Frame(info_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Área de texto
            text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
            scrollbar = tk.Scrollbar(
                text_frame, orient=tk.VERTICAL, command=text_widget.yview
            )
            text_widget.configure(yscrollcommand=scrollbar.set)

            # Posicionar os widgets
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Botão para fechar
            close_button = tk.Button(
                info_window, text="Fechar", command=info_window.destroy
            )
            close_button.pack(pady=5)

            # Obter e exibir as informações
            info_window.update()  # Atualizar a janela
            text_widget.insert(tk.END, "Coletando informações do sistema...\n\n")
            info_window.update()

            # Obter as informações formatadas
            system_info = get_pc_info_formatted()

            # Limpar o texto e inserir as informações
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, "=== INFORMAÇÕES DO SISTEMA ===\n\n")
            text_widget.insert(tk.END, system_info)

            # Tornar o texto somente leitura
            text_widget.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao obter informações do sistema:\n{str(e)}"
            )

    def clear_log(self):
        """Limpar log"""
        if self.log_text:
            self.logger.clear_widget()
            self.parent.update_status("Log limpo")

    def save_log(self):
        """Salvar log"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt"), ("Todos os arquivos", "*.*")],
        )

        if file_path:
            if self.logger.save_logs_to_file(file_path):
                messagebox.showinfo("Sucesso", f"Log salvo em:\n{file_path}")
            else:
                messagebox.showerror("Erro", "Erro ao salvar log.")
