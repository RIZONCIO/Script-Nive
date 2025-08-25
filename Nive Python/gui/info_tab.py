import os
import sys
import subprocess
from pathlib import Path
from tkinter import messagebox
import webbrowser
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import *


class InfoTab:
    """Classe responsável pela aba de informações e créditos"""

    def __init__(self, parent_interface):
        """Inicializar aba de informações"""
        self.parent = parent_interface
        self.config = parent_interface.config

    # ==================== NOVO MÉTODO PARA ABRIR O PDF ====================
    def _get_doc_path(self) -> Path:
        """
        Retorna o caminho absoluto do PDF de documentação.
        """
        # Pega a pasta raiz do projeto
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
        return base_dir / "DOC" / "Documentação-Técnica-do-ScriptNive.pdf"

    def _open_local_doc(self):
        """
        Abre o PDF da documentação técnica com o leitor padrão do sistema.
        """
        pdf = self._get_doc_path()
        if not pdf.exists():
            messagebox.showerror(
                "Arquivo não encontrado", f"Não encontrei a documentação:\n{pdf}"
            )
            return

        try:
            if sys.platform.startswith("win"):
                os.startfile(str(pdf))  # Windows
            elif sys.platform == "darwin":
                subprocess.run(["open", str(pdf)], check=False)  # macOS
            else:
                subprocess.run(["xdg-open", str(pdf)], check=False)  # Linux
        except Exception:
            webbrowser.open(pdf.as_uri())  # Fallback caso os outros falhem

    # ======================================================================

    def create_info_tab(self, notebook):
        """Criar aba de informações e créditos"""
        info_tab = ttk_bs.Frame(notebook)
        notebook.add(info_tab, text=f"{self.config.get_icon('about')} Sobre")

        info_frame = ttk_bs.Frame(info_tab, padding=20)
        info_frame.pack(fill=BOTH, expand=True)

        # Logo/Título
        title = ttk_bs.Label(
            info_frame, text="ScriptNive", font=("Arial", 24, "bold"), bootstyle="info"
        )
        title.pack(pady=(0, 10))

        version = ttk_bs.Label(
            info_frame,
            text=f"Versão {self.config.version} - Interface Gráfica",
            font=("Arial", 12),
        )
        version.pack(pady=(0, 20))

        # Informações
        info_text = """ScriptNive é uma ferramenta completa para manutenção e otimização do Windows.
Desenvolvida para facilitar tarefas de manutenção que normalmente requerem
conhecimento técnico avançado.

Características:
• Interface gráfica moderna e intuitiva
• Ferramentas de diagnóstico avançado
• Limpeza automática do sistema
• Reparos automáticos de erros
• Otimização de performance
• Log detalhado de operações"""

        info_label = ttk_bs.Label(info_frame, text=info_text, justify=LEFT)
        info_label.pack(pady=(0, 20), anchor=W)

        # Créditos
        credits_frame = ttk_bs.LabelFrame(info_frame, text="Créditos", padding=15)
        credits_frame.pack(fill=X, pady=(0, 10))

        credits_text = """Criador do ScriptNive: Ryan Vinicius Carvalho Pereira
Criador do Reparo Completo: Ivo Dias
Criador do OtimizadorEdge: AFaustini
Interface Gráfica: Python + ttkbootstrap
Data de Lançamento: 10/Set./2022"""

        credits_label = ttk_bs.Label(credits_frame, text=credits_text, justify=LEFT)
        credits_label.pack(anchor=W)

        # Links (incluindo o da documentação)
        links_frame = ttk_bs.Frame(info_frame)
        links_frame.pack(fill=X, pady=(10, 0))

        links = [
            ("Documentação Técnica (PDF)", self._open_local_doc),
            ("Documentação Microsoft", self.config.get_link("microsoft_docs")),
            ("DOS Tips", self.config.get_link("dos_tips")),
            ("GitHub", self.config.get_link("github")),
        ]

        for text, action in links:
            if callable(action):
                cmd = action
            else:
                cmd = lambda u=action: webbrowser.open(u)
            ttk_bs.Button(
                links_frame,
                text=text,
                command=cmd,
                bootstyle="link",
            ).pack(side=LEFT, padx=5)

        return info_tab
