from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import configparser
import logging

class FirebirdDB:
    def __init__(self, config_file='Config/Config.ini'):
        # Lê o arquivo de configuração INI
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # Carrega os parâmetros de conexão
        usuario = self.config.get('database', 'usuario')
        senha = self.config.get('database', 'senha')
        ip = self.config.get('database', 'ip')
        porta = self.config.get('database', 'porta', fallback='3050')
        caminho = self.config.get('database', 'caminho')

        # Monta a URL de conexão compatível com SQLAlchemy
        self.db_url = f"firebird+fdb://{usuario}:{senha}@{ip}:{porta}/{caminho}"

        # Cria o engine com um pool de conexões
        self.engine = create_engine(
            self.db_url,
            poolclass=QueuePool,   # Usa um pool do tipo fila (queue)
            pool_size=10,          # Número fixo de conexões mantidas abertas
            max_overflow=5,        # Conexões extras temporárias além do pool
            pool_timeout=30,       # Tempo máximo (segundos) para aguardar conexão livre
            pool_recycle=1800,     # Recicla conexões após 30 minutos (evita timeout de rede)
            echo=False             # Altere para True se quiser logar SQL no terminal
        )

        # Configura o logger para capturar erros e mensagens
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def execute_queries(self, query, params=None):
        """
        Executa uma consulta SELECT.
        :param query: string SQL com ou sem parâmetros (use :nome)
        :param params: dicionário com os parâmetros da query (opcional)
        :return: lista de dicionários com os resultados
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                return [dict(row) for row in result]
        except Exception as e:
            self.logger.error(f"Erro na consulta: {e}")
            return []

    def execute_udi(self, query, params=None):
        """
        Executa comandos INSERT, UPDATE ou DELETE.
        :param query: string SQL (com ou sem parâmetros)
        :param params: dicionário com os parâmetros da query (opcional)
        :return: None
        """
        try:
            # begin() inicia uma transação automática com commit no final
            with self.engine.begin() as conn:
                conn.execute(text(query), params or {})
        except Exception as e:
            self.logger.error(f"Erro na execução de UDI: {e}")
            raise  # Relevanta o erro para permitir tratamento externo, se necessário


db = FirebirdDB()