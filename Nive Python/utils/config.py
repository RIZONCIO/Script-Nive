import os
from pathlib import Path


class Config:
    """Classe de configurações da aplicação"""

    def __init__(self):
        """Inicializar configurações"""
        # Versão da aplicação
        self.version = "1.6.8"

        # Configurações da janela
        self.window_width = 950
        self.window_height = 750
        self.theme = "superhero"  # Tema do ttkbootstrap

        # Caminhos
        self.base_path = Path(__file__).parent.parent
        self.icon_path = self.base_path / "assets" / "icon.ico"
        self.logs_path = self.base_path / "logs"

        # Criar diretórios se não existirem
        self._create_directories()

        # Configurações dos comandos
        self.commands = {
            "recycle_bin": "rd /S /Q c:\\$Recycle.bin",
            "godmode_folder": "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}",
            "disk_check": {
                "status_check": "WMIC diskdrive get status",
                "model_status": "WMIC diskdrive get model,status",
                "check_repair": "CHKDSK /R",
                "shutdown": "shutdown -r -t 30",
            },
            "memory_check": "mdsched",
            "system_repair": [
                "sfc /scannow",
                "Dism /Online /Cleanup-Image /ScanHealth",
                "Dism /Online /Cleanup-Image /RestoreHealth",
                "shutdown -r -t 30",
            ],
            "temp_cleanup": [
                'del /q /f /s "%temp%\\*"',
                'del /q/f/s "C:\\Windows\\Temp\\*"',
                'del /q /f /s "%windir%\\Prefetch\\*"',
                'del /q /f /s "%appdata%\\Microsoft\\Windows\\Recent\\*"',
            ],
            "dns_cleanup": [
                "netsh winsock reset",
                "netsh int ip reset",
                "ipconfig /release",
                "ipconfig /renew",
                "ipconfig /flushdns",
                "ipconfig /registerdns",
            ],
            "audio_repair": [
                "net stop audiosrv",
                "timeout /t 5",
                "net start audiosrv",
                "net start AudioEndpointBuilder",
                "net start wuauserv",
            ],
            "diagnostics": "perfmon /rel",
            "mrt": "powershell.exe -command \"Start-Process 'C:\\Windows\\System32\\MRT.exe'\"",
        }

        # URLs e links
        self.links = {
            "microsoft_docs": "https://docs.microsoft.com/pt-br/windows-server/administration/windows-commands/cmd",
            "dos_tips": "https://www.dostips.com/",
            "github": "https://github.com/RIZONCIO/Script-Nive",
            "text_image": "https://www.text-image.com/",
        }

        # Símbolos de ícones Unicode
        self.icons = {
            "trash": "🗑",
            "settings": "⚙",
            "hard_drive": "💾",
            "cpu": "🧠",
            "wrench": "🔧",
            "broom": "🧹",
            "wifi": "🌐",
            "control_panel": "⚙",
            "activity": "📊",
            "shield": "🛡",
            "package": "📦",
            "volume": "🔊",
            "download": "⬇",
            "folder_x": "🗂",
            "tool": "🛠",
            "zap": "⚡",
            "info": "ℹ",
            "clipboard": "📋",
            "clean": "✨",
            "folder": "📁",
            "home": "🏠",
            "system": "💻",
            "tools": "🔧",
            "about": "❓",
            "save": "💾",
            "success": "✅",
            "error": "❌",
            "warning": "⚠",
            "loading": "⏳",
        }

    def _create_directories(self):
        """Criar diretórios necessários"""

    def get_icon(self, icon_name):
        """Obter ícone por nome"""
        return self.icons.get(icon_name, "•")

    def get_command(self, command_name):
        """Obter comando por nome"""
        return self.commands.get(command_name)

    def get_link(self, link_name):
        """Obter link por nome"""
        return self.links.get(link_name)
