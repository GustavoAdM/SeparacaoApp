import os
import win32print
import configparser
import subprocess

class ElginLabelPrinter:
    def __init__(self, config_file=None):
        """
        Inicializa a classe. Se um arquivo .ini for informado, carrega as configurações.
        Caso contrário, utiliza valores padrão:
          - Impressora padrão do sistema.
          - Caminho base onde os relatórios (PDFs) estão armazenados.
          - Caminho para o Foxit PDF Reader.
        """
        self.config = {}
        if config_file:
            self.carregar_config(config_file)
        # Usa o nome da impressora definido no .ini ou a impressora padrão do Windows.
        self.printer_name = self.config.get('nome_printer', win32print.GetDefaultPrinter())
        # Caminho base onde os PDFs estão armazenados.
        self.caminho_base = self.config.get('caminho_base', '')
        # Caminho para o Foxit PDF Reader.
        self.foxit_path = self.config.get('foxit_path', r"C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitReader.exe")

    @staticmethod
    def listar_impressoras():
        """
        Retorna uma lista com os nomes de todas as impressoras instaladas.
        """
        printers = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
        return [printer[2] for printer in printers]

    def carregar_config(self, config_file):
        """
        Carrega as configurações do arquivo .ini e atualiza os atributos da classe.
        O arquivo .ini deve conter uma seção [impressao] com:
            nome_printer: Nome da impressora a ser utilizada.
            caminho_base: Caminho base onde os relatórios (PDFs) estão armazenados.
            foxit_path: Caminho para o executável do Foxit PDF Reader.
        """
        parser = configparser.ConfigParser()
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Arquivo de configuração '{config_file}' não encontrado.")
        parser.read(config_file)
        if 'impressao' not in parser:
            raise KeyError("A seção [impressao] não foi encontrada no arquivo de configuração.")
        impressao_config = parser['impressao']
        self.config['nome_printer'] = impressao_config.get('nome_printer', fallback=win32print.GetDefaultPrinter())
        self.config['caminho_base'] = impressao_config.get('caminho_base', fallback='')
        self.config['foxit_path'] = impressao_config.get('foxit_path', fallback="")

    def imprimir_pdf_com_foxit(self, nome_arquivo):
        """
        Envia o PDF para impressão utilizando o Foxit PDF Reader.
        
        O comando utilizado segue a sintaxe:
          FoxitReader.exe /t "caminho_do_pdf" "nome_impressora"
          
        Essa abordagem delega a conversão do PDF ao próprio Foxit.
        """
        caminho_completo = os.path.join(self.caminho_base, nome_arquivo)
        if not os.path.exists(caminho_completo):
            raise FileNotFoundError(f"Arquivo '{caminho_completo}' não encontrado.")
        
        # Monta o comando apenas com o caminho do PDF e o nome da impressora
        cmd = f'"{self.foxit_path}" /t "{caminho_completo}" "{self.printer_name}"'
        #print("Executando comando:", cmd)
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            raise Exception("Erro ao executar o comando de impressão via Foxit PDF Reader.")

    def imprimir_relatorio(self, nome_arquivo):
        """
        Atalho para imprimir um relatório (PDF) que está dentro do caminho base configurado.
        Exemplo de uso:
            impressora.imprimir_relatorio("relatorio1.pdf")
        """
        self.imprimir_pdf_com_foxit(nome_arquivo)
