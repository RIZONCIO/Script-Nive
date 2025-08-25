# gui/optimization_results.py - Métodos para exibir resultados das otimizações

from tkinter import messagebox


class OptimizationResults:
    """Classe responsável por exibir os resultados das otimizações"""

    def __init__(self, optimization_handlers):
        """Inicializar classe de resultados"""
        self.handlers = optimization_handlers

    def show_telemetry_result(
        self, progress_window, status_label, success, sucessos, erros
    ):
        """Exibir resultado da remoção de telemetria"""
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
            result_message += (
                "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"
            )

            progress_window.after(3000, progress_window.destroy)
            messagebox.showinfo("Telemetria Removida", result_message)

        elif len(sucessos) > len(erros):
            status_label.config(text="⚠️ Concluído com alguns avisos")
            result_message = f"⚠️ TELEMETRIA PARCIALMENTE REMOVIDA\n\n"
            result_message += f"✅ Sucessos: {len(sucessos)}\n"
            result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
            result_message += "🔒 A maior parte da telemetria foi desabilitada.\n\n"
            result_message += "Detalhes dos erros:\n"
            for erro in erros[:5]:
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
            result_message += "\nVerifique se está executando como Administrador!"

            progress_window.after(2000, progress_window.destroy)
            messagebox.showerror("Erros na Remoção", result_message)

        # Log da atividade
        self.handlers.parent.log_activity(
            f"Remoção de telemetria: {len(sucessos)} sucessos, {len(erros)} erros"
        )

    def show_features_result(
        self, progress_window, status_label, success, sucessos, erros
    ):
        """Exibir resultado da remoção de features"""
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
            result_message += (
                "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"
            )

            progress_window.after(3000, progress_window.destroy)
            messagebox.showinfo("Features Removidas", result_message)

        elif len(sucessos) > len(erros):
            status_label.config(text="⚠️ Concluído com alguns avisos")
            result_message = f"⚠️ FEATURES PARCIALMENTE REMOVIDAS\n\n"
            result_message += f"✅ Sucessos: {len(sucessos)}\n"
            result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
            result_message += "🗑️ A maior parte das features foi removida.\n\n"
            result_message += "Detalhes dos erros:\n"
            for erro in erros[:5]:
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
            result_message += "\nVerifique se está executando como Administrador!"

            progress_window.after(2000, progress_window.destroy)
            messagebox.showerror("Erros na Remoção", result_message)

        # Log da atividade
        self.handlers.parent.log_activity(
            f"Remoção de features: {len(sucessos)} sucessos, {len(erros)} erros"
        )

    def show_animations_result(
        self, progress_window, status_label, success, sucessos, erros
    ):
        """Exibir resultado da remoção de animações"""
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

            progress_window.after(3000, progress_window.destroy)
            messagebox.showinfo("Animações Removidas", result_message)

        elif len(sucessos) > len(erros):
            status_label.config(text="⚠️ Concluído com alguns avisos")
            result_message = f"⚠️ ANIMAÇÕES PARCIALMENTE REMOVIDAS\n\n"
            result_message += f"✅ Sucessos: {len(sucessos)}\n"
            result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
            result_message += "🎨 A maior parte das animações foi desabilitada.\n\n"
            result_message += "Detalhes dos erros:\n"
            for erro in erros[:5]:
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
            result_message += "\nVerifique se está executando como Administrador!"

            progress_window.after(2000, progress_window.destroy)
            messagebox.showerror("Erros na Remoção", result_message)

        # Log da atividade
        self.handlers.parent.log_activity(
            f"Remoção de animações: {len(sucessos)} sucessos, {len(erros)} erros"
        )

    def show_edge_result(self, progress_window, status_label, success, sucessos, erros):
        """Exibir resultado da otimização do Edge"""
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

            progress_window.after(3000, progress_window.destroy)
            messagebox.showinfo("Edge Otimizado", result_message)

        elif len(sucessos) > len(erros):
            status_label.config(text="⚠️ Concluído com alguns avisos")
            result_message = f"⚠️ EDGE PARCIALMENTE OTIMIZADO\n\n"
            result_message += f"✅ Sucessos: {len(sucessos)}\n"
            result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
            result_message += "🌍 A maior parte das otimizações foi aplicada.\n\n"
            result_message += "Detalhes dos erros:\n"
            for erro in erros[:5]:
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
            result_message += "\nVerifique se está executando como Administrador!"

            progress_window.after(2000, progress_window.destroy)
            messagebox.showerror("Erros na Otimização", result_message)

        # Log da atividade
        self.handlers.parent.log_activity(
            f"Otimização do Edge: {len(sucessos)} sucessos, {len(erros)} erros"
        )

    def show_acceleration_result(
        self, progress_window, status_label, success, sucessos, erros
    ):
        """Exibir resultado da aceleração do Windows"""
        if success and len(erros) == 0:
            status_label.config(text="✅ Todas as otimizações foram aplicadas!")
            result_message = f"🎉 SUCESSO COMPLETO!\n\n"
            result_message += (
                f"✅ {len(sucessos)} otimizações aplicadas com sucesso\n\n"
            )
            result_message += (
                "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"
            )

            progress_window.after(3000, progress_window.destroy)
            messagebox.showinfo("Otimizações Concluídas", result_message)

        elif len(sucessos) > len(erros):
            status_label.config(text="⚠️ Concluído com alguns avisos")
            result_message = f"⚠️ CONCLUÍDO COM AVISOS\n\n"
            result_message += f"✅ Sucessos: {len(sucessos)}\n"
            result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
            result_message += "Detalhes dos erros:\n"
            for erro in erros[:5]:
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
            result_message += "\nVerifique se está executando como Administrador!"

            progress_window.after(2000, progress_window.destroy)
            messagebox.showerror("Erros na Otimização", result_message)

        # Log da atividade
        self.handlers.parent.log_activity(
            f"Aceleração do Windows: {len(sucessos)} sucessos, {len(erros)} erros"
        )

    def show_tasks_result(
        self, progress_window, status_label, success, sucessos, erros
    ):
        """Exibir resultado da desabilitação de tarefas"""
        if success and len(erros) == 0:
            status_label.config(text="✅ Tarefas desabilitadas com sucesso!")
            result_message = f"🎉 TAREFAS AGENDADAS DESABILITADAS COM SUCESSO!\n\n"
            result_message += f"✅ {len(sucessos)} tarefas processadas\n\n"
            result_message += "📅 TAREFAS DESABILITADAS:\n"
            result_message += "• Telemetria e coleta de dados removida\n"
            result_message += "• Customer Experience Program desabilitado\n"
            result_message += "• Diagnósticos automáticos parados\n"
            result_message += (
                "• Atualizações automáticas do Office/Edge desabilitadas\n"
            )
            result_message += "• Tarefas de manutenção otimizadas\n\n"
            result_message += (
                "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"
            )

            progress_window.after(3000, progress_window.destroy)
            messagebox.showinfo("Tarefas Desabilitadas", result_message)

        elif len(sucessos) > len(erros):
            status_label.config(text="⚠️ Concluído com alguns avisos")
            result_message = f"⚠️ TAREFAS PARCIALMENTE DESABILITADAS\n\n"
            result_message += f"✅ Sucessos: {len(sucessos)}\n"
            result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
            result_message += "📅 A maior parte das tarefas foi desabilitada.\n\n"
            result_message += "Detalhes dos erros:\n"
            for erro in erros[:5]:
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
            result_message += "\nVerifique se está executando como Administrador!"

            progress_window.after(2000, progress_window.destroy)
            messagebox.showerror("Erros na Desabilitação", result_message)

        # Log da atividade
        self.handlers.parent.log_activity(
            f"Desabilitação de tarefas: {len(sucessos)} sucessos, {len(erros)} erros"
        )

    def show_disable_software_result(
        self, progress_window, status_label, success, sucessos, erros
    ):
        """Exibir resultado da desabilitação de softwares"""
        if success and len(erros) == 0:
            status_label.config(text="✅ Softwares desabilitados com sucesso!")
            result_message = f"🎉 SOFTWARES DESABILITADOS COM SUCESSO!\n\n"
            result_message += f"✅ {len(sucessos)} softwares processados\n\n"
            result_message += "💻 SOFTWARES DESABILITADOS:\n"
            result_message += "• Aplicativos desnecessários removidos\n"
            result_message += "• Softwares em segundo plano desabilitados\n"
            result_message += "• Recursos de sistema otimizados\n"
            result_message += "• Performance melhorada\n"
            result_message += "• Consumo de recursos reduzido\n\n"
            result_message += (
                "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"
            )

            progress_window.after(3000, progress_window.destroy)
            messagebox.showinfo("Softwares Desabilitados", result_message)

        elif len(sucessos) > len(erros):
            status_label.config(text="⚠️ Concluído com alguns avisos")
            result_message = f"⚠️ SOFTWARES PARCIALMENTE DESABILITADOS\n\n"
            result_message += f"✅ Sucessos: {len(sucessos)}\n"
            result_message += f"⚠️ Avisos/Erros: {len(erros)}\n\n"
            result_message += "💻 A maior parte dos softwares foi desabilitada.\n\n"
            result_message += "Detalhes dos erros:\n"
            for erro in erros[:5]:
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
            result_message += "\nVerifique se está executando como Administrador!"

            progress_window.after(2000, progress_window.destroy)
            messagebox.showerror("Erros na Desabilitação", result_message)

        # Log da atividade
        self.handlers.parent.log_activity(
            f"Desabilitação de softwares: {len(sucessos)} sucessos, {len(erros)} erros"
        )
