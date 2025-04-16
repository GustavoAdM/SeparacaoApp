import configparser
import logging
from firebird.driver import driver_config, connect, TPB, Isolation, TraAccessMode, tpb
from contextlib import contextmanager
from queue import Queue, Empty
from threading import Lock

class FirebirdDB:
    def __init__(self, config_file='Config\\Config.ini', pool_size=10):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.usuario = self.config.get('database', 'usuario', fallback=None)
        self.senha = self.config.get('database', 'senha', fallback=None)
        self.ip = self.config.get('database', 'ip', fallback=None)
        self.caminho = self.config.get('database', 'caminho', fallback=None)
        self.porta = self.config.getint('database', 'porta', fallback=3050)
        self.lib_path = self.config.get('database', 'lib_path', fallback=None)

        driver_config.server_defaults.host.value = str(self.ip)
        driver_config.server_defaults.port.value = str(self.porta)
        driver_config.server_defaults.user.value = str(self.usuario)
        driver_config.server_defaults.password.value = str(self.senha)
        driver_config.fb_client_library.value = self.lib_path

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self._validate_config()

        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self.pool_lock = Lock()

        for _ in range(pool_size):
            self.pool.put(self._create_connection())

    def _validate_config(self):
        if not all([self.usuario, self.senha, self.ip, self.caminho]):
            raise ValueError("Parâmetros de conexão incompletos no arquivo de configuração.")

    def _create_connection(self):
        return connect(self.caminho)

    @contextmanager
    def get_connection(self):
        conn = None
        try:
            conn = self.pool.get(timeout=5)
            yield conn
        except Empty:
            self.logger.error("Pool de conexões esgotado.")
            raise
        finally:
            if conn:
                self.pool.put(conn)

    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            try:
                tpb_bytes = tpb(Isolation.READ_COMMITTED, TraAccessMode.READ)
                conn.begin(tpb=tpb_bytes)
                with conn.cursor() as cursor:
                    cursor.execute(query, params or [])
                    columns = [col[0] for col in cursor.description]
                    results = [tuple(row) for row in cursor.fetchall()]
                conn.commit()
                return results
            except Exception as e:
                self.logger.error(f"Erro na consulta read-only: {e}")
                conn.rollback()
                return []

    def execute_udi(self, query, params=None):
        with self.get_connection() as conn:
            try:
                conn.begin()
                with conn.cursor() as cursor:
                    cursor.execute(query, params or [])
                conn.commit()
            except Exception as e:
                self.logger.error(f"Erro na operação UDI: {e}")
                conn.rollback()

db = FirebirdDB()
