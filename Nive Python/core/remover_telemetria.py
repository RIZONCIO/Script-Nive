# core/remover_telemetria.py - Remoção de telemetria e coleta de dados do Windows
# Conversão do arquivo RemoverTelemetria.bat

import winreg
import ctypes
from typing import List, Tuple, Optional


class RemoverTelemetria:
    """Classe para remover telemetria e sistemas de coleta de dados do Windows"""

    def __init__(self, logger=None):
        self.logger = logger
        self.errors = []
        self.successes = []

    def log(self, message: str):
        """Log das ações realizadas"""
        if self.logger:
            self.logger.log(message)
        print(message)

    def is_admin(self) -> bool:
        """Verifica se o script está rodando como administrador"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def add_registry_key(
        self,
        hive: int,
        key_path: str,
        value_name: str,
        value_type: int,
        value_data,
        description: str = "",
    ) -> bool:
        """Adiciona/modifica uma chave do registro"""
        try:
            with winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                self.log(f"✓ {description}: {key_path}\\{value_name}")
                self.successes.append(description)
                return True
        except FileNotFoundError:
            # Tenta criar a chave se não existir
            try:
                with winreg.CreateKey(hive, key_path) as key:
                    winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    self.log(
                        f"✓ {description} (chave criada): {key_path}\\{value_name}"
                    )
                    self.successes.append(description)
                    return True
            except Exception as e:
                self.log(f"✗ Erro ao criar {description}: {str(e)}")
                self.errors.append(f"{description}: {str(e)}")
                return False
        except Exception as e:
            self.log(f"✗ Erro em {description}: {str(e)}")
            self.errors.append(f"{description}: {str(e)}")
            return False

    def desabilitar_metadata_rede(self) -> bool:
        """Desabilitar metadados de dispositivo da rede"""
        self.log("\n--- Desabilitando Metadados de Dispositivo ---")

        return self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Device Metadata",
            "PreventDeviceMetadataFromNetwork",
            winreg.REG_DWORD,
            1,
            "Impedir metadados de dispositivo da rede",
        )

    def desabilitar_telemetria_principal(self) -> bool:
        """Desabilitar telemetria principal do Windows"""
        self.log("\n--- Desabilitando Telemetria Principal ---")
        success = True

        # Telemetria principal (64-bit)
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection",
            "AllowTelemetry",
            winreg.REG_DWORD,
            0,
            "Desabilitar telemetria (64-bit)",
        )

        # Telemetria para aplicações 32-bit no Windows 64-bit
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\DataCollection",
            "AllowTelemetry",
            winreg.REG_DWORD,
            0,
            "Desabilitar telemetria (32-bit)",
        )

        # Telemetria adicional via Policies
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "AllowTelemetry",
            winreg.REG_DWORD,
            0,
            "Desabilitar telemetria via políticas",
        )

        return success

    def desabilitar_malicious_removal_tool(self) -> bool:
        """Desabilitar ofertas do Malicious Software Removal Tool via Windows Update"""
        self.log("\n--- Desabilitando MRT via Windows Update ---")

        return self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Policies\Microsoft\MRT",
            "DontOfferThroughWUAU",
            winreg.REG_DWORD,
            1,
            "Não oferecer MRT via Windows Update",
        )

    def desabilitar_ceip(self) -> bool:
        """Desabilitar Customer Experience Improvement Program (CEIP)"""
        self.log("\n--- Desabilitando CEIP ---")
        success = True

        # CEIP via Policies
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Policies\Microsoft\SQMClient\Windows",
            "CEIPEnable",
            winreg.REG_DWORD,
            0,
            "Desabilitar CEIP via políticas",
        )

        # CEIP direto
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\SQMClient\Windows",
            "CEIPEnable",
            winreg.REG_DWORD,
            0,
            "Desabilitar CEIP diretamente",
        )

        return success

    def desabilitar_app_compat(self) -> bool:
        """Desabilitar Application Compatibility tracking"""
        self.log("\n--- Desabilitando Application Compatibility ---")
        success = True

        # Desabilitar Application Impact Telemetry
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Policies\Microsoft\Windows\AppCompat",
            "AITEnable",
            winreg.REG_DWORD,
            0,
            "Desabilitar Application Impact Telemetry",
        )

        # Desabilitar User Activity Reporting
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Policies\Microsoft\Windows\AppCompat",
            "DisableUAR",
            winreg.REG_DWORD,
            1,
            "Desabilitar User Activity Reporting",
        )

        return success

    def desabilitar_auto_loggers(self) -> bool:
        """Desabilitar AutoLoggers de diagnóstico"""
        self.log("\n--- Desabilitando AutoLoggers ---")
        success = True

        # Desabilitar Diagtrack Listener
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\AutoLogger-Diagtrack-Listener",
            "Start",
            winreg.REG_DWORD,
            0,
            "Desabilitar AutoLogger Diagtrack",
        )

        # Desabilitar SQM Logger
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\WMI\AutoLogger\SQMLogger",
            "Start",
            winreg.REG_DWORD,
            0,
            "Desabilitar SQM Logger",
        )

        return success

    def desabilitar_smartscreen(self) -> bool:
        """Desabilitar Windows SmartScreen"""
        self.log("\n--- Desabilitando Windows SmartScreen ---")
        success = True

        # SmartScreen global (HKLM)
        success &= self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer",
            "SmartScreenEnabled",
            winreg.REG_SZ,
            "Off",
            "Desabilitar SmartScreen globalmente",
        )

        # SmartScreen para usuário atual
        success &= self.add_registry_key(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppHost",
            "SmartScreenEnabled",
            winreg.REG_SZ,
            "Off",
            "Desabilitar SmartScreen para usuário atual",
        )

        return success

    def desabilitar_assistencia_remota(self) -> bool:
        """Desabilitar controle total da Assistência Remota"""
        self.log("\n--- Desabilitando Assistência Remota ---")

        return self.add_registry_key(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Remote Assistance",
            "fAllowFullControl",
            winreg.REG_DWORD,
            0,
            "Desabilitar controle total da Assistência Remota",
        )

    def executar_remocao_completa(self) -> Tuple[bool, List[str], List[str]]:
        """Executa todas as operações de remoção de telemetria"""

        if not self.is_admin():
            self.log("⚠ AVISO: Execute como administrador para melhores resultados")

        self.log("=== INICIANDO REMOÇÃO DE TELEMETRIA E COLETA DE DADOS ===")

        # Lista de operações de remoção
        operacoes = [
            ("Metadados de Dispositivo", self.desabilitar_metadata_rede),
            ("Telemetria Principal", self.desabilitar_telemetria_principal),
            ("Malicious Removal Tool", self.desabilitar_malicious_removal_tool),
            ("CEIP (Customer Experience)", self.desabilitar_ceip),
            ("Application Compatibility", self.desabilitar_app_compat),
            ("AutoLoggers de Diagnóstico", self.desabilitar_auto_loggers),
            ("Windows SmartScreen", self.desabilitar_smartscreen),
            ("Assistência Remota", self.desabilitar_assistencia_remota),
        ]

        # Executar todas as operações
        overall_success = True
        for nome, funcao in operacoes:
            try:
                success = funcao()
                if not success:
                    overall_success = False
                    self.log(f"⚠ {nome}: Concluído com alguns erros")
            except Exception as e:
                overall_success = False
                error_msg = f"Erro crítico em {nome}: {str(e)}"
                self.log(f"✗ {error_msg}")
                self.errors.append(error_msg)

        self.log(f"\n=== RESULTADO DA REMOÇÃO DE TELEMETRIA ===")
        self.log(f"✓ Sucessos: {len(self.successes)}")
        self.log(f"✗ Erros: {len(self.errors)}")

        if overall_success and len(self.errors) == 0:
            self.log("🎉 TODA A TELEMETRIA FOI REMOVIDA COM SUCESSO!")
            self.log("🔒 Privacidade significativamente melhorada!")
        elif len(self.successes) > len(self.errors):
            self.log("⚠ REMOÇÃO DE TELEMETRIA CONCLUÍDA COM ALGUNS AVISOS")
            self.log("🔒 Maior parte da telemetria foi removida")
        else:
            self.log("⚠ REMOÇÃO DE TELEMETRIA CONCLUÍDA COM VÁRIOS ERROS")
            self.log("⚠ Algumas configurações podem não ter sido aplicadas")

        self.log("\n📋 O QUE FOI DESABILITADO:")
        self.log("• Coleta de telemetria do Windows")
        self.log("• Metadados de dispositivos da rede")
        self.log("• Customer Experience Improvement Program")
        self.log("• Application Compatibility tracking")
        self.log("• AutoLoggers de diagnóstico")
        self.log("• Windows SmartScreen")
        self.log("• Controle total da Assistência Remota")
        self.log("• Ofertas do Malicious Software Removal Tool")

        self.log("\n⚠ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!")
        self.log("🔒 PRIVACIDADE: Sua privacidade foi significativamente melhorada!")

        return overall_success, self.successes, self.errors


def main():
    """Função principal para teste independente"""
    remover = RemoverTelemetria()
    success, sucessos, erros = remover.executar_remocao_completa()

    if erros:
        print(f"\nErros encontrados:")
        for erro in erros:
            print(f"  - {erro}")

    return success


if __name__ == "__main__":
    main()
