import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import QModelIndex, Qt, QTimer, QThread, Signal
from Ui.main import Ui_MainWindow
from Src.Database.Queries import (pedidos_nao_separados, inserir_inicio, cancelar,
                                  finalizar, orcamentos_separacao, inserir_orcamento,
                                  cacelar_orcamento, finalizar_orcamento)
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
                data = pedidos_nao_separados(empresa=self.empresa)
            elif self.tabela == "O":
                data = orcamentos_separacao(cd_empresa=self.empresa)

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
        self.ui = Ui_MainWindow()
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
        self.pedido = []
        self.usuario = None
        self.empresa = None
        self.tipo_tabela = ""
        self.limpar_pedidos = False

        # Timer para atualizar a tabela a cada 10 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_data_to_table)
        self.timer.start(10000)

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
            self.limpar_pedidos = True
            self.ui.TW_ordemservico.clearSelection()

            self.tipo_tabela = 'P'
            row = index.row()
            self.pedido = self.get_value_nrpedido(row)
            self.empresa = self.get_empresa_pedido(row)
            status_pedido = self.get_status_pedido(row)

            self.ui.usuario.setCurrentIndex(0)

            if status_pedido != 'N':
                self.mostrar_encerrar()
            else:
                self.mostrar_iniciar()
        except Exception as e:
            self.info_error(f"Erro ao processar clique na tabela: {e}")

    def mostrar_iniciar(self):
        """Exibe os elementos para iniciar o processo."""
        self.ui.iniciar.show()
        self.ui.usuario.show()
        self.ui.cancelar.hide()
        self.ui.finalizar.hide()

    def mostrar_encerrar(self):
        """Exibe os elementos para encerrar o processo."""
        self.ui.iniciar.hide()
        self.ui.usuario.hide()
        self.ui.cancelar.show()
        self.ui.finalizar.show()

    def inserir_usuario(self):
        """Popula o campo de usuários com dados da configuração."""
        try:
            usuarios = self.config[self.USUARIO_KEY]['separador']
            usuarios_separados = usuarios.split(',')
            for usuario in usuarios_separados:
                if usuario:
                    self.ui.usuario.addItem(usuario)
        except Exception as e:
            self.info_error(f"Erro ao inserir usuários: {e}")

    def iniciar(self):
        """Inicia o pedido com a informação do usuário e pedido selecionados."""
        try:
            if not self.usuario:
                self.info_error(
                    "Campo usuário obrigatório. Por favor, preencha o campo usuário antes de continuar.")
                return

            if not self.pedido:
                self.info_error(
                    "Por favor, selecione um pedido para continuar.")

            if self.tipo_tabela == "P":
                inserir_inicio(
                    empresa=self.empresa, pedido=self.pedido[0], status='I', usuario=self.usuario)
            elif self.tipo_tabela == "O":
                for empresa, orcamento, item, status, id, *_ in self.pedido:
                    if status == "N":
                        inserir_orcamento(
                            cd_empresa=empresa, nr_orcamento=orcamento, cd_item=item, separador=self.usuario, id=id)
                self.ui.TW_ordemservico.clearSelection()
                self.gerar_romaneio()
                

            self.add_data_to_table()
            self.mostrar_encerrar()
        except Exception as e:
            self.info_error(f"Erro ao iniciar pedido: {e}")

    def cancelar(self):
        """Cancela o pedido selecionado."""
        try:
            if not self.pedido:
                self.info_error("Selecione um pedido para cancelar.")
                return

            if self.tipo_tabela == "P":
                cancelar(empresa=self.empresa, pedido=self.pedido[0])
            elif self.tipo_tabela == "O":
                for empresa, orcamento, item, status, id, *_ in self.pedido:
                    if status == "I":
                        cacelar_orcamento(
                            cd_empresa=empresa, nr_orcamento=orcamento, cd_item=item, separador=self.usuario, id=id)
                self.ui.TW_ordemservico.clearSelection()

            self.add_data_to_table()
            self.mostrar_iniciar()
        except Exception as e:
            self.info_error(f"Erro ao cancelar pedido: {e}")

    def finalizar(self):
        """Finaliza o pedido selecionado."""
        try:
            if not self.pedido:
                self.info_error("Selecione um pedido para finalizar.")
                return

            if self.tipo_tabela == "P":
                finalizar(empresa=self.empresa, pedido=self.pedido[0])
            elif self.tipo_tabela == "O":
                for empresa, orcamento, item, status, id, *_ in self.pedido:
                    if status == "I":
                        finalizar_orcamento(
                            cd_empresa=empresa, nr_orcamento=orcamento, cd_item=item, separador=self.usuario, id=id)

                self.ui.TW_ordemservico.clearSelection()

            self.add_data_to_table()
            self.mostrar_iniciar()
        except Exception as e:
            self.info_error(f"Erro ao finalizar pedido: {e}")

    def get_value_usuario(self):
        """Obtém o valor do usuário selecionado."""
        self.usuario = self.ui.usuario.currentText()

    def get_value_nrpedido(self, row):
        """Obtém o número do pedido na linha especificada."""
        try:
            self.tipo_tabela = "P"
            nr_pedido_index = self.ui.ListaPedido.model().index(row, 4)
            return [self.ui.ListaPedido.model().data(nr_pedido_index)]
        except Exception as e:
            self.info_error(f"Erro ao obter número do pedido: {e}")
            return None

    def get_status_pedido(self, row):
        """Obtém o status do pedido na linha especificada."""
        try:
            self.tipo_tabela = "P"
            status_index = self.ui.ListaPedido.model().index(row, 1)
            return self.ui.ListaPedido.model().data(status_index)
        except Exception as e:
            self.info_error(f"Erro ao obter status do pedido: {e}")
            return None

    def get_empresa_pedido(self, row):
        """Obtém a empresa do pedido na linha especificada."""
        try:
            empresa_pedido_index = self.ui.ListaPedido.model().index(row, 2)
            return self.ui.ListaPedido.model().data(empresa_pedido_index)
        except Exception as e:
            self.info_error(f"Erro ao obter empresa do pedido: {e}")
            return None

    def get_value_orcamento(self, selected, deselected):
        """Atualiza a lista de seleções quando as linhas são selecionadas ou desmarcadas"""
        if self.limpar_pedidos:
            self.pedido.clear()
            self.limpar_pedidos = False

        # Para cada linha desmarcada, removemos o código da lista
        self.ui.ListaPedido.clearSelection()

        # Desabilitar atualizações para evitar redraws frequentes
        self.ui.TW_ordemservico.setUpdatesEnabled(False)

        for index in deselected.indexes():
            row = index.row()

            # Acessa todas as células necessárias
            status = self.ui.TW_ordemservico.item(row, 1).text()
            cod_empres = self.ui.TW_ordemservico.item(row, 2).text()
            cod_item = self.ui.TW_ordemservico.item(row, 3).text()
            desc_item = self.ui.TW_ordemservico.item(row, 4).text()
            locais = self.ui.TW_ordemservico.item(row, 5).text()
            unidade = self.ui.TW_ordemservico.item(row, 8).text()
            marca = self.ui.TW_ordemservico.item(row, 9).text()
            nr_orcamento = self.ui.TW_ordemservico.item(row, 10).text()
            vendedor = self.ui.TW_ordemservico.item(row, 12).text()
            quantidade = self.ui.TW_ordemservico.item(row, 14).text()
            cd_fornecedor = self.ui.TW_ordemservico.item(row, 17).text()
            id = self.ui.TW_ordemservico.item(row, 16).text()

            # Cria uma tupla com as informações relevantes
            pedido = (cod_empres, nr_orcamento, cod_item, status, id, desc_item,
                      locais, vendedor, quantidade, unidade, marca, cd_fornecedor)

            # Verifica se o pedido está na lista de pedidos e remove
            if pedido in self.pedido:
                self.tipo_tabela = "O"
                self.pedido.remove(pedido)

                # Atualiza a interface dependendo do status
                if status == "N":
                    self.mostrar_iniciar()
                elif status == "I":
                    self.mostrar_encerrar()

        # Para cada linha selecionada, adicionamos o código à lista
        for index in selected.indexes():
            row = index.row()

            # Acessa todas as células necessárias
            status = self.ui.TW_ordemservico.item(row, 1).text()
            cod_empres = self.ui.TW_ordemservico.item(row, 2).text()
            cod_item = self.ui.TW_ordemservico.item(row, 3).text()
            desc_item = self.ui.TW_ordemservico.item(row, 4).text()
            locais = self.ui.TW_ordemservico.item(row, 5).text()
            unidade = self.ui.TW_ordemservico.item(row, 8).text()
            marca = self.ui.TW_ordemservico.item(row, 9).text()
            nr_orcamento = self.ui.TW_ordemservico.item(row, 10).text()
            vendedor = self.ui.TW_ordemservico.item(row, 12).text()
            quantidade = self.ui.TW_ordemservico.item(row, 14).text()
            cd_fornecedor = self.ui.TW_ordemservico.item(row, 17).text()
            id = self.ui.TW_ordemservico.item(row, 16).text()

            # Cria uma tupla com as informações relevantes
            pedido = (cod_empres, nr_orcamento, cod_item, status, id, desc_item,
                      locais, vendedor, quantidade, unidade, marca, cd_fornecedor)

            # Adiciona à lista se o pedido não estiver presente
            if pedido not in self.pedido:
                self.tipo_tabela = "O"
                self.pedido.append(pedido)

                # Atualiza a interface dependendo do status
                if status == "N":
                    self.mostrar_iniciar()
                elif status == "I":
                    self.mostrar_encerrar()

        # Reabilitar atualizações de UI
        self.ui.TW_ordemservico.setUpdatesEnabled(True)
        self.tipo_tabela = "O"

    def info_error(self, msg):
        """Exibe uma mensagem de erro na interface."""
        self.ui.infos.setText(f'Erro: {msg}')

    def click_tabela_orcamento(self):
        self.pedido.clear()

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
            self.update_table(self.ui.ListaPedido, data, tabela)
        elif tabela == "O":
            self.update_table(self.ui.TW_ordemservico, data, tabela)

    def update_table(self, table_widget, data, tabela):
        """Atualiza uma tabela com os dados fornecidos."""
        try:
            table_widget.setRowCount(len(data))
            # Desabilita atualizações visuais
            table_widget.setUpdatesEnabled(False)

            for row_idx, row_data in enumerate(data):
                for col_idx, item in enumerate(row_data):
                    item = item.isoformat() if isinstance(
                        item, (datetime.date, datetime.datetime)) else str(item)
                    cell = QTableWidgetItem(item)
                    if tabela == "P":
                        alignment = Qt.AlignLeft | Qt.AlignVCenter if col_idx in {
                            5, 6} else Qt.AlignCenter
                    elif tabela == "O":
                        alignment = Qt.AlignLeft | Qt.AlignVCenter if col_idx in {
                            11, 12, 13} else Qt.AlignCenter
                    cell.setTextAlignment(alignment)
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    table_widget.setItem(row_idx, col_idx, cell)

            # Reabilita atualizações visuais
            table_widget.setUpdatesEnabled(True)

        except Exception as e:
            self.info_error(f"Erro ao atualizar a tabela: {e}")

    def gerar_romaneio(self):
        caminho_pedf = self.config["impressao"]["caminho_relatorio"]
        pdf = RomaneioSeparacao(f"{caminho_pedf}\\{self.usuario}")
        pdf.adicionar_primeira_pagina()
        pdf.adicionar_itens(self.pedido)
        pdf.adicionar_assinatura(self.usuario)
        nome_arquivo = pdf.salvar_pdf()

        try:
            printer = ElginLabelPrinter('Config\\Config.ini')
            # printer.listar_impressoras()
            printer.imprimir_relatorio(nome_arquivo=nome_arquivo)
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
