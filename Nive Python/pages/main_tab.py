import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import psutil
import threading
import time
from utils import icons as ic

COLORS = {
    "content_bg": "#1e1e2e",
    "card_bg": "#252537",
    "card_hover": "#2e2e45",
    "accent": "#4f9cf9",
    "text_primary": "#e2e8f0",
    "text_muted": "#8892a4",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#3b82f6",
    "purple": "#a855f7",
    "teal": "#14b8a6",
    "orange": "#f97316",
}


def alpha_blend(hex_color: str, bg: str = "#252537", alpha: float = 0.15) -> str:
    def parse(h):
        h = h.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    r1, g1, b1 = parse(hex_color)
    r2, g2, b2 = parse(bg)
    return "#{:02x}{:02x}{:02x}".format(
        int(r1 * alpha + r2 * (1 - alpha)),
        int(g1 * alpha + g2 * (1 - alpha)),
        int(b1 * alpha + b2 * (1 - alpha)),
    )


class Tooltip:
    def __init__(self, widget, text, delay=400):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self._after_id = None
        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._hide)
        widget.bind("<Motion>", self._move)

    def _schedule(self, event=None):
        self._unschedule()
        self._after_id = self.widget.after(self.delay, self._show)

    def _unschedule(self):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def _show(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_pointerx() + 12
        y = self.widget.winfo_pointery() + 12
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#20232a",
            foreground="#f8fafc",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 10),
            padx=8,
            pady=4,
            wraplength=260,
        )
        label.pack()
        tw.wm_geometry(f"+{x}+{y}")

    def _move(self, event):
        if self.tip_window:
            x = event.x_root + 12
            y = event.y_root + 12
            self.tip_window.wm_geometry(f"+{x}+{y}")

    def _hide(self, event=None):
        self._unschedule()
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


def make_action_card(
    parent, icon_key, title, subtitle, command, accent_color, row, col
):
    card = ctk.CTkFrame(
        parent,
        fg_color=COLORS["card_bg"],
        corner_radius=12,
        border_width=1,
        border_color="#2d2d44",
    )
    card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

    icon_frame = ctk.CTkFrame(
        card,
        fg_color=alpha_blend(accent_color, COLORS["card_bg"], 0.15),
        width=48,
        height=48,
        corner_radius=10,
    )
    icon_frame.pack_propagate(False)
    icon_frame.pack(side="left", padx=(14, 10), pady=14)

    ctk.CTkLabel(
        icon_frame,
        text=ic.get(icon_key),
        font=ctk.CTkFont(
            family=ic.family(icon_key), size=20, weight=ic.weight(icon_key)
        ),
        text_color=accent_color,
    ).pack(expand=True)

    text_frame = ctk.CTkFrame(card, fg_color="transparent")
    text_frame.pack(side="left", fill="both", expand=True, pady=12, padx=(0, 14))

    ctk.CTkLabel(
        text_frame,
        text=title,
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        text_color=COLORS["text_primary"],
        anchor="w",
    ).pack(fill="x")

    ctk.CTkLabel(
        text_frame,
        text=subtitle,
        font=ctk.CTkFont(size=11),
        text_color=COLORS["text_muted"],
        anchor="w",
        wraplength=190,
    ).pack(fill="x", pady=(2, 0))

    border_hover = alpha_blend(accent_color, COLORS["card_hover"], 0.38)

    def on_enter(e):
        card.configure(fg_color=COLORS["card_hover"], border_color=border_hover)

    def on_leave(e):
        card.configure(fg_color=COLORS["card_bg"], border_color="#2d2d44")

    def on_click(e):
        command()

    for w in (card, icon_frame, text_frame):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
        w.bind("<Button-1>", on_click)

    Tooltip(card, subtitle)
    return card


class MainTab:
    def __init__(self, parent_interface):
        self.parent = parent_interface
        self.system_commands = parent_interface.system_commands
        self.config = parent_interface.config
        self.logger = parent_interface.logger
        self.monitor_running = False

    def create_main_tab(self, notebook):
        page = ctk.CTkScrollableFrame(
            notebook,
            fg_color=COLORS["content_bg"],
            scrollbar_fg_color=COLORS["content_bg"],
            scrollbar_button_color="#2d2d44",
            corner_radius=0,
        )

        # Dashboard de Monitoramento
        self._create_system_monitor(page)

        self._section(page, "Tarefas Comuns")
        grid1 = ctk.CTkFrame(page, fg_color="transparent")
        grid1.pack(fill="x", padx=16, pady=(4, 8))
        grid1.columnconfigure((0, 1, 2), weight=1)

        COMMON = [
            (
                "trash",
                "Esvaziar Lixeira",
                "Remove arquivos deletados",
                self.system_commands.empty_recycle_bin,
                COLORS["success"],
            ),
            (
                "bolt",
                "Ativar GodMode",
                "Acesso a todas as configurações",
                self.system_commands.activate_godmode,
                COLORS["accent"],
            ),
            (
                "hdd",
                "Verificar HD/SSD",
                "Chkdsk para erros no disco",
                self.system_commands.check_disk_errors,
                COLORS["warning"],
            ),
            (
                "microchip",
                "Verificar RAM",
                "Diagnóstico de memória",
                self.system_commands.check_ram,
                COLORS["info"],
            ),
            (
                "wrench",
                "Reparar Sistema",
                "SFC + DISM automático",
                self.system_commands.repair_system,
                COLORS["danger"],
            ),
            (
                "broom",
                "Limpar Temporários",
                "Apaga arquivos temp do sistema",
                self.system_commands.clean_temp_files,
                COLORS["teal"],
            ),
        ]
        for i, (k, t, s, c, col) in enumerate(COMMON):
            make_action_card(grid1, k, t, s, c, col, i // 3, i % 3)

        self._section(page, "Ferramentas do Sistema")
        grid2 = ctk.CTkFrame(page, fg_color="transparent")
        grid2.pack(fill="x", padx=16, pady=(4, 24))
        grid2.columnconfigure((0, 1, 2), weight=1)

        SYSTEM = [
            (
                "task_manager",
                "Gerenciador de Tarefas",
                "Processos e desempenho",
                self.open_task_manager,
                COLORS["info"],
            ),
            (
                "shield",
                "Iniciar MRT",
                "Remove malware da Microsoft",
                self.start_mrt,
                COLORS["purple"],
            ),
            (
                "box",
                "Atualizar Programas",
                "Winget / Windows Update",
                self.system_commands.update_programs,
                COLORS["success"],
            ),
            (
                "sliders",
                "Reparar Som",
                "Reinicia serviço de áudio",
                self.system_commands.fix_audio,
                COLORS["orange"],
            ),
            (
                "box",
                "Reinstalar Software",
                "Instala pacotes essenciais",
                self.parent.reinstall_software_placeholder,
                COLORS["danger"],
            ),
            (
                "folder",
                "Deletar Pasta Corrompida",
                "Remove diretórios problemáticos",
                self.delete_corrupted_folders,
                COLORS["warning"],
            ),
            (
                "medkit",
                "Reparo Completo Windows",
                "Pipeline completo de reparo",
                self.parent.complete_repair_placeholder,
                COLORS["danger"],
            ),
            (
                "sliders",
                "Painel de Controle",
                "Configurações clássicas do Windows",
                self.open_control_panel,
                COLORS["text_muted"],
            ),
        ]
        for i, (k, t, s, c, col) in enumerate(SYSTEM):
            make_action_card(grid2, k, t, s, c, col, i // 3, i % 3)

        return page

    def _create_system_monitor(self, parent):
        """Cria o dashboard de monitoramento do sistema"""
        self._section(parent, "Monitoramento do Sistema")

        monitor_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["card_bg"],
            corner_radius=12,
            border_width=1,
            border_color="#2d2d44",
        )
        monitor_frame.pack(fill="x", padx=16, pady=(4, 16))

        # Labels para métricas
        self.cpu_label = ctk.CTkLabel(
            monitor_frame,
            text="CPU: Calculando...",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_primary"],
        )
        self.cpu_label.pack(pady=(12, 4))

        self.ram_label = ctk.CTkLabel(
            monitor_frame,
            text="RAM: Calculando...",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_primary"],
        )
        self.ram_label.pack(pady=4)

        self.disk_label = ctk.CTkLabel(
            monitor_frame,
            text="Disco: Calculando...",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_primary"],
        )
        self.disk_label.pack(pady=4)

        self.gpu_label = ctk.CTkLabel(
            monitor_frame,
            text="GPU: Calculando...",
            font=ctk.CTkFont(size=12),
            text_color=COLORS["text_primary"],
        )
        self.gpu_label.pack(pady=(4, 12))

        # Iniciar atualização em thread separada
        self.monitor_running = True
        threading.Thread(target=self._update_monitor, daemon=True).start()

    def _update_monitor(self):
        """Atualiza as métricas do sistema periodicamente"""
        while self.monitor_running:
            try:
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_color = self._get_usage_color(cpu_percent)
                self.cpu_label.configure(
                    text=f"CPU: {cpu_percent:.1f}%", text_color=cpu_color
                )

                # RAM
                ram = psutil.virtual_memory()
                ram_percent = ram.percent
                ram_color = self._get_usage_color(ram_percent)
                self.ram_label.configure(
                    text=f"RAM: {ram_percent:.1f}% ({ram.used // (1024**3)}GB / {ram.total // (1024**3)}GB)",
                    text_color=ram_color,
                )

                # Disco
                disk = psutil.disk_usage("/")
                disk_percent = disk.percent
                disk_color = self._get_usage_color(disk_percent)
                self.disk_label.configure(
                    text=f"Disco: {disk_percent:.1f}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)",
                    text_color=disk_color,
                )

                # GPU
                gpu_info = self._get_gpu_info()
                self.gpu_label.configure(text=f"GPU: {gpu_info}")

            except Exception as e:
                self.cpu_label.configure(
                    text=f"CPU: Erro - {e}", text_color=COLORS["danger"]
                )
                self.ram_label.configure(
                    text=f"RAM: Erro - {e}", text_color=COLORS["danger"]
                )
                self.disk_label.configure(
                    text=f"Disco: Erro - {e}", text_color=COLORS["danger"]
                )
                self.gpu_label.configure(
                    text=f"GPU: Erro - {e}", text_color=COLORS["danger"]
                )

            time.sleep(2)  # Atualizar a cada 2 segundos

    def _get_usage_color(self, percent):
        """Retorna cor baseada no uso"""
        if percent < 50:
            return COLORS["success"]
        elif percent < 80:
            return COLORS["warning"]
        else:
            return COLORS["danger"]

    def _get_gpu_info(self):
        try:
            GPUtil = __import__("GPUtil")
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                load = gpu.load * 100
                return f"{load:.0f}%"
        except Exception:
            pass

        return "N/D"

    def _section(self, parent, text):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=16, pady=(18, 4))
        ctk.CTkLabel(
            f,
            text=text,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(side="left")
        ctk.CTkFrame(
            f,
            height=2,
            fg_color=alpha_blend(COLORS["accent"], COLORS["content_bg"], 0.25),
            corner_radius=1,
        ).pack(side="left", fill="x", expand=True, padx=(10, 0), pady=10)

    def open_control_panel(self):
        subprocess.Popen("control.exe")
        self.logger.log_info("Painel de Controle aberto")
        self.parent.update_status("Painel de Controle aberto")

    def open_task_manager(self):
        subprocess.Popen("taskmgr.exe")
        self.logger.log_info("Gerenciador de Tarefas aberto")
        self.parent.update_status("Gerenciador de Tarefas aberto")

    def start_mrt(self):
        try:
            subprocess.run(self.config.get_command("mrt"), shell=True, check=True)
            self.logger.log_success("MRT iniciado com sucesso")
            self.parent.update_status("MRT iniciado")
        except Exception as e:
            self.logger.log_error(f"Erro ao iniciar MRT: {e}")
            messagebox.showerror("Erro", f"Erro ao iniciar MRT:\n{e}")

    def delete_corrupted_folders(self):
        path = filedialog.askdirectory(title="Selecione a pasta corrompida")
        if path and messagebox.askyesno(
            "Confirmar",
            f"Deletar permanentemente:\n{path}\n\nEsta ação não pode ser desfeita!",
        ):
            if self.system_commands.delete_corrupted_folder(path):
                self.logger.log_success(f"Pasta deletada: {path}")
                messagebox.showinfo("Sucesso", "Pasta deletada com sucesso!")
            else:
                self.logger.log_warning(f"Falha ao deletar pasta: {path}")
                messagebox.showwarning(
                    "Aviso", "A pasta pode ainda existir.\nTente em modo seguro."
                )
