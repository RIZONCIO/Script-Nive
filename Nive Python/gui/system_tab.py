# gui/system_tab.py - Aba de ferramentas do sistema

import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *


class SystemTab:
    """Classe responsável pela aba de ferramentas do sistema"""

    def __init__(self, parent_interface):
        """Inicializar aba de sistema"""
        self.parent = parent_interface
        self.system_commands = parent_interface.system_commands
        self.config = parent_interface.config
        self.logger = parent_interface.logger

    def create_system_tab(self, notebook):
        """Criar aba de ferramentas do sistema"""
        system_tab = ttk_bs.Frame(notebook)
        notebook.add(system_tab, text=f"{self.config.get_icon('system')} Sistema")

        buttons_frame = ttk_bs.Frame(system_tab, padding=10)
        buttons_frame.pack(fill=BOTH, expand=True)

        system_tasks = [
            (
                f"{self.config.get_icon('activity')} Gerenciador de Tarefas",
                self.open_task_manager,
                "primary",
            ),
            (f"{self.config.get_icon('shield')} Iniciar MRT", self.start_mrt, "info"),
            (
                f"{self.config.get_icon('package')} Atualizar Programas",
                self.system_commands.update_programs,
                "success",
            ),
            (
                f"{self.config.get_icon('volume')} Reparar Som",
                self.system_commands.fix_audio,
                "warning",
            ),
            (
                f"{self.config.get_icon('download')} Reinstalar Software",
                self.parent.reinstall_software_placeholder,  # Delegado para o parent
                "danger",
            ),
            (
                f"{self.config.get_icon('folder_x')} Deletar Pastas Corrompidas",
                self.delete_corrupted_folders,
                "dark",
            ),
            (
                f"{self.config.get_icon('tool')} Reparo Completo do Windows",
                self.parent.complete_repair_placeholder,  # Delegado para o parent
                "danger",
            ),
        ]

        for i, (text, command, style) in enumerate(system_tasks):
            row = i // 2
            col = i % 2

            btn = ttk_bs.Button(
                buttons_frame, text=text, command=command, bootstyle=style, width=35
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

        return system_tab

    def open_task_manager(self):
        """Abrir gerenciador de tarefas"""
        subprocess.Popen("taskmgr.exe")
        self.parent.update_status("Gerenciador de Tarefas aberto")

    def start_mrt(self):
        """Iniciar MRT (Ferramenta de Remoção de Malware da Microsoft)"""
        try:
            mrt_command = self.config.get_command("mrt")
            subprocess.run(mrt_command, shell=True, check=True)
            self.parent.update_status(
                "MRT (Ferramenta de Remoção de Malware) iniciado com sucesso"
            )
            self.logger.log("MRT iniciado com sucesso")
        except subprocess.CalledProcessError as e:
            error_msg = f"Erro ao iniciar MRT: {str(e)}"
            self.logger.log(error_msg)
            messagebox.showerror("Erro", error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado ao iniciar MRT: {str(e)}"
            self.logger.log(error_msg)
            messagebox.showerror("Erro", error_msg)

    def check_diagnostics(self):
        """Verificar diagnóstico de erro - Abrir Monitor de Confiabilidade"""
        try:
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

    def delete_corrupted_folders(self):
        """Deletar pastas corrompidas"""
        folder_path = filedialog.askdirectory(
            title="Selecione a pasta corrompida para deletar"
        )

        if folder_path:
            if messagebox.askyesno(
                "Confirmar",
                f"Deletar permanentemente a pasta:\n{folder_path}\n\nEsta ação não pode ser desfeita!",
            ):
                success = self.system_commands.delete_corrupted_folder(folder_path)
                if success:
                    messagebox.showinfo("Sucesso", "Pasta deletada com sucesso!")
                else:
                    messagebox.showwarning(
                        "Aviso",
                        "A pasta pode ainda existir.\nTente reiniciar o PC em modo seguro e repetir a operação.",
                    )
