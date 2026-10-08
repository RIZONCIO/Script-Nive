"""
network_tab.py - Aba de rede modernizada com ícones Font Awesome
"""

import subprocess
import threading
import customtkinter as ctk
from tkinter import messagebox
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


class NetworkTab:
    def __init__(self, parent_interface):
        self.parent = parent_interface
        self.system_commands = parent_interface.system_commands
        self.config = parent_interface.config
        self.logger = parent_interface.logger
        self.logger = parent_interface.logger

    def create_network_tab(self, notebook):
        page = ctk.CTkScrollableFrame(
            notebook,
            fg_color=COLORS["content_bg"],
            scrollbar_fg_color=COLORS["content_bg"],
            scrollbar_button_color="#2d2d44",
            corner_radius=0,
        )

        self._section(page, "Reparo e Reset")
        g1 = self._grid(page)
        REPAIR = [
            (
                "broom",
                "Limpar Cache DNS",
                "Renova configurações DNS",
                self.system_commands.clean_dns_cache,
                COLORS["info"],
            ),
            (
                "rotate",
                "Renovar IP",
                "Release + renew DHCP",
                self.renew_ip_address,
                COLORS["teal"],
            ),
            (
                "bomb",
                "Reset Completo de Rede",
                "Winsock + TCP/IP + DNS",
                self.complete_network_reset,
                COLORS["warning"],
            ),
            (
                "globe",
                "Testar Conectividade",
                "Ping Google/Cloudflare/OpenDNS",
                self.test_connectivity,
                COLORS["success"],
            ),
            (
                "shield",
                "Reset Winsock",
                "Catálogo Winsock padrão",
                self.reset_winsock,
                COLORS["purple"],
            ),
            (
                "plug",
                "Reiniciar Adaptador",
                "Desativa e reativa a placa",
                self.restart_network_adapter,
                COLORS["danger"],
            ),
        ]
        for i, (k, t, s, c, col) in enumerate(REPAIR):
            self._card(g1, k, t, s, c, col, i // 3, i % 3)

        self._section(page, "Informações de Rede")
        g2 = self._grid(page)
        INFO = [
            (
                "wifi",
                "Configuração IP",
                "ipconfig /all",
                self.show_ip_config,
                COLORS["info"],
            ),
            (
                "map",
                "Tabela de Roteamento",
                "route print",
                self.show_route_table,
                COLORS["teal"],
            ),
            (
                "chart_line",
                "Estatísticas de Rede",
                "netstat -e",
                self.show_network_stats,
                COLORS["success"],
            ),
            (
                "tools",
                "Configurações de Rede",
                "ncpa.cpl — placas de rede",
                self.open_network_settings,
                COLORS["accent"],
            ),
            (
                "map",
                "Diagnóstico Automático",
                "msdt NetworkDiagnosticsWeb",
                self.network_diagnostics,
                COLORS["purple"],
            ),
        ]
        for i, (k, t, s, c, col) in enumerate(INFO):
            self._card(g2, k, t, s, c, col, i // 3, i % 3)

        return page

    def _section(self, parent, text):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", padx=16, pady=(18, 4))
        ctk.CTkLabel(
            f,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["text_primary"],
        ).pack(side="left")
        ctk.CTkFrame(
            f,
            height=2,
            fg_color=alpha_blend(COLORS["accent"], COLORS["content_bg"], 0.25),
            corner_radius=1,
        ).pack(side="left", fill="x", expand=True, padx=(10, 0), pady=10)

    def _grid(self, parent):
        g = ctk.CTkFrame(parent, fg_color="transparent")
        g.pack(fill="x", padx=16, pady=(4, 8))
        g.columnconfigure((0, 1, 2), weight=1)
        return g

    def _card(self, parent, icon_key, title, sub, cmd, color, row, col):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["card_bg"],
            corner_radius=12,
            border_width=1,
            border_color="#2d2d44",
        )
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        ico_f = ctk.CTkFrame(
            card,
            fg_color=alpha_blend(color, COLORS["card_bg"], 0.15),
            width=48,
            height=48,
            corner_radius=10,
        )
        ico_f.pack_propagate(False)
        ico_f.pack(side="left", padx=(14, 10), pady=14)

        ctk.CTkLabel(
            ico_f,
            text=ic.get(icon_key),
            font=ctk.CTkFont(
                family=ic.family(icon_key), size=20, weight=ic.weight(icon_key)
            ),
            text_color=color,
        ).pack(expand=True)

        txt_f = ctk.CTkFrame(card, fg_color="transparent")
        txt_f.pack(side="left", fill="both", expand=True, pady=12, padx=(0, 14))
        ctk.CTkLabel(
            txt_f,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS["text_primary"],
            anchor="w",
        ).pack(fill="x")
        ctk.CTkLabel(
            txt_f,
            text=sub,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"],
            anchor="w",
            wraplength=190,
        ).pack(fill="x")

        border_hover = alpha_blend(color, COLORS["card_hover"], 0.38)

        def on_enter(e):
            card.configure(fg_color=COLORS["card_hover"], border_color=border_hover)

        def on_leave(e):
            card.configure(fg_color=COLORS["card_bg"], border_color="#2d2d44")

        def on_click(e):
            cmd()

        for w in (card, ico_f, txt_f):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)

    # ── Lógica de rede ────────────────────────────────────────────────────────

    def renew_ip_address(self):
        def _run():
            try:
                subprocess.run(
                    "ipconfig /release && ipconfig /renew", shell=True, check=True
                )
                self.logger.log_success("IP renovado com sucesso")
                self.parent.root.after(
                    0, lambda: messagebox.showinfo("Sucesso", "IP renovado!")
                )
            except Exception as e:
                self.logger.log_error(f"Erro ao renovar IP: {e}")
                self.parent.root.after(0, lambda: messagebox.showerror("Erro", str(e)))

        threading.Thread(target=_run, daemon=True).start()

    def complete_network_reset(self):
        if not messagebox.askyesno(
            "Confirmar Reset",
            "Reset completo de rede.\nSistema reiniciará em 60s.\n\nContinuar?",
        ):
            return
        cmds = [
            "netsh winsock reset",
            "netsh int ip reset",
            "ipconfig /flushdns",
            "ipconfig /release",
            "ipconfig /renew",
            "shutdown -r -t 60",
        ]
        subprocess.Popen(" && ".join(cmds), shell=True)
        self.logger.log_success("Reset completo de rede agendado - reinício em 60s")
        messagebox.showinfo("Reset Agendado", "Sistema será reiniciado em 60 segundos.")

    def test_connectivity(self):
        def _run():
            hosts = [
                ("8.8.8.8", "Google DNS"),
                ("1.1.1.1", "Cloudflare"),
                ("208.67.222.222", "OpenDNS"),
            ]
            results = []
            for ip, name in hosts:
                ok = (
                    "TTL="
                    in subprocess.run(
                        f"ping -n 2 {ip}", shell=True, capture_output=True, text=True
                    ).stdout
                )
                results.append(f"{'✅' if ok else '❌'} {name} ({ip})")
            self.logger.log_info("Teste de conectividade realizado")
            self.parent.root.after(
                0, lambda: messagebox.showinfo("Conectividade", "\n".join(results))
            )

        threading.Thread(target=_run, daemon=True).start()

    def reset_winsock(self):
        subprocess.Popen("netsh winsock reset", shell=True)
        self.logger.log_success("Winsock resetado - reinício necessário")
        messagebox.showinfo("Winsock", "Winsock resetado. Reinicie o PC.")

    def open_network_settings(self):
        subprocess.Popen("ncpa.cpl", shell=True)
        self.logger.log_info("Configurações de rede abertas")

    def network_diagnostics(self):
        subprocess.Popen("msdt.exe -id NetworkDiagnosticsWeb", shell=True)
        self.logger.log_info("Diagnóstico de rede iniciado")

    def restart_network_adapter(self):
        if messagebox.askyesno(
            "Confirmar",
            "Reiniciar adaptadores?\nA conexão será interrompida brevemente.",
        ):
            subprocess.Popen(
                "wmic path win32_networkadapter call disable && "
                "timeout /t 3 && wmic path win32_networkadapter call enable",
                shell=True,
            )
            self.logger.log_success("Reinício de adaptadores de rede iniciado")

    def _show_cmd_output(self, title, cmd):
        def _run():
            out = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
            win = ctk.CTkToplevel()
            win.title(title)
            win.geometry("800x500")
            win.configure(fg_color="#1e1e2e")
            tb = ctk.CTkTextbox(win, font=ctk.CTkFont(family="Consolas", size=11))
            tb.pack(fill="both", expand=True, padx=10, pady=10)
            tb.insert("end", out)
            tb.configure(state="disabled")
            self.logger.log_info(f"Comando executado: {cmd}")

        threading.Thread(target=_run, daemon=True).start()

    def show_ip_config(self):
        self._show_cmd_output("Configuração IP", "ipconfig /all")

    def show_route_table(self):
        self._show_cmd_output("Tabela de Roteamento", "route print")

    def show_network_stats(self):
        self._show_cmd_output("Estatísticas", "netstat -e")
