"""
Sistema de Log para ScriptNive
utils/logger.py
"""

import os
import tkinter as tk
from datetime import datetime
from pathlib import Path


class Logger:
    """Classe para gerenciar logs da aplicação"""

    def __init__(self, log_widget=None):
        """Inicializar logger"""
        self.log_widget = log_widget
        self.log_file = (
            Path("logs") / f"scriptnive_{datetime.now().strftime('%Y%m%d')}.log"
        )

        # Criar diretório de logs se não existir
        self.log_file.parent.mkdir(exist_ok=True)

        # Lista para armazenar logs na memória
        self.memory_logs = []

    def set_widget(self, widget):
        """Definir widget de texto para exibir logs"""
        self.log_widget = widget

    def log(self, message, level="INFO"):
        """Adicionar mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"

        # Adicionar à memória
        self.memory_logs.append(log_entry)

        # Exibir no widget se disponível
        if self.log_widget:
            try:
                self.log_widget.insert(tk.END, log_entry + "\n")
                self.log_widget.see(tk.END)
                self.log_widget.update_idletasks()
            except:
                pass

        # Salvar no arquivo
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Erro ao salvar log: {e}")

    def log_success(self, message):
        """Log de sucesso"""
        self.log(f"✅ {message}", "SUCCESS")

    def log_error(self, message):
        """Log de erro"""
        self.log(f"❌ {message}", "ERROR")

    def log_warning(self, message):
        """Log de aviso"""
        self.log(f"⚠ {message}", "WARNING")

    def log_info(self, message):
        """Log de informação"""
        self.log(f"ℹ {message}", "INFO")

    def clear_widget(self):
        """Limpar widget de log"""
        if self.log_widget:
            try:
                self.log_widget.delete(1.0, tk.END)
            except:
                pass

    def get_all_logs(self):
        """Obter todos os logs da memória"""
        return "\n".join(self.memory_logs)

    def save_logs_to_file(self, file_path):
        """Salvar logs em arquivo específico"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.get_all_logs())
            return True
        except Exception as e:
            self.log_error(f"Erro ao salvar logs: {e}")
            return False
