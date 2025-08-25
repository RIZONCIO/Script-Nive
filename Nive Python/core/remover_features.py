import subprocess
import os
import sys


class RemoverFeatures:
    """Classe para remover recursos e features não utilizadas do Windows"""

    def __init__(self, logger=None):
        """Inicializar removedor de features"""
        self.logger = logger

        # Lista de features/recursos para desabilitar
        self.features_para_remover = [
            # Features básicas não utilizadas
            "SimpleTCP",
            "Windows-Identity-Foundation",
            "DirectoryServices-ADAM-Client",
            # IIS e componentes web (raramente utilizados em desktop)
            "IIS-WebServerRole",
            "IIS-WebServer",
            "IIS-CommonHttpFeatures",
            "IIS-HttpErrors",
            "IIS-HttpRedirect",
            "IIS-ApplicationDevelopment",
            "IIS-NetFxExtensibility",
            "IIS-NetFxExtensibility45",
            "IIS-HealthAndDiagnostics",
            "IIS-HttpLogging",
            "IIS-LoggingLibraries",
            "IIS-RequestMonitor",
            "IIS-HttpTracing",
            "IIS-Security",
            "IIS-URLAuthorization",
            "IIS-RequestFiltering",
            "IIS-IPSecurity",
            "IIS-Performance",
            "IIS-HttpCompressionDynamic",
            "IIS-WebServerManagementTools",
            "IIS-ManagementScriptingTools",
            "IIS-IIS6ManagementCompatibility",
            "IIS-Metabase",
            # Windows Activation Service
            "WAS-WindowsActivationService",
            "WAS-ProcessModel",
            "WAS-NetFxEnvironment",
            "WAS-ConfigurationAPI",
            # Mais componentes IIS
            "IIS-HostableWebCore",
            "IIS-CertProvider",
            "IIS-WindowsAuthentication",
            "IIS-DigestAuthentication",
            "IIS-ClientCertificateMappingAuthentication",
            "IIS-IISCertificateMappingAuthentication",
            "IIS-ODBCLogging",
            "IIS-StaticContent",
            "IIS-DefaultDocument",
            "IIS-DirectoryBrowsing",
            "IIS-WebDAV",
            "IIS-WebSockets",
            "IIS-ApplicationInit",
            "IIS-ASPNET",
            "IIS-ASPNET45",
            "IIS-ASP",
            "IIS-CGI",
            "IIS-ISAPIExtensions",
            "IIS-ISAPIFilter",
            "IIS-ServerSideIncludes",
            "IIS-CustomLogging",
            "IIS-BasicAuthentication",
            "IIS-HttpCompressionStatic",
            "IIS-ManagementConsole",
            "IIS-ManagementService",
            "IIS-WMICompatibility",
            "IIS-LegacyScripts",
            "IIS-LegacySnapIn",
            # FTP Server
            "IIS-FTPServer",
            "IIS-FTPSvc",
            "IIS-FTPExtensibility",
            # Message Queue (MSMQ)
            "MSMQ-Container",
            "MSMQ-Server",
            "MSMQ-Triggers",
            "MSMQ-ADIntegration",
            "MSMQ-HTTP",
            "MSMQ-Multicast",
            "MSMQ-DCOMProxy",
            # WCF Features
            "WCF-HTTP-Activation45",
            "WCF-TCP-Activation45",
            "WCF-Pipe-Activation45",
            "WCF-MSMQ-Activation45",
            "WCF-HTTP-Activation",
            "WCF-NonHTTP-Activation",
            "WCF-TCP-PortSharing45",
            # Outros recursos
            "NetFx4Extended-ASPNET45",
            "MediaPlayback",
            "Printing-XPSServices-Features",
            "MSRDC-Infrastructure",
            "TelnetClient",
            "TFTP",
            "TIFFIFilter",
            "WorkFolders-Client",
            "SMB1Protocol",  # Protocolo antigo e inseguro
            # Hyper-V (para usuários que não usam virtualização)
            "Microsoft-Hyper-V-All",
            "Microsoft-Hyper-V-Tools-All",
            "Microsoft-Hyper-V",
            "Microsoft-Hyper-V-Management-Clients",
            "Microsoft-Hyper-V-Management-PowerShell",
            # Outros
            "SearchEngine-Client-Package",
            "SmbDirect",
            "Printing-Foundation-Features",
            "Printing-Foundation-InternetPrinting-Client",
        ]

        # Capabilities para remover (apps/recursos opcionais)
        self.capabilities_para_remover = [
            "App.StepsRecorder~~~~0.0.1.0",  # Gravador de Passos
            "App.Support.QuickAssist~~~~0.0.1.0",  # Assistência Rápida
            "Browser.InternetExplorer~~~~0.0.11.0",  # Internet Explorer
            "Hello.Face.20134~~~~0.0.1.0",  # Windows Hello Face
            "MathRecognizer~~~~0.0.1.0",  # Reconhecedor de Matemática
            "Media.WindowsMediaPlayer~~~~0.0.12.0",  # Windows Media Player
            "Microsoft.Windows.WordPad~~~~0.0.1.0",  # WordPad
        ]

    def log(self, message):
        """Registrar mensagem no log"""
        if self.logger:
            self.logger.log(message)
        else:
            print(message)

    def verificar_permissoes_admin(self):
        """Verificar se está executando como administrador"""
        try:
            return os.getuid() == 0
        except AttributeError:
            # Windows
            try:
                return os.access(
                    os.path.join(
                        os.environ.get("SystemRoot", "C:\\Windows"), "system32"
                    ),
                    os.W_OK,
                )
            except:
                return False

    def executar_comando_dism(self, comando):
        """Executar comando DISM de forma segura"""
        try:
            # Executar comando DISM
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,  # Timeout de 60 segundos por comando
            )

            return resultado.returncode == 0, resultado.stdout, resultado.stderr

        except subprocess.TimeoutExpired:
            return False, "", "Timeout - comando demorou muito para executar"
        except Exception as e:
            return False, "", str(e)

    def desabilitar_feature(self, feature_name):
        """Desabilitar uma feature específica"""
        self.log(f"Desabilitando feature: {feature_name}")

        comando = f"DISM.exe /Online /norestart /Disable-Feature /featurename:{feature_name} /Remove"

        sucesso, stdout, stderr = self.executar_comando_dism(comando)

        if sucesso:
            self.log(f"✅ Feature {feature_name} desabilitada com sucesso")
            return True
        else:
            # Alguns erros são esperados (feature não instalada, etc)
            if "não foi encontrado" in stderr or "not found" in stderr.lower():
                self.log(f"⚠️ Feature {feature_name} não estava instalada")
                return True  # Não é um erro real
            elif (
                "não pode ser removido" in stderr
                or "cannot be removed" in stderr.lower()
            ):
                self.log(
                    f"⚠️ Feature {feature_name} não pode ser removida (protegida pelo sistema)"
                )
                return True  # Não é um erro crítico
            else:
                self.log(f"❌ Erro ao desabilitar {feature_name}: {stderr}")
                return False

    def remover_capability(self, capability_name):
        """Remover uma capability específica"""
        self.log(f"Removendo capability: {capability_name}")

        comando = f"DISM /Online /norestart /Remove-Capability /CapabilityName:{capability_name}"

        sucesso, stdout, stderr = self.executar_comando_dism(comando)

        if sucesso:
            self.log(f"✅ Capability {capability_name} removida com sucesso")
            return True
        else:
            # Alguns erros são esperados
            if "não foi encontrado" in stderr or "not found" in stderr.lower():
                self.log(f"⚠️ Capability {capability_name} não estava instalada")
                return True  # Não é um erro real
            else:
                self.log(f"❌ Erro ao remover {capability_name}: {stderr}")
                return False

    def executar_remocao_features(self):
        """Executar remoção de todas as features"""
        self.log("=== INICIANDO REMOÇÃO DE FEATURES DESNECESSÁRIAS ===")

        if not self.verificar_permissoes_admin():
            self.log("⚠️ AVISO: Execute como Administrador para melhores resultados!")

        sucessos = []
        erros = []

        # Desabilitar features
        self.log("\n--- Desabilitando Features do Windows ---")
        for feature in self.features_para_remover:
            try:
                if self.desabilitar_feature(feature):
                    sucessos.append(f"Feature desabilitada: {feature}")
                else:
                    erros.append(f"Falha ao desabilitar feature: {feature}")
            except Exception as e:
                erros.append(f"Erro crítico em {feature}: {str(e)}")

        # Remover capabilities
        self.log("\n--- Removendo Capabilities/Apps Opcionais ---")
        for capability in self.capabilities_para_remover:
            try:
                if self.remover_capability(capability):
                    sucessos.append(f"Capability removida: {capability}")
                else:
                    erros.append(f"Falha ao remover capability: {capability}")
            except Exception as e:
                erros.append(f"Erro crítico em {capability}: {str(e)}")

        # Relatório final
        self.log("\n=== RELATÓRIO FINAL ===")
        self.log(f"✅ Sucessos: {len(sucessos)}")
        self.log(f"❌ Erros: {len(erros)}")

        if len(erros) > 0:
            self.log("\n--- Detalhes dos Erros ---")
            for erro in erros[:10]:  # Mostrar apenas os primeiros 10 erros
                self.log(f"• {erro}")
            if len(erros) > 10:
                self.log(f"... e mais {len(erros) - 10} erros")

        # Consideramos sucesso se teve mais sucessos que erros
        sucesso_geral = len(sucessos) >= len(erros)

        if sucesso_geral:
            self.log("\n🎉 REMOÇÃO DE FEATURES CONCLUÍDA COM SUCESSO!")
            self.log("⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!")
        else:
            self.log("\n⚠️ REMOÇÃO CONCLUÍDA COM MUITOS ERROS")
            self.log("Verifique se está executando como Administrador")

        return sucesso_geral, sucessos, erros


# Função principal para teste
def main():
    """Função principal para testar o removedor"""
    print("=== TESTE DO REMOVEDOR DE FEATURES ===")

    class SimpleLogger:
        def log(self, message):
            print(message)

    removedor = RemoverFeatures(logger=SimpleLogger())
    sucesso, sucessos, erros = removedor.executar_remocao_features()

    print(f"\nResultado: {'Sucesso' if sucesso else 'Falhou'}")
    print(f"Sucessos: {len(sucessos)}, Erros: {len(erros)}")


if __name__ == "__main__":
    main()
