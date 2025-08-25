from gui.base_interface import BaseInterface
from gui.main_tab import MainTab
from gui.system_tab import SystemTab
from gui.optimization_tab import OptimizationTab
from gui.tools_tab import ToolsTab
from gui.info_tab import InfoTab
from gui.software_manager_gui import SoftwareManagerGUI
from gui.repair_dialog import RepairDialog


class ScriptNiveInterface:
    """Classe da interface gráfica principal - Versão Refatorada"""

    def __init__(self, root, system_commands, logger, config):
        """Inicializar interface"""
        self.root = root
        self.system_commands = system_commands
        self.logger = logger
        self.config = config

        # Criar interface base
        self.base_interface = BaseInterface(root, system_commands, logger, config)

        # CORREÇÃO: Adicionar os placeholders na base_interface
        self.setup_placeholders()

        # Inicializar componentes das abas
        self.main_tab = MainTab(self.base_interface)
        self.system_tab = SystemTab(self.base_interface)
        self.optimization_tab = OptimizationTab(self.base_interface)
        self.tools_tab = ToolsTab(self.base_interface)
        self.info_tab = InfoTab(self.base_interface)

        # Inicializar componentes de diálogos
        self.software_manager = SoftwareManagerGUI(self.base_interface)
        self.repair_dialog = RepairDialog(self.base_interface)

        # Criar interface
        self.create_widgets()

    def setup_placeholders(self):
        self.base_interface.reinstall_software_placeholder = (
            self.reinstall_software_placeholder
        )
        self.base_interface.complete_repair_placeholder = (
            self.complete_repair_placeholder
        )

    def create_widgets(self):
        """Criar todos os widgets da interface"""
        # Configurar estrutura base
        main_frame = self.base_interface.setup_base_widgets()

        # Criar todas as abas
        self.create_all_tabs()

        # Configurar logger para usar o widget de texto após criação das abas
        if hasattr(self.tools_tab, "log_text"):
            self.logger.set_widget(self.tools_tab.log_text)

    def create_all_tabs(self):
        """Criar todas as abas do notebook"""
        notebook = self.base_interface.notebook

        # Criar cada aba
        self.main_tab.create_main_tab(notebook)
        self.system_tab.create_system_tab(notebook)
        self.optimization_tab.create_optimization_tab(notebook)
        self.tools_tab.create_tools_tab(notebook)
        self.info_tab.create_info_tab(notebook)

    # Métodos de conveniência para acessar funcionalidades das abas
    def update_status(self, message):
        """Atualizar mensagem de status"""
        self.base_interface.update_status(message)

    def log_activity(self, message):
        """Registrar atividade no log"""
        self.base_interface.log_activity(message)

    # Métodos que são chamados pelas abas (delegação)
    def reinstall_software_placeholder(self):
        """Delegar para o gerenciador de software"""
        return self.software_manager.reinstall_software_placeholder()

    def complete_repair_placeholder(self):
        """Delegar para o diálogo de reparo"""
        return self.repair_dialog.complete_repair_placeholder()

    # Propriedades para compatibilidade com código existente
    @property
    def status_var(self):
        return self.base_interface.status_var

    @property
    def notebook(self):
        return self.base_interface.notebook

    @property
    def progress(self):
        return self.base_interface.progress
