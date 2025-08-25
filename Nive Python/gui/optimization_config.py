# gui/optimization_config.py - Configurações e constantes para otimização


class OptimizationConfig:
    """Configurações e constantes para o módulo de otimização"""

    # Versão do NiveBoost
    VERSION = "1.1.0"

    # Mensagens padrão
    RESTART_MESSAGE = "⚠️ IMPORTANTE: Reinicie o sistema para aplicar todas as mudanças!"
    ADMIN_WARNING = "⚠️ Execute como Administrador para melhores resultados!"
    IRREVERSIBLE_WARNING = "⚠️ Esta função é IRREVERSÍVEL sem um ponto de restauração!"

    # Configurações de interface
    PROGRESS_WINDOW_SIZE = "400x200"
    BUTTON_WIDTH = 45
    DESC_WRAP_LENGTH = 300

    # Timeouts e delays (em milissegundos)
    SUCCESS_WINDOW_DELAY = 3000
    WARNING_WINDOW_DELAY = 2000
    ERROR_WINDOW_DELAY = 1000
    RESULT_SHOW_DELAY = 500

    # Configurações de log
    MAX_ERRORS_DISPLAY = 5
    MAX_MAIN_ERRORS_DISPLAY = 3

    # Opções de otimização disponíveis
    OPTIMIZATION_OPTIONS = [
        {
            "text": "🔧 Desabilitar Alguns Serviços do Windows",
            "method": "disable_windows_services",
            "style": "warning",
            "description": "Desabilita serviços desnecessários para melhorar performance",
            "warning": "Esta operação irá desabilitar serviços desnecessários do Windows.",
        },
        {
            "text": "📅 Desabilitar Tweaks de Tarefas Agendadas",
            "method": "disable_scheduled_tasks",
            "style": "warning",
            "description": "Remove tarefas agendadas que consomem recursos",
            "warning": """Esta operação irá desabilitar tarefas agendadas desnecessárias:

• Tarefas de telemetria e coleta de dados
• Customer Experience Improvement Program
• Diagnósticos e manutenção automática
• Tarefas do Microsoft Office
• Atualizações automáticas do Edge
• File History e outras tarefas
• E diversas outras tarefas que consomem recursos...""",
        },
        {
            "text": "💾 Desabilitar Alguns Softwares do Windows",
            "method": "disable_windows_software",
            "style": "warning",
            "description": "Desabilita aplicativos e recursos desnecessários",
            "warning": "Esta operação irá desabilitar aplicativos e softwares desnecessários.",
        },
        {
            "text": "🕵️ Remover Telemetria e Coleta de Dados",
            "method": "remove_telemetry",
            "style": "danger",
            "description": "Remove sistemas de coleta de dados e telemetria",
            "warning": """Esta operação irá remover sistemas de telemetria e coleta de dados:

• Desabilitar telemetria do Windows
• Remover metadados de dispositivos da rede
• Desabilitar Customer Experience Improvement Program
• Desabilitar Application Compatibility tracking
• Desabilitar AutoLoggers de diagnóstico
• Desabilitar Windows SmartScreen
• Desabilitar controle da Assistência Remota
• Desabilitar ofertas do Malicious Software Removal Tool""",
        },
        {
            "text": "🗑️ Remover Features Não Usadas",
            "method": "remove_unused_features",
            "style": "warning",
            "description": "Remove recursos e funcionalidades não utilizadas",
            "warning": """Esta operação irá remover recursos e funcionalidades não utilizadas:

• Desabilitar IIS e componentes web
• Remover Message Queue (MSMQ)
• Desabilitar WCF e recursos de desenvolvimento
• Remover Hyper-V (se não utilizado)
• Remover apps opcionais (WordPad, IE, etc.)
• Desabilitar protocolo SMB1 (inseguro)
• Remover recursos de rede avançados
• E outras funcionalidades raramente usadas...""",
        },
        {
            "text": "🎨 Remover Animações Inúteis",
            "method": "remove_animations",
            "style": "info",
            "description": "Remove animações para melhorar a responsividade",
            "warning": """Esta operação irá desabilitar animações e efeitos visuais:

• Desabilitar animações de janelas
• Remover efeitos visuais avançados
• Desabilitar animações da barra de tarefas
• Otimizar arrastar janelas
• Desabilitar transparências desnecessárias
• Remover sombras em listas
• Otimizar suavização de fontes
• E outras otimizações visuais...""",
        },
        {
            "text": "🔍 Desabilitar Busca Web na Barra de Pesquisa",
            "method": "disable_web_search",
            "style": "info",
            "description": "Desabilita busca online na barra de pesquisa do Windows",
            "warning": "Esta operação irá desabilitar a busca online na barra de pesquisa.",
        },
        {
            "text": "🌐 Desabilitar Cache de Navegadores e Streaming",
            "method": "disable_browser_cache",
            "style": "warning",
            "description": "Otimiza cache de navegadores e serviços de streaming",
            "warning": "Esta operação irá otimizar o cache de navegadores e streaming.",
        },
        {
            "text": "🔒 Desabilitar Propagandas na Tela de Bloqueio",
            "method": "disable_lock_screen_ads",
            "style": "success",
            "description": "Remove propagandas e sugestões da tela de bloqueio",
            "warning": "Esta operação irá remover propagandas da tela de bloqueio.",
        },
        {
            "text": "🌍 Otimizar o Edge",
            "method": "optimize_edge",
            "style": "primary",
            "description": "Aplica otimizações específicas para o Microsoft Edge",
            "warning": """Esta operação irá aplicar otimizações específicas para o Microsoft Edge:

• Desabilitar sidebar/botão Bing
• Desabilitar execução em segundo plano
• Desabilitar inicialização automática
• Remover botão de assinatura Acrobat
• Desabilitar geolocalização por padrão
• Desabilitar acesso a sensores
• Desabilitar notificações de sites
• E outras otimizações de privacidade...""",
        },
        {
            "text": "⚡Acelerar Windows",
            "method": "accelerate_windows",
            "style": "success",
            "description": "Aplicação geral de otimizações para acelerar o sistema",
            "warning": """Esta operação irá aplicar 12 otimizações específicas para acelerar o sistema:

• Otimização de Boot
• Aceleração do Menu Iniciar
• Aumento da Taxa de Upload
• Otimização TCP/IP e DNS
• GPU Hardware Scheduling
• Modo Compacto no Explorer
• Desabilitar Apps em Background
• Otimização para Jogos
• E outras melhorias...""",
        },
    ]

    # Texto de aviso principal
    WARNING_TEXT = """🔴 ATENÇÃO: Estas funções são IRREVERSÍVEIS a não ser que tenha criado um ponto de restauração!

📋 RECOMENDAÇÕES OBRIGATÓRIAS:
• Crie um ponto de restauração ANTES de usar qualquer função
• Leia as informações sobre cada otimização antes de aplicar
• Não execute mais de uma otimização por vez
• Execute como Administrador para melhores resultados
• Reinicie o sistema após aplicar as otimizações

⚠️ Use por sua conta e risco. Sempre faça backup do seu sistema!"""

    @staticmethod
    def get_optimization_by_method(method_name):
        """Obter configuração de otimização pelo nome do método"""
        for option in OptimizationConfig.OPTIMIZATION_OPTIONS:
            if option["method"] == method_name:
                return option
        return None

    @staticmethod
    def get_warning_message(method_name):
        """Obter mensagem de aviso formatada para um método específico"""
        option = OptimizationConfig.get_optimization_by_method(method_name)
        if not option:
            return "Operação de otimização não encontrada."

        warning = option["warning"]
        full_warning = f"{warning}\n\n{OptimizationConfig.IRREVERSIBLE_WARNING}\n{OptimizationConfig.ADMIN_WARNING}\n\nDeseja continuar?"

        return full_warning
