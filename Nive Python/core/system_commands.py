"""
Comandos do Sistema ScriptNive
core/system_commands.py
"""

import subprocess
import os
import threading
from pathlib import Path
from tkinter import messagebox


class SystemCommands:
    """Classe para executar comandos do sistema"""

    def __init__(self, logger):
        """Inicializar comandos do sistema"""
        self.logger = logger
        self.is_running = False

    def run_command_sync(self, command, shell=True):
        """Executar comando sincronamente"""
        try:
            self.logger.log(f"Executando comando: {command}")
            result = subprocess.run(
                command, shell=shell, capture_output=True, text=True, timeout=300
            )

            if result.returncode == 0:
                self.logger.log_success(f"Comando executado com sucesso")
                return True, result.stdout
            else:
                self.logger.log_error(f"Erro no comando. Código: {result.returncode}")
                self.logger.log_error(f"Stderr: {result.stderr}")
                return False, result.stderr

        except subprocess.TimeoutExpired:
            self.logger.log_error("Comando excedeu tempo limite (5 minutos)")
            return False, "Timeout"
        except Exception as e:
            self.logger.log_error(f"Erro ao executar comando: {str(e)}")
            return False, str(e)

    def run_command_async(self, command, success_callback=None, error_callback=None):
        """Executar comando assincronamente"""

        def run():
            try:
                self.is_running = True
                success, output = self.run_command_sync(command)
                self.is_running = False

                if success:
                    if success_callback:
                        success_callback(output)
                else:
                    if error_callback:
                        error_callback(output)

            except Exception as e:
                self.is_running = False
                self.logger.log_error(f"Erro em thread assíncrona: {str(e)}")
                if error_callback:
                    error_callback(str(e))

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return thread

    def empty_recycle_bin(self):
        """Esvaziar lixeira"""
        command = (
            'powershell -NoProfile -Command "'
            "try { Clear-RecycleBin -Force -ErrorAction Stop } "
            "catch { Write-Error $_.Exception.Message; exit 1 }"
            '"'
        )

        def success_callback(output):
            self.logger.log_success("Lixeira esvaziada com sucesso")
            messagebox.showinfo("Sucesso", "Lixeira esvaziada com sucesso!")

        def error_callback(error):
            self.logger.log_error("Erro ao esvaziar lixeira")
            self.logger.log(f"Detalhe do erro na lixeira: {error}")
            message = (
                "Não foi possível esvaziar totalmente a lixeira. "
                "Alguns itens podem estar em uso ou exigir privilégios elevados."
            )
            messagebox.showwarning("Atenção", message)

        return self.run_command_async(command, success_callback, error_callback)

    def activate_godmode(self):
        """Ativar GodMode"""
        try:
            desktop_path = Path.home() / "Desktop"
            godmode_path = (
                desktop_path / "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}"
            )

            godmode_path.mkdir(exist_ok=True)

            self.logger.log_success("GodMode criado na Área de Trabalho")
            messagebox.showinfo("Sucesso", "GodMode foi criado na Área de Trabalho!")

        except Exception as e:
            self.logger.log_error(f"Erro ao criar GodMode: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao criar GodMode:\n{str(e)}")

    def check_disk_errors(self):
        """Verificar erros no HD/SSD - COMANDO COMPLETO IGUAL AO .BAT"""
        if not messagebox.askyesno(
            "Confirmar",
            "Esta operação requer reinicialização do sistema.\nDeseja continuar?",
        ):
            return

        # Comandos exatamente como no ScriptNive.bat
        commands = [
            "WMIC diskdrive get status",
            "WMIC diskdrive get model,status",
            "CHKDSK /R",
            "shutdown -r -t 30",
        ]

        full_command = " & ".join(commands)

        def success_callback(output):
            self.logger.log_success(
                "Verificação de disco agendada - Sistema será reiniciado"
            )
            messagebox.showinfo(
                "Sucesso",
                "Verificação de disco agendada.\nO sistema será reiniciado em 30 segundos.",
            )

        def error_callback(error):
            self.logger.log_error("Erro ao agendar verificação de disco")
            messagebox.showerror("Erro", f"Erro ao agendar verificação:\n{error}")

        return self.run_command_async(full_command, success_callback, error_callback)

    def check_ram(self):
        """Verificar RAM"""
        command = "mdsched"

        def success_callback(output):
            self.logger.log_success("Diagnóstico de memória iniciado")
            messagebox.showinfo("Sucesso", "Diagnóstico de memória iniciado!")

        def error_callback(error):
            self.logger.log_error("Erro ao iniciar diagnóstico de memória")
            messagebox.showerror("Erro", f"Erro ao iniciar diagnóstico:\n{error}")

        return self.run_command_async(command, success_callback, error_callback)

    def repair_system(self):
        """Reparar sistema"""
        if not messagebox.askyesno(
            "Confirmar",
            "Esta operação pode demorar muito tempo e requer reinicialização.\nDeseja continuar?",
        ):
            return

        commands = [
            "sfc /scannow",
            "Dism /Online /Cleanup-Image /ScanHealth",
            "Dism /Online /Cleanup-Image /RestoreHealth",
            "shutdown -r -t 30",
        ]

        full_command = " && ".join(commands)

        def success_callback(output):
            self.logger.log_success("Reparo do sistema concluído")
            messagebox.showinfo(
                "Sucesso", "Reparo do sistema concluído!\nSistema será reiniciado."
            )

        def error_callback(error):
            self.logger.log_error("Erro durante reparo do sistema")
            messagebox.showerror("Erro", f"Erro durante reparo:\n{error}")

        return self.run_command_async(full_command, success_callback, error_callback)

    def clean_temp_files(self):
        """Limpar arquivos temporários"""
        commands = [
            'del /q /f /s "%temp%\\*"',
            'del /q/f/s "C:\\Windows\\Temp\\*"',
            'del /q /f /s "%windir%\\Prefetch\\*"',
            'del /q /f /s "%appdata%\\Microsoft\\Windows\\Recent\\*"',
        ]

        # Executar comandos de limpeza
        for cmd in commands:
            success, output = self.run_command_sync(cmd)

        # Abrir limpeza de disco
        try:
            subprocess.Popen("cleanmgr.exe", shell=True)
        except:
            pass

        self.logger.log_success("Arquivos temporários limpos")
        messagebox.showinfo("Sucesso", "Arquivos temporários limpos com sucesso!")

    def clean_dns_cache(self):
        """Limpar cache DNS - Versão corrigida"""

        # Primeiro, verificar se é necessário executar como administrador
        import ctypes
        import sys

        def is_admin():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        if not is_admin():
            self.logger.log_error("Operação requer privilégios de administrador")
            messagebox.showerror(
                "Erro - Privilégios",
                "Esta operação requer privilégios de administrador.\n"
                "Execute o programa como Administrador e tente novamente.",
            )
            return

        # Comandos de limpeza DNS separados para melhor controle
        dns_commands = [
            (
                "Resetando Winsock (repara catálogo de sockets)...",
                "netsh winsock reset",
            ),
            (
                "Resetando pilha TCP/IP (repara configurações IP)...",
                "netsh int ip reset",
            ),
            (
                "Limpando cache NetBIOS (purga nomes locais)...",
                "nbtstat -R",
            ),  # Extra: útil para problemas de nomes de rede
            (
                "Liberando nomes NetBIOS (atualiza registro)...",
                "nbtstat -RR",
            ),  # Extra: complementa o anterior
            (
                "Limpando cache ARP (remove mapeamentos de IP para MAC)...",
                "arp -d *",
            ),  # Extra: bom para conflitos de hardware na rede
            (
                "Parando serviço DNS Client...",
                "net stop dnscache",
            ),  # Da sua lista, opcional mas ajuda em flushes mais profundos
            ("Limpando cache DNS...", "ipconfig /flushdns"),
            ("Reiniciando serviço DNS Client...", "net start dnscache"),  # Da sua lista
            ("Liberando IP atual...", "ipconfig /release"),
            ("Renovando IP...", "ipconfig /renew"),
            ("Registrando DNS...", "ipconfig /registerdns"),
        ]

        def execute_dns_cleanup():
            success_count = 0
            total_commands = len(dns_commands)

            try:
                for description, command in dns_commands:
                    self.logger.log(f"{description}")

                    # Executar comando individual
                    result = subprocess.run(
                        command, shell=True, capture_output=True, text=True, timeout=60
                    )

                    if result.returncode == 0:
                        success_count += 1
                        self.logger.log_success(f"✓ {description} - Sucesso")
                    else:
                        self.logger.log_warning(
                            f"⚠ {description} - Código: {result.returncode}"
                        )
                        # Continuar mesmo se um comando falhar

                # Comandos adicionais de reset de rede (opcionais)
                additional_commands = ["netsh winsock reset", "netsh int ip reset"]

                for cmd in additional_commands:
                    try:
                        result = subprocess.run(
                            cmd, shell=True, capture_output=True, text=True, timeout=30
                        )
                        if result.returncode == 0:
                            success_count += 1
                            self.logger.log_success(f"✓ {cmd} - Sucesso")
                    except:
                        self.logger.log_warning(f"⚠ Comando opcional falhou: {cmd}")

                return (
                    success_count > 0,
                    f"Executados {success_count} comandos com sucesso",
                )

            except subprocess.TimeoutExpired:
                return False, "Timeout - Operação demorou muito para completar"
            except Exception as e:
                return False, f"Erro inesperado: {str(e)}"

        def success_callback(output):
            self.logger.log_success("Cache DNS limpo com sucesso!")
            messagebox.showinfo(
                "Sucesso",
                "Cache DNS limpo com sucesso!\n\n"
                "Recomenda-se reiniciar o navegador para aplicar as mudanças.\n\n"
                "Detalhes no log.",
            )

        def error_callback(error):
            self.logger.log_error(f"Erro ao limpar cache DNS: {error}")
            messagebox.showerror(
                "Erro",
                f"Erro ao limpar cache DNS:\n\n{error}\n\n"
                "Possíveis soluções:\n"
                "• Execute como Administrador\n"
                "• Verifique sua conexão de rede\n"
                "• Tente novamente em alguns minutos",
            )

        # Executar de forma assíncrona
        def run():
            try:
                self.is_running = True
                self.logger.log("Iniciando limpeza de cache DNS...")

                success, output = execute_dns_cleanup()
                self.is_running = False

                if success:
                    success_callback(output)
                else:
                    error_callback(output)

            except Exception as e:
                self.is_running = False
                error_callback(str(e))

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        return thread

    def fix_audio(self):
        """Reparar som - Exatamente como no .bat"""
        commands = [
            "net stop audiosrv",
            "timeout /t 5",
            "net start audiosrv",
            "net start AudioEndpointBuilder",
            "net start wuauserv",
        ]

        full_command = " & ".join(commands)

        def success_callback(output):
            self.logger.log_success("Serviços de áudio reiniciados")
            messagebox.showinfo(
                "Sucesso",
                "Serviços de áudio reiniciados!\nVerifique se os problemas foram resolvidos.",
            )

        def error_callback(error):
            self.logger.log_error("Erro ao reparar áudio")
            messagebox.showerror("Erro", f"Erro ao reparar áudio:\n{error}")

        return self.run_command_async(full_command, success_callback, error_callback)

    def update_programs(self):
        """Atualizar programas com winget"""
        command = "winget upgrade --all"

        def success_callback(output):
            self.logger.log_success("Programas atualizados")
            messagebox.showinfo("Sucesso", "Atualização de programas concluída!")

        def error_callback(error):
            self.logger.log_error("Erro ao atualizar programas")
            messagebox.showerror("Erro", f"Erro ao atualizar programas:\n{error}")

        return self.run_command_async(command, success_callback, error_callback)

    def delete_corrupted_folder(self, folder_path):
        """Deletar pasta corrompida - Exatamente como no .bat"""
        if not folder_path or not os.path.exists(folder_path):
            self.logger.log_error("Caminho da pasta inválido")
            return False

        commands = [
            f'attrib -R -S -H "{folder_path}" /S /D',
            f'takeown /f "{folder_path}" /r /d y',
            f'icacls "{folder_path}" /grant administrators:F /t',
            f'rd /s /q "{folder_path}"',
        ]

        self.logger.log(f"Tentando deletar pasta: {folder_path}")

        for cmd in commands:
            success, output = self.run_command_sync(cmd)

        # Verificar se pasta ainda existe
        if not os.path.exists(folder_path):
            self.logger.log_success(f"Pasta deletada com sucesso: {folder_path}")
            return True
        else:
            # Tentar método "zumbi" como no .bat original
            self.logger.log_warning(
                "Pasta ainda existe, tentando método alternativo..."
            )

            try:
                import tempfile

                temp_dir = tempfile.mkdtemp()

                # Usar robocopy para sobrescrever com pasta vazia
                robocopy_cmd = f'robocopy "{temp_dir}" "{folder_path}" /MIR'
                success, output = self.run_command_sync(robocopy_cmd)

                # Tentar deletar novamente
                success, output = self.run_command_sync(f'rd /s /q "{folder_path}"')

                # Limpar pasta temporária
                os.rmdir(temp_dir)

                if not os.path.exists(folder_path):
                    self.logger.log_success(
                        "Pasta corrompida deletada com método alternativo"
                    )
                    return True
                else:
                    self.logger.log_error(
                        "Não foi possível deletar a pasta mesmo com método alternativo"
                    )
                    return False

            except Exception as e:
                self.logger.log_error(f"Erro no método alternativo: {str(e)}")
                return False

    def open_system_tools(self):
        """Métodos para abrir ferramentas do sistema"""

        def open_control_panel(self):
            subprocess.Popen("control.exe")
            self.logger.log("Painel de Controle aberto")

        def open_task_manager(self):
            subprocess.Popen("taskmgr.exe")
            self.logger.log("Gerenciador de Tarefas aberto")

        def start_mrt(self):
            command = "powershell.exe -command \"Start-Process 'C:\\Windows\\System32\\MRT.exe'\""

            def success_callback(output):
                self.logger.log_success(
                    "MRT (Malicious Software Removal Tool) iniciado"
                )

            def error_callback(error):
                self.logger.log_error("Erro ao iniciar MRT")
                messagebox.showerror("Erro", f"Erro ao iniciar MRT:\n{error}")

            return self.run_command_async(command, success_callback, error_callback)

        def check_diagnostics(self):
            subprocess.Popen("perfmon /rel")
            self.logger.log("Monitor de Confiabilidade (perfmon) aberto")

        return {
            "control_panel": open_control_panel,
            "task_manager": open_task_manager,
            "mrt": start_mrt,
            "diagnostics": check_diagnostics,
        }

    # Adicione no final da classe SystemCommands no seu system_commands.py:

    def complete_windows_repair(self, progress_callback=None):
        """Executar reparo completo do Windows (baseado no script do Ivo Dias)"""
        from core.complete_repair import get_complete_repair

        # Confirmação antes de executar
        from tkinter import messagebox

        if not messagebox.askyesno(
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
        ):
            return

        # Obter instância do reparo completo
        repair_tool = get_complete_repair(self.logger)

        def success_callback(message):
            self.logger.log_success("Reparo completo finalizado com sucesso!")
            messagebox.showinfo(
                "Reparo Concluído",
                "Reparo completo do Windows finalizado!\n\n"
                "RECOMENDA-SE REINICIAR O COMPUTADOR AGORA.\n\n"
                "Deseja reiniciar agora?",
            )

            if messagebox.askyesno("Reiniciar", "Reiniciar o computador agora?"):
                subprocess.run("shutdown -r -t 10", shell=True)

        def error_callback(error):
            self.logger.log_error(f"Erro durante reparo completo: {error}")
            messagebox.showerror(
                "Erro no Reparo",
                f"Ocorreu um erro durante o reparo completo:\n\n{error}\n\n"
                "Verifique o log para mais detalhes.",
            )

        return repair_tool.run_complete_repair_async(
            success_callback=success_callback,
            error_callback=error_callback,
            progress_callback=progress_callback,
        )

    def is_command_running(self):
        """Verificar se algum comando está em execução"""
        return self.is_running
