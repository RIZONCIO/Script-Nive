def remove_telemetry(self):
    """Remover Telemetria usando o módulo RemoverTelemetria"""
    if not self.confirm_operation(
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
    progress_window, status_label, progress_bar, log_text = self.show_progress_dialog(
        "Removendo Telemetria"
    )

    def run_telemetry_removal():
        """Executar remoção de telemetria em thread separada"""
        try:
            # Criar logger personalizado para capturar as mensagens
            class ProgressLogger:
                def __init__(self, log_widget):
                    self.log_widget = log_widget

                def log(self, message):
                    # Atualizar o log text widget de forma thread-safe
                    self.log_widget.after(0, lambda: self.update_log(message))

                def update_log(self, message):
                    self.log_widget.insert(tk.END, message + "\n")
                    self.log_widget.see(tk.END)
                    self.log_widget.update()

            # Criar removedor de telemetria com logger personalizado
            progress_logger = ProgressLogger(log_text)
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

                if success and len(erros) == 0:
                    status_label.config(text="✅ Telemetria removida com sucesso!")
                    result_message = f"🎉 TELEMETRIA REMOVIDA COM SUCESSO!\n\n"
                    result_message += f"✅ {len(sucessos)} configurações aplicadas\n\n"
                    result_message += "🔒 PRIVACIDADE MELHORADA:\n"
                    result_message += "• Telemetria do Windows desabilitada\n"
                    result_message += "• Coleta de dados interrompida\n"
                    result_message += "• Tracking de aplicações desabilitado\n"
                    result_message += "• SmartScreen desabilitado\n"
                    result_message += "• AutoLoggers de diagnóstico parados\n\n"
                    result_message += "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"

                    # Fechar janela de progresso após 3 segundos
                    progress_window.after(3000, progress_window.destroy)

                    messagebox.showinfo("Telemetria Removida", result_message)

                elif len(sucessos) > len(erros):
                    status_label.config(text="⚠️ Concluído com alguns avisos")
                    result_message = f"⚠️ TELEMETRIA PARCIALMENTE REMOVIDA\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
                    result_message += (
                        "🔒 A maior parte da telemetria foi desabilitada.\n\n"
                    )
                    result_message += "Detalhes dos erros:\n"
                    for erro in erros[:5]:  # Mostrar apenas os primeiros 5 erros
                        result_message += f"• {erro}\n"
                    if len(erros) > 5:
                        result_message += f"... e mais {len(erros) - 5} erros\n"
                    result_message += "\n⚠️ IMPORTANTE: Reinicie o sistema!"

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showwarning("Remoção Parcial", result_message)

                else:
                    status_label.config(text="❌ Concluído com vários erros")
                    result_message = f"❌ MUITOS ERROS NA REMOÇÃO\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"❌ Erros: {len(erros)}\n\n"
                    result_message += "Principais erros:\n"
                    for erro in erros[:3]:
                        result_message += f"• {erro}\n"
                    result_message += (
                        f"\nVerifique se está executando como Administrador!"
                    )

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showerror("Erros na Remoção", result_message)

                # Log da atividade
                self.log_activity(
                    f"Remoção de telemetria: {len(sucessos)} sucessos, {len(erros)} erros"
                )

            # Agendar para thread principal
            progress_window.after(500, show_result)

        except Exception as e:

            def show_error():
                progress_bar.stop()
                status_label.config(text="❌ Erro crítico")
                progress_window.after(1000, progress_window.destroy)
                messagebox.showerror(
                    "Erro Crítico", f"Erro crítico durante a remoção:\n\n{str(e)}"
                )
                self.log_activity(f"Erro crítico na remoção de telemetria: {str(e)}")

            progress_window.after(0, show_error)

    # Executar em thread separada para não travar a interface
    thread = threading.Thread(target=run_telemetry_removal, daemon=True)
    thread.start()

    def remove_unused_features(self):
        """Remover Features Não Usadas usando o módulo RemoverFeatures"""

    if not self.confirm_operation(
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
    progress_window, status_label, progress_bar, log_text = self.show_progress_dialog(
        "Removendo Features Não Usadas"
    )

    def run_features_removal():
        """Executar remoção de features em thread separada"""
        try:
            # Criar logger personalizado para capturar as mensagens
            class ProgressLogger:
                def __init__(self, log_widget):
                    self.log_widget = log_widget

                def log(self, message):
                    # Atualizar o log text widget de forma thread-safe
                    self.log_widget.after(0, lambda: self.update_log(message))

                def update_log(self, message):
                    self.log_widget.insert(tk.END, message + "\n")
                    self.log_widget.see(tk.END)
                    self.log_widget.update()

            # Criar removedor de features com logger personalizado
            progress_logger = ProgressLogger(log_text)
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

                if success and len(erros) == 0:
                    status_label.config(text="✅ Features removidas com sucesso!")
                    result_message = f"🎉 FEATURES REMOVIDAS COM SUCESSO!\n\n"
                    result_message += f"✅ {len(sucessos)} configurações aplicadas\n\n"
                    result_message += "🗑️ RECURSOS REMOVIDOS:\n"
                    result_message += "• IIS e componentes web desabilitados\n"
                    result_message += "• Apps opcionais removidos\n"
                    result_message += "• Recursos de rede avançados desabilitados\n"
                    result_message += "• Protocolo SMB1 desabilitado\n"
                    result_message += "• Features de desenvolvimento removidas\n\n"
                    result_message += "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"

                    # Fechar janela de progresso após 3 segundos
                    progress_window.after(3000, progress_window.destroy)

                    messagebox.showinfo("Features Removidas", result_message)

                elif len(sucessos) > len(erros):
                    status_label.config(text="⚠️ Concluído com alguns avisos")
                    result_message = f"⚠️ FEATURES PARCIALMENTE REMOVIDAS\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
                    result_message += "🗑️ A maior parte das features foi removida.\n\n"
                    result_message += "Detalhes dos erros:\n"
                    for erro in erros[:5]:  # Mostrar apenas os primeiros 5 erros
                        result_message += f"• {erro}\n"
                    if len(erros) > 5:
                        result_message += f"... e mais {len(erros) - 5} erros\n"
                    result_message += "\n⚠️ IMPORTANTE: Reinicie o sistema!"

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showwarning("Remoção Parcial", result_message)

                else:
                    status_label.config(text="❌ Concluído com vários erros")
                    result_message = f"❌ MUITOS ERROS NA REMOÇÃO\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"❌ Erros: {len(erros)}\n\n"
                    result_message += "Principais erros:\n"
                    for erro in erros[:3]:
                        result_message += f"• {erro}\n"
                    result_message += (
                        f"\nVerifique se está executando como Administrador!"
                    )

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showerror("Erros na Remoção", result_message)

                # Log da atividade
                self.log_activity(
                    f"Remoção de features: {len(sucessos)} sucessos, {len(erros)} erros"
                )

            # Agendar para thread principal
            progress_window.after(500, show_result)

        except Exception as e:

            def show_error():
                progress_bar.stop()
                status_label.config(text="❌ Erro crítico")
                progress_window.after(1000, progress_window.destroy)
                messagebox.showerror(
                    "Erro Crítico", f"Erro crítico durante a remoção:\n\n{str(e)}"
                )
                self.log_activity(f"Erro crítico na remoção de features: {str(e)}")

            progress_window.after(0, show_error)

    # Executar em thread separada para não travar a interface
    thread = threading.Thread(target=run_features_removal, daemon=True)
    thread.start()

    def remove_animations(self):
        """Remover Animações usando o módulo RemoverAnimacoes"""
        if not self.confirm_operation(
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
    progress_window, status_label, progress_bar, log_text = self.show_progress_dialog(
        "Removendo Animações"
    )

    def run_animations_removal():
        """Executar remoção de animações em thread separada"""
        try:
            # Criar logger personalizado para capturar as mensagens
            class ProgressLogger:
                def __init__(self, log_widget):
                    self.log_widget = log_widget

                def log(self, message):
                    # Atualizar o log text widget de forma thread-safe
                    self.log_widget.after(0, lambda: self.update_log(message))

                def update_log(self, message):
                    self.log_widget.insert(tk.END, message + "\n")
                    self.log_widget.see(tk.END)
                    self.log_widget.update()

            # Criar removedor de animações com logger personalizado
            progress_logger = ProgressLogger(log_text)
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

                if success and len(erros) == 0:
                    status_label.config(text="✅ Animações desabilitadas com sucesso!")
                    result_message = f"🎉 ANIMAÇÕES REMOVIDAS COM SUCESSO!\n\n"
                    result_message += f"✅ {len(sucessos)} configurações aplicadas\n\n"
                    result_message += "🎨 MELHORIAS APLICADAS:\n"
                    result_message += "• Animações de janelas desabilitadas\n"
                    result_message += "• Efeitos visuais otimizados\n"
                    result_message += "• Barra de tarefas mais responsiva\n"
                    result_message += "• Transparências desnecessárias removidas\n"
                    result_message += "• Sistema mais rápido e fluido\n\n"
                    result_message += "⚠️ IMPORTANTE: Reinicie ou faça logoff/login para aplicar todas as mudanças!"

                    # Fechar janela de progresso após 3 segundos
                    progress_window.after(3000, progress_window.destroy)

                    messagebox.showinfo("Animações Removidas", result_message)

                elif len(sucessos) > len(erros):
                    status_label.config(text="⚠️ Concluído com alguns avisos")
                    result_message = f"⚠️ ANIMAÇÕES PARCIALMENTE REMOVIDAS\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
                    result_message += (
                        "🎨 A maior parte das animações foi desabilitada.\n\n"
                    )
                    result_message += "Detalhes dos erros:\n"
                    for erro in erros[:5]:  # Mostrar apenas os primeiros 5 erros
                        result_message += f"• {erro}\n"
                    if len(erros) > 5:
                        result_message += f"... e mais {len(erros) - 5} erros\n"
                    result_message += "\n⚠️ IMPORTANTE: Reinicie o sistema!"

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showwarning("Remoção Parcial", result_message)

                else:
                    status_label.config(text="❌ Concluído com vários erros")
                    result_message = f"❌ MUITOS ERROS NA REMOÇÃO\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"❌ Erros: {len(erros)}\n\n"
                    result_message += "Principais erros:\n"
                    for erro in erros[:3]:
                        result_message += f"• {erro}\n"
                    result_message += (
                        f"\nVerifique se está executando como Administrador!"
                    )

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showerror("Erros na Remoção", result_message)

                # Log da atividade
                self.log_activity(
                    f"Remoção de animações: {len(sucessos)} sucessos, {len(erros)} erros"
                )

            # Agendar para thread principal
            progress_window.after(500, show_result)

        except Exception as e:

            def show_error():
                progress_bar.stop()
                status_label.config(text="❌ Erro crítico")
                progress_window.after(1000, progress_window.destroy)
                messagebox.showerror(
                    "Erro Crítico", f"Erro crítico durante a remoção:\n\n{str(e)}"
                )
                self.log_activity(f"Erro crítico na remoção de animações: {str(e)}")

            progress_window.after(0, show_error)

    # Executar em thread separada para não travar a interface
    thread = threading.Thread(target=run_animations_removal, daemon=True)
    thread.start()

    def disable_web_search(self):
        if self.confirm_operation(
            "Desabilitar Busca Web",
            "Esta operação irá desabilitar a busca online na barra de pesquisa.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
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
                self.log_activity("Busca web na barra de pesquisa desabilitada")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao desabilitar busca web: {str(e)}")

    def disable_browser_cache(self):
        if self.confirm_operation(
            "Desabilitar Cache de Navegadores",
            "Esta operação irá otimizar o cache de navegadores e streaming.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
            "Deseja continuar?",
        ):
            self.execute_optimization("disable_browser_cache")

    def disable_lock_screen_ads(self):
        if self.confirm_operation(
            "Desabilitar Propagandas na Tela de Bloqueio",
            "Esta operação irá remover propagandas da tela de bloqueio.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
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
                self.log_activity("Propagandas na tela de bloqueio desabilitadas")

            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao desabilitar propagandas: {str(e)}"
                )

    def optimize_edge(self):
        """Otimizar Microsoft Edge usando o módulo OtimizadorEdge"""

    if not self.confirm_operation(
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
    progress_window, status_label, progress_bar, log_text = self.show_progress_dialog(
        "Otimizando Microsoft Edge"
    )

    def run_edge_optimization():
        """Executar otimização do Edge em thread separada"""
        try:
            # Criar logger personalizado para capturar as mensagens
            class ProgressLogger:
                def __init__(self, log_widget):
                    self.log_widget = log_widget

                def log(self, message):
                    # Atualizar o log text widget de forma thread-safe
                    self.log_widget.after(0, lambda: self.update_log(message))

                def update_log(self, message):
                    self.log_widget.insert(tk.END, message + "\n")
                    self.log_widget.see(tk.END)
                    self.log_widget.update()

            # Criar otimizador do Edge com logger personalizado
            progress_logger = ProgressLogger(log_text)
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

                if success and len(erros) == 0:
                    status_label.config(text="✅ Edge otimizado com sucesso!")
                    result_message = f"🎉 MICROSOFT EDGE OTIMIZADO COM SUCESSO!\n\n"
                    result_message += f"✅ {len(sucessos)} configurações aplicadas\n\n"
                    result_message += "🌍 OTIMIZAÇÕES APLICADAS:\n"
                    result_message += "• Sidebar/botão Bing desabilitado\n"
                    result_message += "• Execução em segundo plano removida\n"
                    result_message += "• Inicialização automática desabilitada\n"
                    result_message += "• Botões desnecessários removidos\n"
                    result_message += "• Privacidade melhorada\n"
                    result_message += "• Performance otimizada\n\n"
                    result_message += "⚠️ IMPORTANTE: Reinicie o Microsoft Edge para aplicar todas as mudanças!"

                    # Fechar janela de progresso após 3 segundos
                    progress_window.after(3000, progress_window.destroy)

                    messagebox.showinfo("Edge Otimizado", result_message)

                elif len(sucessos) > len(erros):
                    status_label.config(text="⚠️ Concluído com alguns avisos")
                    result_message = f"⚠️ EDGE PARCIALMENTE OTIMIZADO\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
                    result_message += (
                        "🌍 A maior parte das otimizações foi aplicada.\n\n"
                    )
                    result_message += "Detalhes dos erros:\n"
                    for erro in erros[:5]:  # Mostrar apenas os primeiros 5 erros
                        result_message += f"• {erro}\n"
                    if len(erros) > 5:
                        result_message += f"... e mais {len(erros) - 5} erros\n"
                    result_message += "\n⚠️ IMPORTANTE: Reinicie o Edge!"

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showwarning("Otimização Parcial", result_message)

                else:
                    status_label.config(text="❌ Concluído com vários erros")
                    result_message = f"❌ MUITOS ERROS NA OTIMIZAÇÃO\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"❌ Erros: {len(erros)}\n\n"
                    result_message += "Principais erros:\n"
                    for erro in erros[:3]:
                        result_message += f"• {erro}\n"
                    result_message += (
                        f"\nVerifique se está executando como Administrador!"
                    )

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showerror("Erros na Otimização", result_message)

                # Log da atividade
                self.log_activity(
                    f"Otimização do Edge: {len(sucessos)} sucessos, {len(erros)} erros"
                )

            # Agendar para thread principal
            progress_window.after(500, show_result)

        except Exception as e:

            def show_error():
                progress_bar.stop()
                status_label.config(text="❌ Erro crítico")
                progress_window.after(1000, progress_window.destroy)
                messagebox.showerror(
                    "Erro Crítico",
                    f"Erro crítico durante a otimização:\n\n{str(e)}",
                )
                self.log_activity(f"Erro crítico na otimização do Edge: {str(e)}")

            progress_window.after(0, show_error)

    # Executar em thread separada para não travar a interface
    thread = threading.Thread(target=run_edge_optimization, daemon=True)
    thread.start()

    def accelerate_windows(self):
        """Acelerar Windows usando o módulo AceleradorWindows"""

    if not self.confirm_operation(
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
    progress_window, status_label, progress_bar, log_text = self.show_progress_dialog(
        "Acelerando Windows"
    )

    def run_acceleration():
        """Executar aceleração em thread separada"""
        try:
            # Criar logger personalizado para capturar as mensagens
            class ProgressLogger:
                def __init__(self, log_widget):
                    self.log_widget = log_widget

                def log(self, message):
                    # Atualizar o log text widget de forma thread-safe
                    self.log_widget.after(0, lambda: self.update_log(message))

                def update_log(self, message):
                    self.log_widget.insert(tk.END, message + "\n")
                    self.log_widget.see(tk.END)
                    self.log_widget.update()

            # Criar acelerador com logger personalizado
            progress_logger = ProgressLogger(log_text)
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

                if success and len(erros) == 0:
                    status_label.config(text="✅ Todas as otimizações foram aplicadas!")
                    result_message = f"🎉 SUCESSO COMPLETO!\n\n"
                    result_message += (
                        f"✅ {len(sucessos)} otimizações aplicadas com sucesso\n\n"
                    )
                    result_message += "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"

                    # Fechar janela de progresso após 3 segundos
                    progress_window.after(3000, progress_window.destroy)

                    messagebox.showinfo("Otimizações Concluídas", result_message)

                elif len(sucessos) > len(erros):
                    status_label.config(text="⚠️ Concluído com alguns avisos")
                    result_message = f"⚠️ CONCLUÍDO COM AVISOS\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
                    result_message += "Detalhes dos erros:\n"
                    for erro in erros[:5]:  # Mostrar apenas os primeiros 5 erros
                        result_message += f"• {erro}\n"
                    if len(erros) > 5:
                        result_message += f"... e mais {len(erros) - 5} erros\n"
                    result_message += "\n⚠️ IMPORTANTE: Reinicie o sistema!"

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showwarning("Otimizações Concluídas", result_message)

                else:
                    status_label.config(text="❌ Concluído com vários erros")
                    result_message = f"❌ MUITOS ERROS ENCONTRADOS\n\n"
                    result_message += f"✅ Sucessos: {len(sucessos)}\n"
                    result_message += f"❌ Erros: {len(erros)}\n\n"
                    result_message += "Principais erros:\n"
                    for erro in erros[:3]:
                        result_message += f"• {erro}\n"
                    result_message += (
                        f"\nVerifique se está executando como Administrador!"
                    )

                    progress_window.after(2000, progress_window.destroy)
                    messagebox.showerror("Erros na Otimização", result_message)

                # Log da atividade
                self.log_activity(
                    f"Aceleração do Windows: {len(sucessos)} sucessos, {len(erros)} erros"
                )

            # Agendar para thread principal
            progress_window.after(500, show_result)

        except Exception as e:

            def show_error():
                progress_bar.stop()
                status_label.config(text="❌ Erro crítico")
                progress_window.after(1000, progress_window.destroy)
                messagebox.showerror(
                    "Erro Crítico",
                    f"Erro crítico durante a aceleração:\n\n{str(e)}",
                )
                self.log_activity(f"Erro crítico na aceleração: {str(e)}")

            progress_window.after(0, show_error)

    # Executar em thread separada para não travar a interface
    thread = threading.Thread(target=run_acceleration, daemon=True)
    thread.start()  # gui/optimization_tab.py - Aba de otimização NiveBoost


import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *
import winreg
import threading
import sys
import os

# Adicionar o diretório core ao path para importar o módulo
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "core"))

try:
    from core.acelerar_windows import AceleradorWindows
    from core.remover_telemetria import RemoverTelemetria
    from core.remover_features import RemoverFeatures
    from core.remover_animacoes import RemoverAnimacoes
    from core.otimizar_edge import OtimizadorEdge
    from core.desabilitar_tweaks import DesabilitadorTweaks  # NOVO MÓDULO ADICIONADO
except ImportError:
    print("Aviso: Módulos de otimização não encontrados na pasta core")
    AceleradorWindows = None
    RemoverTelemetria = None
    RemoverFeatures = None
    RemoverAnimacoes = None
    OtimizadorEdge = None
    DesabilitadorTweaks = None  # NOVO MÓDULO ADICIONADO


class OptimizationTab:
    """Classe responsável pela aba de otimização NiveBoost"""

    def __init__(self, parent_interface):
        """Inicializar aba de otimização"""
        self.parent = parent_interface
        self.system_commands = parent_interface.system_commands
        self.config = parent_interface.config
        self.logger = parent_interface.logger

    def create_optimization_tab(self, notebook):
        """Criar aba de otimização com todas as 11 opções do NiveBoost"""
        optimization_tab = ttk_bs.Frame(notebook)
        notebook.add(optimization_tab, text=f"{self.config.get_icon('zap')} Otimização")

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

        # Lista das 11 opções de otimização do NiveBoost
        optimization_options = [
            (
                "🔧 Desabilitar Alguns Serviços do Windows",
                self.disable_windows_services,
                "warning",
                "Desabilita serviços desnecessários para melhorar performance",
            ),
            (
                "📅 Desabilitar Tweaks de Tarefas Agendadas",
                self.disable_scheduled_tasks,
                "warning",
                "Remove tarefas agendadas que consomem recursos",
            ),
            (
                "💾 Desabilitar Alguns Softwares do Windows",
                self.disable_windows_software,
                "warning",
                "Desabilita aplicativos e recursos desnecessários",
            ),
            (
                "🕵️ Remover Telemetria e Coleta de Dados",
                self.remove_telemetry,
                "danger",
                "Remove sistemas de coleta de dados e telemetria",
            ),
            (
                "🗑️ Remover Features Não Usadas",
                self.remove_unused_features,
                "warning",
                "Remove recursos e funcionalidades não utilizadas",
            ),
            (
                "🎨 Remover Animações Inúteis",
                self.remove_animations,
                "info",
                "Remove animações para melhorar a responsividade",
            ),
            (
                "🔍 Desabilitar Busca Web na Barra de Pesquisa",
                self.disable_web_search,
                "info",
                "Desabilita busca online na barra de pesquisa do Windows",
            ),
            (
                "🌐 Desabilitar Cache de Navegadores e Streaming",
                self.disable_browser_cache,
                "warning",
                "Otimiza cache de navegadores e serviços de streaming",
            ),
            (
                "🔒 Desabilitar Propagandas na Tela de Bloqueio",
                self.disable_lock_screen_ads,
                "success",
                "Remove propagandas e sugestões da tela de bloqueio",
            ),
            (
                "🌍 Otimizar o Edge",
                self.optimize_edge,
                "primary",
                "Aplica otimizações específicas para o Microsoft Edge",
            ),
            (
                "⚡Acelerar Windows",
                self.accelerate_windows,
                "success",
                "Aplicação geral de otimizações para acelerar o sistema",
            ),
        ]

        # Criar botões em lista vertical
        for i, (text, command, style, description) in enumerate(optimization_options):
            # Frame para cada opção
            option_frame = ttk_bs.Frame(optimization_frame)
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

        # Aviso importante
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

        return optimization_tab

    def confirm_operation(self, title, message):
        """Método auxiliar para confirmar operações"""
        return messagebox.askyesno(title, message)

    def show_progress_dialog(self, title="Executando Otimização"):
        """Criar janela de progresso"""
        progress_window = tk.Toplevel(self.parent.root)
        progress_window.title(title)
        progress_window.geometry("400x200")
        progress_window.transient(self.parent.root)
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

    def update_log_text(self, log_text, message):
        """Atualizar texto do log de forma thread-safe"""

        def update():
            log_text.insert(tk.END, message + "\n")
            log_text.see(tk.END)
            log_text.update()

        # Agendar atualização na thread principal
        log_text.after(0, update)

    def execute_optimization(self, optimization_type):
        """Executar otimização específica (método genérico para funções não implementadas)"""
        try:
            messagebox.showinfo(
                "Em Desenvolvimento",
                f"A otimização '{optimization_type}' será implementada em breve.\n\n"
                "Os scripts .bat correspondentes precisam ser convertidos para Python.",
            )
            self.log_activity(f"Tentativa de execução: {optimization_type}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar otimização: {str(e)}")
            self.log_activity(f"Erro em {optimization_type}: {str(e)}")

    def log_activity(self, message):
        """Registrar atividade no log"""
        if hasattr(self, "logger") and self.logger:
            self.logger.log(message)

    # Métodos das 11 opções de otimização
    def disable_windows_services(self):
        if self.confirm_operation(
            "Desabilitar Serviços do Windows",
            "Esta operação irá desabilitar serviços desnecessários do Windows.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
            "Deseja continuar?",
        ):
            self.execute_optimization("disable_services")

    def disable_scheduled_tasks(self):
        """Desabilitar Tarefas Agendadas usando o módulo DesabilitadorTweaks"""
        if not self.confirm_operation(
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
            self.show_progress_dialog("Desabilitando Tarefas Agendadas")
        )

        def run_scheduled_tasks_disable():
            """Executar desabilitação de tarefas em thread separada"""
            try:
                # Criar logger personalizado para capturar as mensagens
                class ProgressLogger:
                    def __init__(self, log_widget):
                        self.log_widget = log_widget

                    def log(self, message):
                        # Atualizar o log text widget de forma thread-safe
                        self.log_widget.after(0, lambda: self.update_log(message))

                    def update_log(self, message):
                        self.log_widget.insert(tk.END, message + "\n")
                        self.log_widget.see(tk.END)
                        self.log_widget.update()

                # Criar desabilitador com logger personalizado
                progress_logger = ProgressLogger(log_text)
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

                    if success and len(erros) == 0:
                        status_label.config(
                            text="✅ Tarefas desabilitadas com sucesso!"
                        )
                        result_message = (
                            f"🎉 TAREFAS AGENDADAS DESABILITADAS COM SUCESSO!\n\n"
                        )
                        result_message += f"✅ {len(sucessos)} tarefas processadas\n\n"
                        result_message += "📅 TAREFAS DESABILITADAS:\n"
                        result_message += "• Telemetria e coleta de dados removida\n"
                        result_message += "• Customer Experience Program desabilitado\n"
                        result_message += "• Diagnósticos automáticos parados\n"
                        result_message += (
                            "• Atualizações automáticas do Office/Edge desabilitadas\n"
                        )
                        result_message += "• Tarefas de manutenção otimizadas\n\n"
                        result_message += "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"

                        # Fechar janela de progresso após 3 segundos
                        progress_window.after(3000, progress_window.destroy)

                        messagebox.showinfo("Tarefas Desabilitadas", result_message)

                    elif len(sucessos) > len(erros):
                        status_label.config(text="⚠️ Concluído com alguns avisos")
                        result_message = f"⚠️ TAREFAS PARCIALMENTE DESABILITADAS\n\n"
                        result_message += f"✅ Sucessos: {len(sucessos)}\n"
                        result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
                        result_message += (
                            "📅 A maior parte das tarefas foi desabilitada.\n\n"
                        )
                        result_message += "Detalhes dos erros:\n"
                        for erro in erros[:5]:  # Mostrar apenas os primeiros 5 erros
                            result_message += f"• {erro}\n"
                        if len(erros) > 5:
                            result_message += f"... e mais {len(erros) - 5} erros\n"
                        result_message += "\n⚠️ IMPORTANTE: Reinicie o sistema!"

                        progress_window.after(2000, progress_window.destroy)
                        messagebox.showwarning("Desabilitação Parcial", result_message)

                    else:
                        status_label.config(text="❌ Concluído com vários erros")
                        result_message = f"❌ MUITOS ERROS NA DESABILITAÇÃO\n\n"
                        result_message += f"✅ Sucessos: {len(sucessos)}\n"
                        result_message += f"❌ Erros: {len(erros)}\n\n"
                        result_message += "Principais erros:\n"
                        for erro in erros[:3]:
                            result_message += f"• {erro}\n"
                        result_message += (
                            f"\nVerifique se está executando como Administrador!"
                        )

                        progress_window.after(2000, progress_window.destroy)
                        messagebox.showerror("Erros na Desabilitação", result_message)

                    # Log da atividade
                    self.log_activity(
                        f"Desabilitação de tarefas: {len(sucessos)} sucessos, {len(erros)} erros"
                    )

                # Agendar para thread principal
                progress_window.after(500, show_result)

            except Exception as e:

                def show_error():
                    progress_bar.stop()
                    status_label.config(text="❌ Erro crítico")
                    progress_window.after(1000, progress_window.destroy)
                    messagebox.showerror(
                        "Erro Crítico",
                        f"Erro crítico durante a desabilitação:\n\n{str(e)}",
                    )
                    self.log_activity(
                        f"Erro crítico na desabilitação de tarefas: {str(e)}"
                    )

                progress_window.after(0, show_error)

        # Executar em thread separada para não travar a interface
        thread = threading.Thread(target=run_scheduled_tasks_disable, daemon=True)
        thread.start()

    def disable_windows_software(self):
        if self.confirm_operation(
            "Desabilitar Softwares do Windows",
            "Esta operação irá desabilitar aplicativos e softwares desnecessários.\n\n"
            "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!\n\n"
            "Deseja continuar?",
        ):
            self.execute_optimization("disable_windows_software")
