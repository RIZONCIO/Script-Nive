# core/disable_software.py - Desabilitar alguns softwares do Windows

import subprocess
import os
import sys
from typing import Dict, List, Tuple, Optional


class DisableSoftware:
    """Classe para desabilitar/remover softwares desnecessários do Windows"""

    def __init__(self, logger=None):
        """Inicializar com logger opcional"""
        self.logger = logger
        self.results = []

    def log(self, message: str, level: str = "INFO"):
        """Log de mensagens"""
        if self.logger:
            if level == "ERROR":
                self.logger.error(message)
            else:
                self.logger.info(message)
        else:
            print(f"[{level}] {message}")

    def executar_desabilitacao_softwares(self):
        sucessos = []
        erros = []
        softwares = [
            "OneDrive",
            "Cortana",
            "XboxApp",
            "Apps Store",
            "Cortana",
            "Microsoft Edge",
            "Vínculo com celular",
            "Paint",
            "Hibernação",
        ]

        for software in softwares:
            try:
                self.log(f"Desabilitando {software}...")
                subprocess.run(
                    [
                        "powershell",
                        "Get-AppxPackage",
                        software,
                        "|",
                        "Remove-AppxPackage",
                    ],
                    check=True,
                )
                sucessos.append(software)
            except Exception as e:
                erros.append((software, str(e)))
                self.log(f"Erro ao desabilitar {software}: {e}")

        success = len(erros) == 0
        return success, sucessos, erros

    def run_command(
        self, command: str, shell: bool = True, ignore_errors: bool = False
    ) -> Tuple[bool, str]:
        """Executar comando do sistema"""
        try:
            self.log(f"Executando: {command}")

            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos timeout
            )

            if result.returncode == 0 or ignore_errors:
                self.log(f"Sucesso: {command}")
                return True, result.stdout
            else:
                self.log(f"Erro ao executar: {command} - {result.stderr}", "ERROR")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            self.log(f"Timeout ao executar: {command}", "ERROR")
            return False, "Timeout"
        except Exception as e:
            self.log(f"Exceção ao executar {command}: {str(e)}", "ERROR")
            return False, str(e)

    def disable_hibernation(self) -> bool:
        """Desativar modo hibernação"""
        self.log("Desativando modo hibernação...")
        success, output = self.run_command("powercfg -h off")

        if success:
            self.results.append("✓ Modo hibernação desativado")
            return True
        else:
            self.results.append("✗ Falha ao desativar hibernação")
            return False

    def uninstall_paint(self) -> bool:
        """Desinstalar Paint"""
        self.log("Desinstalando Paint...")
        success, output = self.run_command(
            "winget uninstall 9PCFS5B6T72H", ignore_errors=True
        )

        if success:
            self.results.append("✓ Paint desinstalado")
            return True
        else:
            self.results.append("✗ Falha ao desinstalar Paint (pode já estar removido)")
            return False

    def uninstall_phone_link(self) -> bool:
        """Desinstalar Vínculo com celular"""
        self.log("Desinstalando Vínculo com celular...")
        command = r'winget uninstall "MSIX\Microsoft.YourPhone_1.24062.101.0_x64__8wekyb3d8bbwe"'
        success, output = self.run_command(command, ignore_errors=True)

        if success:
            self.results.append("✓ Vínculo com celular desinstalado")
            return True
        else:
            self.results.append("✗ Falha ao desinstalar Vínculo com celular")
            return False

    def uninstall_edge(self) -> bool:
        """Desinstalar Microsoft Edge completamente"""
        self.log("Desinstalando Microsoft Edge...")

        edge_commands = [
            "winget uninstall Microsoft.Edge",
            r'winget uninstall "ARP\Machine\X86\Microsoft Edge Update"',
            "winget uninstall Microsoft.EdgeWebView2Runtime",
            r'winget uninstall "MSIX\Microsoft.MicrosoftEdge.Stable_126.0.2592.113_neutral__8we"',
        ]

        success_count = 0
        for cmd in edge_commands:
            success, output = self.run_command(cmd, ignore_errors=True)
            if success:
                success_count += 1

        if success_count > 0:
            self.results.append(
                f"✓ Microsoft Edge removido ({success_count}/4 componentes)"
            )
            return True
        else:
            self.results.append("✗ Falha ao remover Microsoft Edge")
            return False

    def uninstall_cortana(self) -> bool:
        """Desinstalar COMPLETAMENTE a Cortana"""
        self.log("Desinstalando Cortana...")

        powershell_cmd = (
            "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "
            '"Get-AppxPackage -allusers Microsoft.549981C3F5F10 | Remove-AppxPackage"'
        )

        success, output = self.run_command(powershell_cmd, ignore_errors=True)

        if success:
            self.results.append("✓ Cortana desinstalada")
            return True
        else:
            self.results.append(
                "✗ Falha ao desinstalar Cortana (pode já estar removida)"
            )
            return False

    def uninstall_onedrive(self) -> bool:
        """Remoção completa do OneDrive"""
        self.log("Removendo OneDrive...")

        # Comandos para remover OneDrive
        onedrive_commands = [
            r'winget uninstall "MSIX\Microsoft.OneDriveSync_24116.609.5.0_neutral__8wekyb3d8bbwe"',
            "winget uninstall Microsoft.OneDrive",
            "taskkill /f /im OneDrive.exe",
            r"%SystemRoot%\System32\OneDriveSetup.exe /uninstall",
            r"%SystemRoot%\SysWOW64\OneDriveSetup.exe /uninstall",
        ]

        success_count = 0
        for cmd in onedrive_commands:
            success, output = self.run_command(cmd, ignore_errors=True)
            if success:
                success_count += 1

        if success_count > 0:
            self.results.append(f"✓ OneDrive removido ({success_count}/5 operações)")
            return True
        else:
            self.results.append("✗ Falha ao remover OneDrive")
            return False

    def remove_store_apps(self) -> bool:
        """Remoção de Apps da Store (mantendo essenciais)"""
        self.log("Removendo Apps da Store desnecessários...")

        powershell_cmd = (
            "Powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "
            "\"Get-AppxPackage | where-object {$_.name -notlike '*GamingApp*'} | "
            "where-object {$_.name -notlike '*Winget*'} | "
            "where-object {$_.name -notlike '*store*'} | "
            "where-object {$_.name -notlike '*DesktopAppInstaller*'} | "
            "where-object {$_.name -notlike '*xbox*'} | "
            "where-object {$_.name -notlike '*terminal*'} | Remove-AppxPackage\""
        )

        success, output = self.run_command(powershell_cmd, ignore_errors=True)

        if success:
            self.results.append("✓ Apps da Store desnecessários removidos")
            return True
        else:
            self.results.append("✗ Falha ao remover Apps da Store")
            return False

    def execute_all(self) -> Dict[str, bool]:
        """Executar todas as operações de remoção"""
        self.log("Iniciando remoção de softwares desnecessários...")
        self.results = []

        operations = {
            "hibernation": self.disable_hibernation,
            "paint": self.uninstall_paint,
            "phone_link": self.uninstall_phone_link,
            "edge": self.uninstall_edge,
            "cortana": self.uninstall_cortana,
            "onedrive": self.uninstall_onedrive,
            "store_apps": self.remove_store_apps,
        }

        results = {}

        for name, operation in operations.items():
            try:
                results[name] = operation()
            except Exception as e:
                self.log(f"Erro na operação {name}: {str(e)}", "ERROR")
                results[name] = False
                self.results.append(f"✗ Erro em {name}: {str(e)}")

        self.log("Operações de remoção concluídas!")
        return results

    def get_results_summary(self) -> List[str]:
        """Obter resumo dos resultados"""
        return self.results.copy()


def main():
    """Função principal para execução standalone"""
    print("NiveBoost - Desabilitador de Software v1.0")
    print("=" * 50)

    disabler = DisableSoftware()
    results = disabler.execute_all()

    print("\nResumo das operações:")
    print("-" * 30)
    for result in disabler.get_results_summary():
        print(result)

    successful = sum(1 for success in results.values() if success)
    total = len(results)

    print(f"\nOperações bem-sucedidas: {successful}/{total}")

    if successful == total:
        print("✓ Todas as operações foram executadas com sucesso!")
    elif successful > 0:
        print("⚠ Algumas operações falharam, mas outras foram bem-sucedidas")
    else:
        print("✗ Todas as operações falharam")


if __name__ == "__main__":
    main()
