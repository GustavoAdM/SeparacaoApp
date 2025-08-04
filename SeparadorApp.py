import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import QModelIndex, Qt, QTimer, QThread, Signal
from Ui.main import Ui_Separadorapp
from Src.Database.Queries import (pedidos_nao_separados, inserir_inicio, cancelar,
                                  finalizar, orcamentos_separacao, inserir_orcamento,
                                  cancelar_orcamento, finalizar_orcamento, encerrar_conexao)
from Src.Layout.RomaneiroSeparacao import RomaneioSeparacao
from Src.Utils.ElgineLabelPrinter import ElginLabelPrinter
import datetime
import configparser


class WorkerThread(QThread):
    # Defina um sinal para retornar os dados
    data_ready = Signal(list, str)

    def __init__(self, empresa, tabela, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.empresa = empresa
        self.tabela = tabela

    def run(self):
        """O código que será executado no thread."""
        try:

            # Obtém os dados (no seu caso, os pedidos)
            if self.tabela == "P":
                data = pedidos_nao_separados(empresas=self.empresa)
            elif self.tabela == "O":
                data = orcamentos_separacao(empresas=self.empresa)

            # Emite o sinal com os dados quando terminar
            self.data_ready.emit(data, self.tabela)
        except Exception as e:
            self.data_ready.emit([], "erro")
            print(f"Erro no WorkerThread: {e}")


class MainWindow(QMainWindow):
    # Definir constantes
    USUARIO_KEY = 'usuario'
    EMPRESA_KEY = 'empresa'

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Separadorapp()
        self.ui.setupUi(self)

        # Carregar configuração .ini
        self.config = self.load_config()

        # Carregar usuários
        self.inserir_usuario()

        # Inicializar a interface
        self.mostrar_iniciar()

        # Adicionar dados à tabela ao iniciar sistema
        self.add_data_to_table()

        # Gatilhos de eventos
        self.ui.ListaPedido.clicked.connect(self.on_click_table)
        self.ui.usuario.currentIndexChanged.connect(self.get_value_usuario)
        self.ui.iniciar.clicked.connect(self.iniciar)
        self.ui.cancelar.clicked.connect(self.cancelar)
        self.ui.finalizar.clicked.connect(self.finalizar)

        # Gatilhos de eventos Orçamento
        self.ui.TW_ordemservico.selectionModel(
        ).selectionChanged.connect(self.get_value_orcamento)

        # Variáveis de controle
        self.pedido = None
        self.ordemservico = []
        self.usuario = None
        self.empresa = None
        self.tipo_tabela = "P"
        self.user_separacao = ""

        # Timer para atualizar a tabela a cada 5 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_data_to_table)
        self.timer.start(5000)

    def load_config(self):
        """Carrega as configurações do arquivo INI."""
        try:
            config = configparser.ConfigParser()
            config.read('Config\\Config.ini')
            return config
        except Exception as e:
            self.info_error(f"Erro ao carregar a configuração: {e}")
            return None

    def on_click_table(self, index: QModelIndex):
        """Gatilho quando um item de qualquer tabela é clicado."""
        try:
            # Limpa a selecação e as OS selecionado da lista
            self.ui.TW_ordemservico.clearSelection()
            self.ordemservico.clear()
            self.tipo_tabela = "P"

            row = index.row()
            self.pedido = self.ui.ListaPedido.item(row, 3).text()
            self.empresa = self.ui.ListaPedido.item(row, 9).text()
            status_pedido = self.ui.ListaPedido.item(row, 8).text()
            self.user_separacao = self.ui.ListaPedido.item(row, 6).text()

            self.ui.usuario.setCurrentIndex(0)

            if status_pedido != 'N':
                self.mostrar_encerrar()
            else:
                self.mostrar_iniciar()
        except Exception as e:
            self.info_error(f"Erro ao processar clique na tabela: {e}")

    def get_value_orcamento(self, selected, deselected):
        """Atualiza a lista de seleções quando as linhas são selecionadas ou desmarcadas"""
        self.ui.ListaPedido.clearSelection()
        self.ui.TW_ordemservico.setUpdatesEnabled(False)
        self.pedido = None
        self.tipo_tabela = "O"
 
        def extrair_pedido(row):
            """Extrai as informações da linha como uma tupla de pedido"""
            def get(col): return self.ui.TW_ordemservico.item(row, col).text()
            return (
                get(8),  # EMPRESA
                get(0),  # nr_orcamento
                get(9),  # cod_item
                get(10),  # status
                get(7),  # id
                get(4),  # desc_item
                get(15),  # locais
                get(2),  # vendedor
                get(5),  # quantidade
                get(14),  # unidade
                get(16),  # marca
                get(11),  # cd_fornecedor
            )

        def atualizar_interface(status):
            if status == "N":
                self.mostrar_iniciar()
            elif status == "I":
                self.mostrar_encerrar()

        # Processa remoções
        for row in {i.row() for i in deselected.indexes()}:
            pedido = extrair_pedido(row)
            status = pedido[3]
            if pedido in self.ordemservico:
                self.user_separacao = self.ui.TW_ordemservico.item(
                    row, 6).text()
                self.ordemservico.remove(pedido)
                atualizar_interface(status)

        # Processa adições
        for row in {i.row() for i in selected.indexes()}:
            pedido = extrair_pedido(row)
            status = pedido[3]
            if pedido not in self.ordemservico:
                self.user_separacao = self.ui.TW_ordemservico.item(
                    row, 6).text()
                self.ordemservico.append(pedido)
                atualizar_interface(status)
        self.ui.TW_ordemservico.setUpdatesEnabled(True)

    def mostrar_iniciar(self):
        """Exibe os elementos para iniciar o processo."""
        self.ui.exbir_iniciar.show()
        self.ui.exibir_finalizar.hide()

    def mostrar_encerrar(self):
        """Exibe os elementos para encerrar o processo."""
        self.ui.exbir_iniciar.hide()
        self.ui.exibir_finalizar.show()

        if self.user_separacao in ["1 (procurando)", "52 (procurando)", "5 (procurando)"]:
            self.ui.cancelar.hide()
        else:
            self.ui.cancelar.show()

    def inserir_usuario(self):
        """Popula o campo de usuários com dados da configuração."""
        try:
            usuarios = self.config[self.USUARIO_KEY]['separador']
            usuarios_separados = usuarios.split(',')
            for usuario in usuarios_separados:
                if usuario:
                    self.ui.usuario.addItem(usuario.strip())
        except Exception as e:
            self.info_error(f"Erro ao inserir usuários: {e}")

    def get_value_usuario(self):
        """Obtém o valor do usuário selecionado."""
        self.usuario = self.ui.usuario.currentText()

    ########## Ação dos Botões ###########
    def iniciar(self):
        """Inicia o pedido com a informação do usuário e pedido selecionados."""
        try:
            if not self.usuario:
                self.info_error(
                    "Campo usuário obrigatório. Por favor, preencha o campo usuário antes de continuar.")
                return

            if not self.pedido and self.tipo_tabela == "P":
                self.info_error(
                    "Por favor, selecione um pedido ou uma ordem de serviço para continuar.")
                return
            elif not self.ordemservico and self.tipo_tabela == "O":
                self.info_error(
                    "Por favor, selecione um pedido ou uma ordem de serviço para continuar.")
                return

            if self.pedido and self.tipo_tabela == "P":

                inserir_inicio(
                    empresa=self.empresa,
                    pedido=self.pedido,
                    status='I',
                    usuario=self.usuario
                )

            elif self.ordemservico:
                for empresa, orcamento, item, status, idItem, *_ in self.ordemservico:
                    if status == "N":
                        inserir_orcamento(
                            cd_empresa=empresa,
                            nr_orcamento=orcamento,
                            cd_item=item,
                            separador=self.usuario,
                            id=idItem
                        )
                self.gerar_romaneio()
                self.ui.TW_ordemservico.clearSelection()

            self.add_data_to_table()
            self.mostrar_encerrar()

        except Exception as e:
            self.info_error(f"Erro ao iniciar pedido: {e}")

    def cancelar(self):
        """Cancela o pedido ou a ordem de serviço selecionada."""
        try:
            if not self.pedido and self.tipo_tabela == "P":
                self.info_error(
                    "Selecione um pedido ou ordem de serviço para cancelar.")
                return
            elif not self.ordemservico and self.tipo_tabela == "O":
                self.info_error(
                    "Selecione um pedido ou ordem de serviço para cancelar.")
                return

            if self.pedido:
                cancelar(empresa=self.empresa, pedido=self.pedido)

            elif self.ordemservico:
                for empresa, orcamento, item, status, iditem, *_ in self.ordemservico:
                    if status == "I":
                        cancelar_orcamento(
                            cd_empresa=empresa,
                            nr_orcamento=orcamento,
                            cd_item=item,
                            separador=self.usuario,
                            id=iditem
                        )
                self.ui.TW_ordemservico.clearSelection()

            self.add_data_to_table()
            self.mostrar_iniciar()

        except Exception as e:
            self.info_error(f"Erro ao cancelar pedido: {e}")

    def finalizar(self):
        """Finaliza o pedido ou a ordem de serviço selecionada."""
        try:
            if not self.pedido and self.tipo_tabela == "P":
                self.info_error(
                    "Selecione um pedido ou ordem de serviço para finalizar.")
                return
            elif not self.ordemservico and self.tipo_tabela == "O":
                self.info_error(
                    "Selecione um pedido ou ordem de serviço para finalizar.")
                return

            if self.pedido:
                finalizar(empresa=self.empresa, pedido=self.pedido)

            elif self.ordemservico:
                for empresa, orcamento, item, status, iditem, *_ in self.ordemservico:
                    if status == "I":
                        finalizar_orcamento(
                            cd_empresa=empresa,
                            nr_orcamento=orcamento,
                            cd_item=item,
                            separador=self.usuario,
                            id=iditem
                        )
                self.ui.TW_ordemservico.clearSelection()

            self.add_data_to_table()
            self.mostrar_iniciar()

        except Exception as e:
            self.info_error(f"Erro ao finalizar pedido: {e}")

    ######### ATUALIZAÇÃO DOS DADOS DA TABELA #########

    def add_data_to_table(self):
        """Atualiza os dados da tabela com os pedidos não separados."""
        try:
            codigoempresa = str(self.config[self.EMPRESA_KEY]['codigo'])
            self.ui.Empresa.setText(codigoempresa)

            # Crie o WorkerThread
            self.worker = WorkerThread(codigoempresa, "P", self)
            self.worker.data_ready.connect(self.update_table_from_thread)
            self.worker.start()

            # Para orçamentos
            self.worker_orcamento = WorkerThread(codigoempresa, "O", self)
            self.worker_orcamento.data_ready.connect(
                self.update_table_from_thread)
            self.worker_orcamento.start()

        except Exception as e:
            self.info_error(f'Erro ao buscar resultado do banco: {e}')

    def update_table_from_thread(self, data, tabela):
        """Método que será chamado quando o WorkerThread emitir os dados."""
        if tabela == "P":
            self.update_table(data, tabela, self.ui.ListaPedido)
        elif tabela == "O":
            self.update_table(data, tabela, self.ui.TW_ordemservico)

    def update_table(self, data, tabela, table_widget):
        """Atualiza uma tabela com os dados fornecidos."""
        try:
            table_widget.setRowCount(len(data))
            # Desabilita atualizações visuais
            table_widget.setUpdatesEnabled(True)

            for row_idx, row_data in enumerate(data):
                for col_idx, item in enumerate(row_data):
                    item = item.isoformat() if isinstance(
                        item, (datetime.date, datetime.datetime)) else str(item)
                    cell = QTableWidgetItem(item)
                    if tabela == "P":
                        alignment = Qt.AlignLeft | Qt.AlignVCenter if col_idx in {
                            0, 4, 5} else Qt.AlignCenter
                    elif tabela == "O":
                        alignment = Qt.AlignLeft | Qt.AlignVCenter if col_idx in {
                            1, 2, 3, 4} else Qt.AlignCenter
                    cell.setTextAlignment(alignment)
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    table_widget.setItem(row_idx, col_idx, cell)

        except Exception as e:
            self.info_error(f"Erro ao atualizar a tabela: {e}")

    def info_error(self, msg):
        """Exibe uma mensagem de erro na interface."""
        self.ui.infos.setText(f'Erro: {msg}')

    """
    ######### IMRESSAO DE ROMANEIO ###########
    """

    def gerar_romaneio(self):
        caminho_pedf = self.config["impressao"]["caminho_relatorio"]
        pdf = RomaneioSeparacao(f"{caminho_pedf}\\{self.usuario}")
        pdf.adicionar_primeira_pagina()
        pdf.adicionar_itens(self.ordemservico)
        pdf.adicionar_assinatura(self.usuario)
        nome_arquivo = pdf.salvar_pdf()

        try:
            printer = ElginLabelPrinter('Config\\Config.ini')
            # printer.listar_impressoras()
            printer.imprimir_relatorio(nome_arquivo=nome_arquivo)
        except Exception as e:
            print(f"Erro: {e}")

    ######## Encerrar processos e conexao DB ########

    def closeEvent(self, event):
        """Executado quando a janela é fechada"""
        # Fecha todas as conexões do banco
        encerrar_conexao()

        # Aceita o evento de fechamento
        event.accept()

    def safe_shutdown(self):
        """Fecha a janela de forma controlada"""
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(window.safe_shutdown)
    sys.exit(app.exec())
