import tkinter as tk
from tkinter import messagebox
import winreg
import threading

# Importar módulos core
try:
    from core.acelerar_windows import AceleradorWindows
    from core.remover_telemetria import RemoverTelemetria
    from core.remover_features import RemoverFeatures
    from core.remover_animacoes import RemoverAnimacoes
    from core.otimizar_edge import OtimizadorEdge
    from core.desabilitar_tweaks import DesabilitadorTweaks
    from core.disable_software import DisableSoftware
except ImportError:
    print("Aviso: Módulos de otimização não encontrados na pasta core")
    AceleradorWindows = None
    RemoverTelemetria = None
    RemoverFeatures = None
    RemoverAnimacoes = None
    OtimizadorEdge = None
    DesabilitadorTweaks = None
    DisableSoftware = None

# Importar módulo de resultados
from .optimization_results import OptimizationResults


class OptimizationHandlers:
    """Classe responsável pelos handlers das funções de otimização"""

    def __init__(self, optimization_tab):
        """Inicializar handlers"""
        self.parent = optimization_tab
        self.results = OptimizationResults(self)

    def remove_telemetry(self):
        """Remover Telemetria usando o módulo RemoverTelemetria"""
        if not self.parent.confirm_operation(
            "Remover Telemetria",
            "Esta operação irá remover sistemas de telemetria e coleta de dados:\n\n"
            "• Desabilitar telemetria do Windows\n"
            "• Remover metadados de dispositivos da rede\n"
            "• Desabilitar Customer Experience Improvement Program\n"
            "• Desabilitar Application Compatibility tracking\n"
            "• Desabilitar AutoLoggers de diagnóstico\n"
            "• Desabilitar Windows SmartScreen\n"
            "• Desabilitar controle da Assistência Remota\n"
            "• Desabilitar ofertas do Malicious Software Removal Tool\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            return

        # Verificar se o módulo está disponível
        if RemoverTelemetria is None:
            messagebox.showerror(
                "Erro",
                "Módulo de remoção de telemetria não encontrado!\n\n"
                "Verifique se o arquivo 'core/remover_telemetria.py' existe.",
            )
            return

        # Criar janela de progresso
        progress_window, status_label, progress_bar, log_text = (
            self.parent.ui.show_progress_dialog("Removendo Telemetria")
        )

        def run_telemetry_removal():
            """Executar remoção de telemetria em thread separada"""
            try:
                progress_logger = self._create_progress_logger(log_text)
                removedor = RemoverTelemetria(logger=progress_logger)

                # Atualizar status
                status_label.after(
                    0, lambda: status_label.config(text="Removendo telemetria...")
                )

                # Executar remoção
                success, sucessos, erros = removedor.executar_remocao_completa()

                # Mostrar resultado final
                def show_result():
                    progress_bar.stop()
                    self.results.show_telemetry_result(
                        progress_window, status_label, success, sucessos, erros
                    )

                # Agendar para thread principal
                progress_window.after(500, show_result)

            except Exception as e:
                self._handle_error(
                    progress_window,
                    progress_bar,
                    status_label,
                    e,
                    "remoção de telemetria",
                )

        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_telemetry_removal, daemon=True)
        thread.start()

    def disable_windows_services(self):
        """Desabilitar serviços do Windows"""
        if self.parent.confirm_operation(
            "Desabilitar Serviços do Windows",
            "Esta operação irá desabilitar serviços desnecessários do Windows.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            self._execute_optimization("disable_services")

    def disable_windows_software(self):
        """Desabilitar softwares do Windows"""
        if not self.parent.confirm_operation(
            "Desabilitar Softwares do Windows",
            "Esta operação irá desabilitar aplicativos e softwares desnecessários.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            return

        if DisableSoftware is None:
            messagebox.showerror(
                "Erro",
                "Módulo de desabilitação de softwares não encontrado!\n\n"
                "Verifique se o arquivo 'core/disable_software.py' existe.",
            )
            return

        # Criar janela de progresso
        progress_window, status_label, progress_bar, log_text = (
            self.parent.ui.show_progress_dialog("Desabilitando Softwares do Windows")
        )

        def run_disable_software():
            """Executar desabilitação de softwares em thread separada"""
            try:
                progress_logger = self._create_progress_logger(log_text)
                desabilitador = DisableSoftware(logger=progress_logger)

                # Atualizar status
                status_label.after(
                    0, lambda: status_label.config(text="Desabilitando softwares...")
                )

                # Executar desabilitação
                success, sucessos, erros = (
                    desabilitador.executar_desabilitacao_softwares()
                )

                # Mostrar resultado final
                def show_result():
                    progress_bar.stop()
                    self.results.show_disable_software_result(
                        progress_window, status_label, success, sucessos, erros
                    )

                # Agendar resultado para a thread principal
                progress_window.after(500, show_result)

            except Exception as e:
                self._handle_error(
                    progress_window,
                    progress_bar,
                    status_label,
                    e,
                    "desabilitação de softwares",
                )

        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_disable_software, daemon=True)
        thread.start()

    def disable_web_search(self):
        """Desabilitar busca web na barra de pesquisa"""
        if self.parent.confirm_operation(
            "Desabilitar Busca Web",
            "Esta operação irá desabilitar a busca online na barra de pesquisa.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            try:
                # Desabilitar BingSearch
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Search",
                    0,
                    winreg.KEY_SET_VALUE,
                )
                winreg.SetValueEx(key, "BingSearchEnabled", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)

                # Desabilitar SearchBox Suggestions
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER,
                    r"SOFTWARE\Policies\Microsoft\Windows\Explorer",
                )
                winreg.SetValueEx(
                    key, "DisableSearchBoxSuggestions", 0, winreg.REG_DWORD, 1
                )
                winreg.CloseKey(key)

                messagebox.showinfo("Sucesso", "Busca web desabilitada com sucesso!")
                self.parent.log_activity("Busca web na barra de pesquisa desabilitada")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao desabilitar busca web: {str(e)}")

    def disable_browser_cache(self):
        """Desabilitar cache de navegadores"""
        if self.parent.confirm_operation(
            "Desabilitar Cache de Navegadores",
            "Esta operação irá otimizar o cache de navegadores e streaming.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            self._execute_optimization("disable_browser_cache")

    def disable_lock_screen_ads(self):
        """Desabilitar propagandas na tela de bloqueio"""
        if self.parent.confirm_operation(
            "Desabilitar Propagandas na Tela de Bloqueio",
            "Esta operação irá remover propagandas da tela de bloqueio.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            try:
                # Desabilitar RotatingLockScreenOverlay
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                    0,
                    winreg.KEY_SET_VALUE,
                )
                winreg.SetValueEx(
                    key, "RotatingLockScreenOverlayEnabled", 0, winreg.REG_DWORD, 0
                )
                winreg.SetValueEx(
                    key, "SubscribedContent-338387Enabled", 0, winreg.REG_DWORD, 0
                )
                winreg.CloseKey(key)

                messagebox.showinfo(
                    "Sucesso", "Propagandas na tela de bloqueio desabilitadas!"
                )
                self.parent.log_activity(
                    "Propagandas na tela de bloqueio desabilitadas"
                )

            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao desabilitar propagandas: {str(e)}"
                )

    # Métodos auxiliares privados
    def _create_progress_logger(self, log_widget):
        """Criar logger personalizado para capturar mensagens"""

        class ProgressLogger:
            def __init__(self, log_widget):
                self.log_widget = log_widget

            def log(self, message):
                # Atualizar o log text widget de forma thread-safe
                self.log_widget.after(0, lambda: self.update_log(message))

            def info(self, message):
                # Alias para compatibilidade com módulos que usam logger.info()
                self.log(f"INFO: {message}")

            def warning(self, message):
                # Alias para compatibilidade com módulos que usam logger.warning()
                self.log(f"WARNING: {message}")

            def error(self, message):
                # Alias para compatibilidade com módulos que usam logger.error()
                self.log(f"ERROR: {message}")

            def update_log(self, message):
                self.log_widget.insert(tk.END, message + "\n")
                self.log_widget.see(tk.END)
                self.log_widget.update()

        return ProgressLogger(log_widget)

    def _execute_optimization(self, optimization_type):
        """Executar otimização específica (método genérico para funções não implementadas)"""
        try:
            messagebox.showinfo(
                "Em Desenvolvimento",
                f"A otimização '{optimization_type}' será implementada em breve.\n\n"
                "Os scripts .bat correspondentes precisam ser convertidos para Python.",
            )
            self.parent.log_activity(f"Tentativa de execução: {optimization_type}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar otimização: {str(e)}")
            self.parent.log_activity(f"Erro em {optimization_type}: {str(e)}")

    def _handle_error(
        self, progress_window, progress_bar, status_label, error, operation_name
    ):
        """Tratar erros gerais"""

        def show_error():
            progress_bar.stop()
            status_label.config(text="❌ Erro crítico")
            progress_window.after(1000, progress_window.destroy)
            messagebox.showerror(
                "Erro Crítico",
                f"Erro crítico durante a {operation_name}:\n\n{str(error)}",
            )
            self.parent.log_activity(f"Erro crítico na {operation_name}: {str(error)}")

        progress_window.after(0, show_error)

    def remove_unused_features(self):
        """Remover Features Não Usadas usando o módulo RemoverFeatures"""
        if not self.parent.confirm_operation(
            "Remover Features Não Usadas",
            "Esta operação irá remover recursos e funcionalidades não utilizadas:\n\n"
            "• Desabilitar IIS e componentes web\n"
            "• Remover Message Queue (MSMQ)\n"
            "• Desabilitar WCF e recursos de desenvolvimento\n"
            "• Remover Hyper-V (se não utilizado)\n"
            "• Remover apps opcionais (WordPad, IE, etc.)\n"
            "• Desabilitar protocolo SMB1 (inseguro)\n"
            "• Remover recursos de rede avançados\n"
            "• E outras funcionalidades raramente usadas...\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            return

        # Verificar se o módulo está disponível
        if RemoverFeatures is None:
            messagebox.showerror(
                "Erro",
                "Módulo de remoção de features não encontrado!\n\n"
                "Verifique se o arquivo 'core/remover_features.py' existe.",
            )
            return

        # Criar janela de progresso
        progress_window, status_label, progress_bar, log_text = (
            self.parent.ui.show_progress_dialog("Removendo Features Não Usadas")
        )

        def run_features_removal():
            """Executar remoção de features em thread separada"""
            try:
                progress_logger = self._create_progress_logger(log_text)
                removedor = RemoverFeatures(logger=progress_logger)

                # Atualizar status
                status_label.after(
                    0,
                    lambda: status_label.config(
                        text="Removendo features não utilizadas..."
                    ),
                )

                # Executar remoção
                success, sucessos, erros = removedor.executar_remocao_features()

                # Mostrar resultado final
                def show_result():
                    progress_bar.stop()
                    self.results.show_features_result(
                        progress_window, status_label, success, sucessos, erros
                    )

                # Agendar para thread principal
                progress_window.after(500, show_result)

            except Exception as e:
                self._handle_error(
                    progress_window,
                    progress_bar,
                    status_label,
                    e,
                    "remoção de features",
                )

        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_features_removal, daemon=True)
        thread.start()

    def remove_animations(self):
        """Remover Animações usando o módulo RemoverAnimacoes"""
        if not self.parent.confirm_operation(
            "Remover Animações Desnecessárias",
            "Esta operação irá desabilitar animações e efeitos visuais:\n\n"
            "• Desabilitar animações de janelas\n"
            "• Remover efeitos visuais avançados\n"
            "• Desabilitar animações da barra de tarefas\n"
            "• Otimizar arrastar janelas\n"
            "• Desabilitar transparências desnecessárias\n"
            "• Remover sombras em listas\n"
            "• Otimizar suavização de fontes\n"
            "• E outras otimizações visuais...\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            return

        # Verificar se o módulo está disponível
        if RemoverAnimacoes is None:
            messagebox.showerror(
                "Erro",
                "Módulo de remoção de animações não encontrado!\n\n"
                "Verifique se o arquivo 'core/remover_animacoes.py' existe.",
            )
            return

        # Criar janela de progresso
        progress_window, status_label, progress_bar, log_text = (
            self.parent.ui.show_progress_dialog("Removendo Animações")
        )

        def run_animations_removal():
            """Executar remoção de animações em thread separada"""
            try:
                progress_logger = self._create_progress_logger(log_text)
                removedor = RemoverAnimacoes(logger=progress_logger)

                # Atualizar status
                status_label.after(
                    0, lambda: status_label.config(text="Desabilitando animações...")
                )

                # Executar remoção
                success, sucessos, erros = removedor.executar_remocao_animacoes()

                # Mostrar resultado final
                def show_result():
                    progress_bar.stop()
                    self.results.show_animations_result(
                        progress_window, status_label, success, sucessos, erros
                    )

                # Agendar para thread principal
                progress_window.after(500, show_result)

            except Exception as e:
                self._handle_error(
                    progress_window,
                    progress_bar,
                    status_label,
                    e,
                    "remoção de animações",
                )

        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_animations_removal, daemon=True)
        thread.start()

    def optimize_edge(self):
        """Otimizar Microsoft Edge usando o módulo OtimizadorEdge"""
        if not self.parent.confirm_operation(
            "Otimizar Microsoft Edge",
            "Esta operação irá aplicar otimizações específicas para o Microsoft Edge:\n\n"
            "• Desabilitar sidebar/botão Bing\n"
            "• Desabilitar execução em segundo plano\n"
            "• Desabilitar inicialização automática\n"
            "• Remover botão de assinatura Acrobat\n"
            "• Desabilitar geolocalização por padrão\n"
            "• Desabilitar acesso a sensores\n"
            "• Desabilitar notificações de sites\n"
            "• E outras otimizações de privacidade...\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            return

        # Verificar se o módulo está disponível
        if OtimizadorEdge is None:
            messagebox.showerror(
                "Erro",
                "Módulo de otimização do Edge não encontrado!\n\n"
                "Verifique se o arquivo 'core/otimizar_edge.py' existe.",
            )
            return

        # Criar janela de progresso
        progress_window, status_label, progress_bar, log_text = (
            self.parent.ui.show_progress_dialog("Otimizando Microsoft Edge")
        )

        def run_edge_optimization():
            """Executar otimização do Edge em thread separada"""
            try:
                progress_logger = self._create_progress_logger(log_text)
                otimizador = OtimizadorEdge(logger=progress_logger)

                # Atualizar status
                status_label.after(
                    0, lambda: status_label.config(text="Otimizando Microsoft Edge...")
                )

                # Executar otimização
                success, sucessos, erros = otimizador.executar_otimizacao_edge()

                # Mostrar resultado final
                def show_result():
                    progress_bar.stop()
                    self.results.show_edge_result(
                        progress_window, status_label, success, sucessos, erros
                    )

                # Agendar para thread principal
                progress_window.after(500, show_result)

            except Exception as e:
                self._handle_error(
                    progress_window, progress_bar, status_label, e, "otimização do Edge"
                )

        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_edge_optimization, daemon=True)
        thread.start()

    def accelerate_windows(self):
        """Acelerar Windows usando o módulo AceleradorWindows"""
        if not self.parent.confirm_operation(
            "Acelerar Windows",
            "Esta operação irá aplicar 12 otimizações específicas para acelerar o sistema:\n\n"
            "• Otimização de Boot\n"
            "• Aceleração do Menu Iniciar\n"
            "• Aumento da Taxa de Upload\n"
            "• Otimização TCP/IP e DNS\n"
            "• GPU Hardware Scheduling\n"
            "• Modo Compacto no Explorer\n"
            "• Desabilitar Apps em Background\n"
            "• Otimização para Jogos\n"
            "• E outras melhorias...\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            return

        # Verificar se o módulo está disponível
        if AceleradorWindows is None:
            messagebox.showerror(
                "Erro",
                "Módulo de aceleração não encontrado!\n\n"
                "Verifique se o arquivo 'core/acelerar_windows.py' existe.",
            )
            return

        # Criar janela de progresso
        progress_window, status_label, progress_bar, log_text = (
            self.parent.ui.show_progress_dialog("Acelerando Windows")
        )

        def run_acceleration():
            """Executar aceleração em thread separada"""
            try:
                progress_logger = self._create_progress_logger(log_text)
                acelerador = AceleradorWindows(logger=progress_logger)

                # Atualizar status
                status_label.after(
                    0, lambda: status_label.config(text="Aplicando otimizações...")
                )

                # Executar otimizações
                success, sucessos, erros = acelerador.executar_todas_otimizacoes()

                # Mostrar resultado final
                def show_result():
                    progress_bar.stop()
                    self.results.show_acceleration_result(
                        progress_window, status_label, success, sucessos, erros
                    )

                # Agendar para thread principal
                progress_window.after(500, show_result)

            except Exception as e:
                self._handle_error(
                    progress_window, progress_bar, status_label, e, "aceleração"
                )

        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_acceleration, daemon=True)
        thread.start()

    def disable_scheduled_tasks(self):
        """Desabilitar Tarefas Agendadas usando o módulo DesabilitadorTweaks"""
        if not self.parent.confirm_operation(
            "Desabilitar Tarefas Agendadas",
            "Esta operação irá desabilitar tarefas agendadas desnecessárias:\n\n"
            "• Tarefas de telemetria e coleta de dados\n"
            "• Customer Experience Improvement Program\n"
            "• Diagnósticos e manutenção automática\n"
            "• Tarefas do Microsoft Office\n"
            "• Atualizações automáticas do Edge\n"
            "• File History e outras tarefas\n"
            "• E diversas outras tarefas que consomem recursos...\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n"
            "⚠️ Execute como Administrador para melhores resultados!\n\n"
            "Deseja continuar?",
        ):
            return

        # Verificar se o módulo está disponível
        if DesabilitadorTweaks is None:
            messagebox.showerror(
                "Erro",
                "Módulo de desabilitação de tarefas não encontrado!\n\n"
                "Verifique se o arquivo 'core/desabilitar_tweaks.py' existe.",
            )
            return

        # Criar janela de progresso
        progress_window, status_label, progress_bar, log_text = (
            self.parent.ui.show_progress_dialog("Desabilitando Tarefas Agendadas")
        )

        def run_scheduled_tasks_disable():
            """Executar desabilitação de tarefas em thread separada"""
            try:
                progress_logger = self._create_progress_logger(log_text)
                desabilitador = DesabilitadorTweaks(logger=progress_logger)

                # Atualizar status
                status_label.after(
                    0,
                    lambda: status_label.config(
                        text="Desabilitando tarefas agendadas..."
                    ),
                )

                # Executar desabilitação
                success, sucessos, erros = desabilitador.executar_desabilitacao_tweaks()

                # Mostrar resultado final
                def show_result():
                    progress_bar.stop()
                    self.results.show_tasks_result(
                        progress_window, status_label, success, sucessos, erros
                    )

                # Agendar para thread principal
                progress_window.after(500, show_result)

            except Exception as e:
                self._handle_error(
                    progress_window,
                    progress_bar,
                    status_label,
                    e,
                    "desabilitação de tarefas",
                )

        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_scheduled_tasks_disable, daemon=True)
        thread.start()
