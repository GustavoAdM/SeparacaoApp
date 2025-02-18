import configparser
import logging
from firebird.driver import driver_config, connect
from contextlib import contextmanager

class FirebirdDB:
    def __init__(self, config_file='Config\\Config.ini'):
        # Leitura do arquivo de configuração
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # Atribuindo os parâmetros de configuração
        self.usuario = self.config.get('database', 'usuario', fallback=None)
        self.senha = self.config.get('database', 'senha', fallback=None)
        self.ip = self.config.get('database', 'ip', fallback=None)
        self.caminho = self.config.get('database', 'caminho', fallback=None)
        self.porta = self.config.getint('database', 'porta', fallback=3050)  # Alterado para inteiro
        self.lib_path = self.config.get('database', 'lib_path', fallback=None)

        #Configurando conexão do Firebird
        driver_config.server_defaults.host.value = str(self.ip)
        driver_config.server_defaults.port.value = str(self.porta)
        driver_config.server_defaults.user.value = str(self.usuario)
        driver_config.server_defaults.password.value = str(self.senha)
        driver_config.fb_client_library.value = self.lib_path

        # Configuração do logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Verifica se as configurações necessárias estão presentes
        self._validate_config()

    def _validate_config(self):
        """Valida se todas as configurações necessárias estão presentes"""
        if not all([self.usuario, self.senha, self.ip, self.caminho]):
            raise ValueError("Parâmetros de conexão incompletos no arquivo de configuração.")

    @contextmanager
    def connect(self):
        """Context manager para gerenciar a conexão"""
        connection = None
        cursor = None
        try:
            connection = connect(self.caminho)
            cursor = connection.cursor()  # Obtemos o cursor a partir da conexão
            yield cursor
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise
        finally:
            if connection:
                connection.close()
                #self.logger.info("Conexão encerrada.")  # Isso pode ser descomentado para registrar o fechamento

    def execute_queries(self, query):
        """Executa uma consulta SELECT e retorna os resultados"""
        with self.connect() as cursor:
            try:
                cursor.execute(query)
                return cursor.fetchall()  # Retorna o resultado da consulta
            except Exception as e:
                self.logger.error(f"Erro ao executar a consulta: {e}")
                return None

    def execute_UDI(self, query):
        """Executa uma consulta de inserção, atualização ou exclusão"""
        with self.connect() as cursor:
            try:
                cursor.execute(query)
                cursor.connection.commit()  # Confirma a transação usando o commit da conexão
            except Exception as e:
                self.logger.error(f"Erro ao executar a consulta de UDI: {e}")
                cursor.connection.rollback()  # Faz rollback caso ocorra erro

# Exemplo de uso
db = FirebirdDB()
