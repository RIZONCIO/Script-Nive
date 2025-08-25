# gui/software_manager_gui.py - Interface do gerenciador de software

import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import ttkbootstrap as ttk_bs
from core.software_manager import SoftwareManager


class SoftwareManagerGUI:
    """Classe responsável pela interface do gerenciador de software"""

    def __init__(self, parent_interface):
        """Inicializar gerenciador de software GUI"""
        self.parent = parent_interface
        self.system_commands = parent_interface.system_commands
        self.config = parent_interface.config
        self.logger = parent_interface.logger

        # Variáveis da interface
        self.software_window = None
        self.software_manager = None
        self.software_list = []
        self.software_listbox = None
        self.software_log_text = None

    def reinstall_software_placeholder(self):
        """Nova implementação para reinstalar software"""
        try:
            # Criar instância do gerenciador
            manager = SoftwareManager()

            # Verifica privilégios de administrador
            if not manager.check_admin_privileges():
                messagebox.showerror(
                    "Privilégios Insuficientes",
                    "Esta funcionalidade requer privilégios de administrador.\n\n"
                    "Por favor, execute o ScriptNive como administrador.",
                )
                return

            # Verifica Chocolatey
            if not manager.check_chocolatey_installed():
                response = messagebox.askyesno(
                    "Chocolatey Não Encontrado",
                    "O Chocolatey não está instalado e é necessário para esta funcionalidade.\n\n"
                    "Deseja instalar o Chocolatey automaticamente?",
                )

                if response:
                    self.install_chocolatey_with_progress(manager)
                else:
                    return

            # Cria interface do gerenciador de software
            self.create_software_manager_interface(manager)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir gerenciador de software: {e}")

    def install_chocolatey_with_progress(self, manager):
        """Instala Chocolatey com janela de progresso"""
        progress_window = tk.Toplevel(self.parent.root)
        progress_window.title("Instalando Chocolatey")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        progress_window.transient(self.parent.root)
        progress_window.grab_set()

        # Centralizar janela
        progress_window.geometry(
            "+%d+%d"
            % (self.parent.root.winfo_rootx() + 50, self.parent.root.winfo_rooty() + 50)
        )

        frame = ttk_bs.Frame(progress_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk_bs.Label(frame, text="Instalando Chocolatey...", font=("Arial", 10)).pack(
            pady=(0, 10)
        )

        progress = ttk_bs.Progressbar(frame, mode="indeterminate")
        progress.pack(fill=tk.X, pady=(0, 10))
        progress.start()

        ttk_bs.Label(frame, text="Por favor, aguarde...").pack()

        def install_in_thread():
            try:
                success = manager.install_chocolatey()
                progress_window.after(0, progress.stop)
                progress_window.after(0, progress_window.destroy)
                if success:
                    messagebox.showinfo("Sucesso", "Chocolatey instalado com sucesso!")
                else:
                    messagebox.showerror("Erro", "Falha na instalação do Chocolatey.")
            except Exception as e:
                progress_window.after(0, progress.stop)
                progress_window.after(0, progress_window.destroy)
                messagebox.showerror("Erro", f"Erro durante instalação: {e}")

        threading.Thread(target=install_in_thread, daemon=True).start()

    def create_software_manager_interface(self, manager):
        """Cria interface do gerenciador de software"""
        # Cria janela principal
        self.software_window = tk.Toplevel(self.parent.root)
        self.software_window.title("Gerenciador de Software - ScriptNive")
        self.software_window.geometry("800x600")
        self.software_window.resizable(True, True)

        # Centraliza janela
        self.software_window.transient(self.parent.root)
        self.software_window.grab_set()

        # Variáveis da interface
        self.software_manager = manager
        self.software_list = []

        self.setup_software_interface()
        self.load_software_list()

    def setup_software_interface(self):
        """Configura a interface do gerenciador de software"""

        # Frame principal
        main_frame = ttk_bs.Frame(self.software_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.software_window.columnconfigure(0, weight=1)
        self.software_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título
        title_label = ttk_bs.Label(
            main_frame,
            text="Selecione o software para reinstalar:",
            font=("Arial", 12, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky=tk.W)

        # Frame da lista
        list_frame = ttk_bs.Frame(main_frame)
        list_frame.grid(
            row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Lista de software com scrollbar
        self.software_listbox = tk.Listbox(list_frame, height=15, font=("Consolas", 9))
        scrollbar = ttk_bs.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.software_listbox.yview
        )
        self.software_listbox.configure(yscrollcommand=scrollbar.set)

        self.software_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Frame de botões
        button_frame = ttk_bs.Frame(main_frame)
        button_frame.grid(
            row=2, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E)
        )

        # Botões
        ttk_bs.Button(
            button_frame, text="Atualizar Lista", command=self.load_software_list
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk_bs.Button(
            button_frame,
            text="Reinstalar Selecionado",
            command=self.reinstall_selected_software,
        ).pack(side=tk.LEFT, padx=5)

        ttk_bs.Button(
            button_frame, text="Fechar", command=self.software_window.destroy
        ).pack(side=tk.RIGHT)

        # Área de log
        log_frame = ttk_bs.LabelFrame(main_frame, text="Log de Operações", padding="5")
        log_frame.grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.software_log_text = scrolledtext.ScrolledText(
            log_frame, height=8, font=("Consolas", 8)
        )
        self.software_log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        main_frame.rowconfigure(3, weight=1)

    def log_software_message(self, message):
        """Adiciona mensagem ao log do software"""
        if self.software_log_text:
            self.software_log_text.insert(tk.END, f"{message}\n")
            self.software_log_text.see(tk.END)
            self.software_log_text.update()

    def load_software_list(self):
        """Carrega lista de software instalado"""
        self.log_software_message("Carregando lista de software instalado...")

        def load_in_thread():
            try:
                self.software_list = self.software_manager.get_installed_software()
                # Atualiza interface na thread principal
                self.software_window.after(0, self.update_software_listbox)
            except Exception as e:
                self.software_window.after(
                    0,
                    lambda: self.log_software_message(
                        f"Erro ao carregar software: {e}"
                    ),
                )

        # Carrega em thread separada para não travar a interface
        threading.Thread(target=load_in_thread, daemon=True).start()

    def update_software_listbox(self):
        """Atualiza a listbox com o software encontrado"""
        if self.software_listbox:
            self.software_listbox.delete(0, tk.END)

            for i, software in enumerate(self.software_list):
                self.software_listbox.insert(
                    tk.END, f"{i:3d} - {software['display_name']}"
                )

            self.log_software_message(
                f"Encontrados {len(self.software_list)} softwares instalados."
            )

    def reinstall_selected_software(self):
        """Reinstala o software selecionado"""
        if not self.software_listbox:
            return

        selection = self.software_listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "Seleção Necessária", "Por favor, selecione um software da lista."
            )
            return

        index = selection[0]
        selected_software = self.software_list[index]

        # Confirmação
        response = messagebox.askyesno(
            "Confirmar Reinstalação",
            "Deseja desinstalar e reinstalar o seguinte software?\n\n"
            f"Nome: {selected_software['display_name']}\n\n"
            "AVISO: Esta operação irá:\n"
            "1. Desinstalar o software atual\n"
            "2. Tentar reinstalá-lo via Chocolatey\n\n"
            "Continuar?",
        )

        if not response:
            return

        # Executa reinstalação em thread separada
        def reinstall_in_thread():
            try:
                self.software_window.after(
                    0,
                    lambda: self.log_software_message(
                        f"Iniciando reinstalação de: {selected_software['display_name']}"
                    ),
                )

                success, message = self.software_manager.process_software_reinstall(
                    selected_software
                )

                # Atualiza interface na thread principal
                if success:
                    self.software_window.after(
                        0, lambda: self.log_software_message(f"✅ {message}")
                    )
                    self.software_window.after(
                        0, lambda: messagebox.showinfo("Sucesso", message)
                    )
                else:
                    self.software_window.after(
                        0, lambda: self.log_software_message(f"❌ {message}")
                    )
                    self.software_window.after(
                        0, lambda: messagebox.showerror("Erro", message)
                    )

                # Atualiza lista
                self.software_window.after(0, self.load_software_list)

            except Exception as e:
                error_msg = f"Erro durante reinstalação: {e}"
                self.software_window.after(
                    0, lambda: self.log_software_message(f"❌ {error_msg}")
                )
                self.software_window.after(
                    0, lambda: messagebox.showerror("Erro", error_msg)
                )

        threading.Thread(target=reinstall_in_thread, daemon=True).start()
