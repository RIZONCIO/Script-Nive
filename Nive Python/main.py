import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk_bs
from interface import ScriptNiveInterface
from core.system_commands import SystemCommands
from utils.logger import Logger
from utils.config import Config


class ScriptNiveGUI:
    """Classe principal da aplicação ScriptNive GUI"""

    def __init__(self):
        """Inicializar aplicação"""
        try:
            # Carregar configurações
            self.config = Config()

            # Configurar logger
            self.logger = Logger()

            # Inicializar comandos do sistema
            self.system_commands = SystemCommands(self.logger)

            # Criar janela principal
            self.root = ttk_bs.Window(themename=self.config.theme)
            self.setup_window()

            # Criar interface
            self.interface = ScriptNiveInterface(
                self.root, self.system_commands, self.logger, self.config
            )

            # Configurar eventos de fechamento
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        except Exception as e:
            messagebox.showerror(
                "Erro de Inicialização", f"Erro ao inicializar aplicação:\n{str(e)}"
            )
            raise

    def setup_window(self):
        """Configurar janela principal"""
        self.root.title(f"ScriptNive {self.config.version} - Interface Gráfica")
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.resizable(True, True)

        # Centralizar janela
        self.center_window()

        # Configurar ícone (se disponível)
        try:
            self.root.iconbitmap(self.config.icon_path)
        except:
            pass

    def center_window(self):
        """Centralizar janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def on_closing(self):
        """Manipular fechamento da aplicação"""
        try:
            self.logger.log("Aplicação fechada pelo usuário")
            self.root.destroy()
        except:
            pass

    def run(self):
        """Executar aplicação"""
        try:
            self.logger.log("ScriptNive GUI iniciado")
            self.root.mainloop()
        except Exception as e:
            self.logger.log(f"Erro durante execução: {str(e)}")
            messagebox.showerror("Erro", f"Erro durante execução:\n{str(e)}")


def main():
    """Função principal"""
    try:
        app = ScriptNiveGUI()
        app.run()
    except ImportError as e:
        if "ttkbootstrap" in str(e):
            messagebox.showerror(
                "Erro de Dependência",
                "ttkbootstrap não está instalado.\n\nPara instalar:\npip install ttkbootstrap",
            )
        else:
            messagebox.showerror(
                "Erro de Dependência", f"Dependência não encontrada:\n{str(e)}"
            )
    except Exception as e:
        messagebox.showerror(
            "Erro Crítico", f"Erro crítico ao iniciar aplicação:\n{str(e)}"
        )


if __name__ == "__main__":
    main()
