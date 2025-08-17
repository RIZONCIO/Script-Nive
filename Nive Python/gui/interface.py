"""
Interface Gráfica ScriptNive
gui/interface.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk_bs
import tkinter as tk
from tkinter import ttk
import subprocess
from ttkbootstrap.constants import *
import webbrowser
import os
from datetime import datetime
from core.system_info import get_pc_info_formatted


class ScriptNiveInterface:
    """Classe da interface gráfica principal"""

    def __init__(self, root, system_commands, logger, config):
        """Inicializar interface"""
        self.root = root
        self.system_commands = system_commands
        self.logger = logger
        self.config = config

        # Status da aplicação
        self.status_var = tk.StringVar(value="Pronto")

        # Criar interface
        self.create_widgets()

        # Configurar logger para usar o widget de texto
        self.logger.set_widget(self.log_text)

    def create_widgets(self):
        """Criar todos os widgets da interface"""
        # Frame principal
        main_frame = ttk_bs.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # Cabeçalho
        self.create_header(main_frame)

        # Notebook para organizar as abas
        self.notebook = ttk_bs.Notebook(main_frame)
        self.notebook.pack(fill=BOTH, expand=True, pady=(10, 0))

        # Criar abas
        self.create_main_tab()
        self.create_system_tab()
        self.create_tools_tab()
        self.create_info_tab()

        # Barra de status
        self.create_status_bar(main_frame)

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

            info_text = f"Computador: {computer_name} | Usuário: {username} | Data: {now.strftime('%d/%m/%Y %H:%M')}"

            info_label = ttk_bs.Label(
                info_frame, text=info_text, font=("Arial", 9), bootstyle="light"
            )
            info_label.pack()
        except:
            pass

    def create_main_tab(self):
        """Criar aba principal com as tarefas mais comuns"""
        main_tab = ttk_bs.Frame(self.notebook)
        self.notebook.add(main_tab, text=f"{self.config.get_icon('home')} Principal")

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

    def create_system_tab(self):
        """Criar aba de ferramentas do sistema"""
        system_tab = ttk_bs.Frame(self.notebook)
        self.notebook.add(system_tab, text=f"{self.config.get_icon('system')} Sistema")

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
                self.reinstall_software_placeholder,
                "danger",
            ),
            (
                f"{self.config.get_icon('folder_x')} Deletar Pastas Corrompidas",
                self.delete_corrupted_folders,
                "dark",
            ),
            (
                f"{self.config.get_icon('tool')} Reparo Completo do Windows",
                self.complete_repair_placeholder,
                "danger",
            ),
            (
                f"{self.config.get_icon('zap')} Otimizar Windows",
                self.optimize_windows_placeholder,
                "success",
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

    def create_tools_tab(self):
        """Criar aba de ferramentas adicionais"""
        tools_tab = ttk_bs.Frame(self.notebook)
        self.notebook.add(
            tools_tab, text=f"{self.config.get_icon('tools')} Ferramentas"
        )

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

    def create_info_tab(self):
        """Criar aba de informações e créditos"""
        info_tab = ttk_bs.Frame(self.notebook)
        self.notebook.add(info_tab, text=f"{self.config.get_icon('about')} Sobre")

        info_frame = ttk_bs.Frame(info_tab, padding=20)
        info_frame.pack(fill=BOTH, expand=True)

        # Logo/Título
        title = ttk_bs.Label(
            info_frame, text="ScriptNive", font=("Arial", 24, "bold"), bootstyle="info"
        )
        title.pack(pady=(0, 10))

        version = ttk_bs.Label(
            info_frame,
            text=f"Versão {self.config.version} - Interface Gráfica",
            font=("Arial", 12),
        )
        version.pack(pady=(0, 20))

        # Informações
        info_text = """ScriptNive é uma ferramenta completa para manutenção e otimização do Windows.
Desenvolvida para facilitar tarefas de manutenção que normalmente requerem
conhecimento técnico avançado.

Características:
• Interface gráfica moderna e intuitiva
• Ferramentas de diagnóstico avançado
• Limpeza automática do sistema
• Reparos automáticos de erros
• Otimização de performance
• Log detalhado de operações"""

        info_label = ttk_bs.Label(info_frame, text=info_text, justify=LEFT)
        info_label.pack(pady=(0, 20), anchor=W)

        # Créditos
        credits_frame = ttk_bs.LabelFrame(info_frame, text="Créditos", padding=15)
        credits_frame.pack(fill=X, pady=(0, 10))

        credits_text = """Criador do ScriptNive: Ryan Vinicius Carvalho Pereira
Criador do Reparo Completo: Ivo Dias
Interface Gráfica: Python + ttkbootstrap
Data de Lançamento: 10/Set./2022"""

        credits_label = ttk_bs.Label(credits_frame, text=credits_text, justify=LEFT)
        credits_label.pack(anchor=W)

        # Botões de links
        links_frame = ttk_bs.Frame(info_frame)
        links_frame.pack(fill=X, pady=(10, 0))

        links = [
            ("Documentação Microsoft", self.config.get_link("microsoft_docs")),
            ("DOS Tips", self.config.get_link("dos_tips")),
            ("GitHub", self.config.get_link("github")),
        ]

        for text, url in links:
            ttk_bs.Button(
                links_frame,
                text=text,
                command=lambda u=url: webbrowser.open(u),
                bootstyle="link",
            ).pack(side=LEFT, padx=5)

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

    # Métodos de interface para ferramentas do sistema
    def open_control_panel(self):
        """Abrir painel de controle"""
        import subprocess

        subprocess.Popen("control.exe")
        self.update_status("Painel de Controle aberto")

    def open_task_manager(self):
        """Abrir gerenciador de tarefas"""
        import subprocess

        subprocess.Popen("taskmgr.exe")
        self.update_status("Gerenciador de Tarefas aberto")

    def start_mrt(self):
        """Iniciar MRT (Ferramenta de Remoção de Malware da Microsoft)"""
        try:
            import subprocess

            # Comando correto do MRT
            mrt_command = self.config.get_command("mrt")
            subprocess.run(mrt_command, shell=True, check=True)
            self.update_status(
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
            import subprocess

            # Comando correto para o Monitor de Confiabilidade
            diag_command = self.config.get_command("diagnostics")
            subprocess.run(diag_command, shell=True, check=True)
            self.update_status("Monitor de Confiabilidade aberto com sucesso")
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

    # Placeholders para funcionalidades que requerem scripts externos
    def reinstall_software_placeholder(self):
        """Placeholder para reinstalar software"""
        messagebox.showinfo(
            "Script Externo Necessário",
            "Esta funcionalidade requer o script PowerShell 'Opcao13.ps1'.\n\nEm desenvolvimento para próxima versão.",
        )

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

            # Se o usuário clicou "Não", simplesmente retorna sem fazer nada
            if not confirm:
                self.update_status("Reparo completo cancelado pelo usuário")
                return

            # SOMENTE AGORA criar a janela de progresso (depois da confirmação)
            self.create_progress_window("Reparo Completo do Windows")

            def progress_callback(percentage, step_description):
                """Callback para atualizar progresso"""
                if hasattr(self, "progress_var") and hasattr(self, "progress_window"):
                    try:
                        self.progress_var.set(percentage)
                        self.progress_label_var.set(step_description)
                        self.progress_window.update()
                    except:
                        pass  # Janela pode ter sido fechada

            def success_callback_wrapper(message):
                """Callback de sucesso com fechamento da janela"""
                # Habilitar botão de fechar
                if hasattr(self, "progress_close_btn"):
                    self.progress_close_btn.config(state=tk.NORMAL)
                    self.progress_label_var.set("Reparo concluído com sucesso!")
                    self.progress_var.set(100)

                messagebox.showinfo(
                    "Reparo Concluído",
                    "Reparo completo do Windows finalizado!\n\n"
                    "RECOMENDA-SE REINICIAR O COMPUTADOR AGORA.\n\n"
                    "Deseja reiniciar agora?",
                )

                if messagebox.askyesno("Reiniciar", "Reiniciar o computador agora?"):
                    subprocess.run("shutdown -r -t 10", shell=True)

                # Fechar janela de progresso
                self.close_progress_window()

            def error_callback_wrapper(error):
                """Callback de erro com fechamento da janela"""
                # Habilitar botão de fechar
                if hasattr(self, "progress_close_btn"):
                    self.progress_close_btn.config(state=tk.NORMAL)
                    self.progress_label_var.set("Erro durante o reparo!")

                messagebox.showerror(
                    "Erro no Reparo",
                    f"Ocorreu um erro durante o reparo completo:\n\n{error}\n\n"
                    "Verifique o log para mais detalhes.",
                )

                # Fechar janela de progresso
                self.close_progress_window()

            # Chamar o reparo completo SEM mostrar a confirmação novamente
            # (pois já foi mostrada acima)
            self.system_commands.complete_windows_repair_direct(
                progress_callback, success_callback_wrapper, error_callback_wrapper
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar reparo completo:\n{str(e)}")
            # Se houve erro, fechar janela de progresso se ela existir
            if hasattr(self, "progress_window"):
                self.close_progress_window()

    def optimize_windows_placeholder(self):
        """Placeholder para otimizar Windows"""
        messagebox.showinfo(
            "Script Externo Necessário",
            "Esta funcionalidade requer o script 'NiveBoost.bat'.\n\nEm desenvolvimento para próxima versão.",
        )

    # E substitua a função show_pc_info por esta:
    def show_pc_info(self):
        """Mostrar informações do PC"""
        try:
            # Criar uma nova janela para mostrar as informações
            info_window = tk.Toplevel(self.root)
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

    def custom_cleanup_placeholder(self):
        """Placeholder para limpeza personalizada"""
        messagebox.showinfo(
            "Em Desenvolvimento",
            "Funcionalidade de limpeza personalizada em desenvolvimento.\n\nSerá incluída em próxima atualização.",
        )

    # Métodos de controle do log
    def clear_log(self):
        """Limpar log"""
        self.logger.clear_widget()
        self.update_status("Log limpo")

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

    def update_status(self, message):
        """Atualizar mensagem de status"""
        self.status_var.set(message)
        self.logger.log(message)
        self.root.update_idletasks()
