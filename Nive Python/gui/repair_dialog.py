# gui/repair_dialog.py - Diálogo do reparo completo do Windows

import subprocess
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk_bs


class RepairDialog:
    """Classe responsável pelo diálogo de reparo completo do Windows"""

    def __init__(self, parent_interface):
        """Inicializar diálogo de reparo"""
        self.parent = parent_interface
        self.system_commands = parent_interface.system_commands
        self.config = parent_interface.config
        self.logger = parent_interface.logger

        # Variáveis da janela de progresso
        self.progress_window = None
        self.progress_var = None
        self.progress_label_var = None
        self.progress_close_btn = None

    def complete_repair_placeholder(self):
        """Executar Reparo Completo do Windows"""
        try:
            # PRIMEIRO: Mostrar confirmação ANTES de criar a janela de progresso
            confirm = messagebox.askyesno(
                "ATENÇÃO - Reparo Completo do Windows",
                "Esta operação irá:\n\n"
                "• Executar reparos profundos no sistema\n"
                "• Resetar configurações de rede\n"
                "• Limpar arquivos do Windows Update\n"
                "• Remover software pirata (se encontrado)\n"
                "• Re-registrar DLLs críticas\n"
                "• Agendar verificação de disco\n\n"
                "ESTE PROCESSO PODE DEMORAR MUITO TEMPO!\n"
                "Deseja continuar?",
            )

            if not confirm:
                self.parent.update_status("Reparo completo cancelado pelo usuário")
                return

            # Criar janela de progresso
            self.create_progress_window("Reparo Completo do Windows")

            def progress_callback(percentage, step_description):
                """Callback para atualizar progresso"""
                if hasattr(self, "progress_var") and hasattr(self, "progress_window"):
                    try:
                        self.progress_var.set(percentage)
                        self.progress_label_var.set(step_description)
                        self.progress_window.update()
                    except Exception:
                        pass  # Janela pode ter sido fechada

            def success_callback_wrapper(_message):
                """Callback de sucesso com fechamento da janela"""
                if hasattr(self, "progress_close_btn"):
                    self.progress_close_btn.config(state=tk.NORMAL)
                    self.progress_label_var.set("Reparo concluído com sucesso!")
                    self.progress_var.set(100)

                if messagebox.askyesno("Reiniciar", "Reiniciar o computador agora?"):
                    subprocess.run("shutdown -r -t 10", shell=True)

                self.close_progress_window()

            def error_callback_wrapper(error):
                """Callback de erro com fechamento da janela"""
                if hasattr(self, "progress_close_btn"):
                    self.progress_close_btn.config(state=tk.NORMAL)
                    self.progress_label_var.set("Erro durante o reparo!")

                messagebox.showerror(
                    "Erro no Reparo",
                    "Ocorreu um erro durante o reparo completo:\n\n"
                    f"{error}\n\nVerifique o log para mais detalhes.",
                )
                self.close_progress_window()

            # Chamar o reparo completo direto
            self.system_commands.complete_windows_repair_direct(
                progress_callback, success_callback_wrapper, error_callback_wrapper
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar reparo completo:\n{str(e)}")
            if hasattr(self, "progress_window"):
                self.close_progress_window()

    def create_progress_window(self, title: str):
        """Cria uma janela de progresso simples (utilizada no reparo completo)."""
        self.progress_window = tk.Toplevel(self.parent.root)
        self.progress_window.title(title)
        self.progress_window.geometry("450x160")
        self.progress_window.resizable(False, False)
        self.progress_window.transient(self.parent.root)
        self.progress_window.grab_set()

        # Centralizar janela
        x = self.parent.root.winfo_rootx() + 50
        y = self.parent.root.winfo_rooty() + 50
        self.progress_window.geometry(f"+{x}+{y}")

        container = ttk_bs.Frame(self.progress_window, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        self.progress_label_var = tk.StringVar(value="Iniciando...")
        ttk_bs.Label(container, textvariable=self.progress_label_var).pack(anchor="w")

        self.progress_var = tk.DoubleVar(value=0.0)
        ttk_bs.Progressbar(
            container, variable=self.progress_var, maximum=100, mode="determinate"
        ).pack(fill=tk.X, pady=10)

        self.progress_close_btn = ttk_bs.Button(
            container,
            text="Fechar",
            state=tk.DISABLED,
            command=self.close_progress_window,
        )
        self.progress_close_btn.pack(anchor="e")

    def close_progress_window(self):
        """Fecha a janela de progresso, se existir."""
        try:
            if (
                hasattr(self, "progress_window")
                and self.progress_window
                and self.progress_window.winfo_exists()
            ):
                self.progress_window.grab_release()
                self.progress_window.destroy()
                self.progress_window = None
        except Exception:
            pass
