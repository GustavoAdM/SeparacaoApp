# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHeaderView,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_Separadorapp(object):
    def setupUi(self, Separadorapp):
        if not Separadorapp.objectName():
            Separadorapp.setObjectName(u"Separadorapp")
        Separadorapp.setWindowModality(Qt.NonModal)
        Separadorapp.resize(1350, 750)
        Separadorapp.setMinimumSize(QSize(1350, 750))
        Separadorapp.setMaximumSize(QSize(1350, 750))
        self.centralwidget = QWidget(Separadorapp)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ListaPedido = QTableWidget(self.centralwidget)
        if (self.ListaPedido.columnCount() < 10):
            self.ListaPedido.setColumnCount(10)
        
        # Tamanho
        self.ListaPedido.setColumnWidth(0, 80)
        self.ListaPedido.setColumnWidth(1, 90)
        self.ListaPedido.setColumnWidth(2, 80)
        self.ListaPedido.setColumnWidth(3, 80)
        self.ListaPedido.setColumnWidth(4, 270)
        self.ListaPedido.setColumnWidth(5, 270)

        # Index Invisiveis
        self.ListaPedido.verticalHeader().setVisible(False)

        # Ocultar colunas de índice 6 em diante
        for col in range(7, self.ListaPedido.columnCount()):
            self.ListaPedido.setColumnHidden(col, True)

        font = QFont()
        font.setPointSize(8)

        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem1.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem2.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem3.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem4.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem5.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.ListaPedido.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.ListaPedido.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.ListaPedido.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        self.ListaPedido.setObjectName(u"ListaPedido")
        self.ListaPedido.setGeometry(QRect(10, 10, 1091, 341))
        self.ListaPedido.setStyleSheet(u"font: 75 10pt \"Arial\";")
        self.ListaPedido.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ListaPedido.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.infos = QLineEdit(self.centralwidget)
        self.infos.setObjectName(u"infos")
        self.infos.setGeometry(QRect(20, 696, 911, 41))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(1130, 370, 171, 41))
        self.lineEdit.setStyleSheet(u"font: 75 12pt \"Arial\";")
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(1130, 420, 171, 41))
        self.lineEdit_2.setStyleSheet(u"font: 75 12pt \"Arial\";")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(1130, 470, 171, 41))
        self.lineEdit_3.setStyleSheet(u"font: 75 12pt \"Arial\";")
        self.lineEdit_3.setReadOnly(True)
        self.Empresa = QLineEdit(self.centralwidget)
        self.Empresa.setObjectName(u"Empresa")
        self.Empresa.setGeometry(QRect(1222, 694, 91, 42))
        self.Empresa.setStyleSheet(u"font: 75 10pt \"Arial\";")
        self.Empresa.setReadOnly(True)
        self.TW_ordemservico = QTableWidget(self.centralwidget)
        if (self.TW_ordemservico.columnCount() < 18):
            self.TW_ordemservico.setColumnCount(18)
        
        # Tamanho
        self.TW_ordemservico.setColumnWidth(0, 65)
        self.TW_ordemservico.setColumnWidth(1, 270)
        self.TW_ordemservico.setColumnWidth(2, 150)
        self.TW_ordemservico.setColumnWidth(3, 145)
        self.TW_ordemservico.setColumnWidth(4, 295)
        self.TW_ordemservico.setColumnWidth(5, 50)

        # Index Invisiveis
        self.TW_ordemservico.verticalHeader().setVisible(False)

        # Ocultar colunas de índice 6 em diante
        for col in range(7, self.TW_ordemservico.columnCount()):
            self.TW_ordemservico.setColumnHidden(col, True)
            
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setTextAlignment(Qt.AlignCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setTextAlignment(Qt.AlignCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(8, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(9, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(10, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(11, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(12, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(13, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(14, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(15, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(16, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(17, __qtablewidgetitem27)
        self.TW_ordemservico.setObjectName(u"TW_ordemservico")
        self.TW_ordemservico.setGeometry(QRect(11, 370, 1091, 310))
        self.TW_ordemservico.setStyleSheet(u"font: 75 10pt \"Arial\";")
        self.TW_ordemservico.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.TW_ordemservico.setDragEnabled(False)
        self.TW_ordemservico.setAlternatingRowColors(False)
        self.TW_ordemservico.setSelectionMode(QAbstractItemView.MultiSelection)
        self.TW_ordemservico.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.exbir_iniciar = QWidget(self.centralwidget)
        self.exbir_iniciar.setObjectName(u"exbir_iniciar")
        self.exbir_iniciar.setEnabled(True)
        self.exbir_iniciar.setGeometry(QRect(1116, 20, 221, 191))
        self.usuario = QComboBox(self.exbir_iniciar)
        self.usuario.addItem("")
        self.usuario.setObjectName(u"usuario")
        self.usuario.setGeometry(QRect(20, 10, 191, 61))
        self.usuario.setStyleSheet(u"font: 75 12pt \"Arial\";")
        self.iniciar = QPushButton(self.exbir_iniciar)
        self.iniciar.setObjectName(u"iniciar")
        self.iniciar.setGeometry(QRect(30, 120, 161, 61))
        self.iniciar.setStyleSheet(u"background-color: rgb(0, 255, 0);\n"
"font: 75 12pt \"Arial\";")
        self.exibir_finalizar = QWidget(self.centralwidget)
        self.exibir_finalizar.setObjectName(u"exibir_finalizar")
        self.exibir_finalizar.setGeometry(QRect(1116, 20, 221, 190))
        self.cancelar = QPushButton(self.exibir_finalizar)
        self.cancelar.setObjectName(u"cancelar")
        self.cancelar.setGeometry(QRect(30, 10, 161, 61))
        self.cancelar.setStyleSheet(u"background-color: rgb(255, 255, 0);\n"
"font: 75 12pt \"Arial\";")
        self.finalizar = QPushButton(self.exibir_finalizar)
        self.finalizar.setObjectName(u"finalizar")
        self.finalizar.setGeometry(QRect(31, 120, 161, 61))
        self.finalizar.setStyleSheet(u"background-color: rgb(255, 0, 0);\n"
"font: 75 12pt \"Arial\";")
        Separadorapp.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.ListaPedido, self.usuario)
        QWidget.setTabOrder(self.usuario, self.iniciar)
        QWidget.setTabOrder(self.iniciar, self.cancelar)
        QWidget.setTabOrder(self.cancelar, self.finalizar)
        QWidget.setTabOrder(self.finalizar, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.Empresa)
        QWidget.setTabOrder(self.Empresa, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.infos)

        self.retranslateUi(Separadorapp)

        QMetaObject.connectSlotsByName(Separadorapp)
    # setupUi

    def retranslateUi(self, Separadorapp):
        Separadorapp.setWindowTitle(QCoreApplication.translate("Separadorapp", u"SearacaoApp", None))
        ___qtablewidgetitem = self.ListaPedido.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Separadorapp", u"Urgencia", None));
        ___qtablewidgetitem1 = self.ListaPedido.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Separadorapp", u"Data", None));
        ___qtablewidgetitem2 = self.ListaPedido.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Separadorapp", u"Hora", None));
        ___qtablewidgetitem3 = self.ListaPedido.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Separadorapp", u"Pedido", None));
        ___qtablewidgetitem4 = self.ListaPedido.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Separadorapp", u"Cliente", None));
        ___qtablewidgetitem5 = self.ListaPedido.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Separadorapp", u"Vendedor", None));
        ___qtablewidgetitem6 = self.ListaPedido.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Separadorapp", u"Separador", None));
        ___qtablewidgetitem7 = self.ListaPedido.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Separadorapp", u"_TIPO", None));
        ___qtablewidgetitem8 = self.ListaPedido.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Separadorapp", u"_STATUS", None));
        ___qtablewidgetitem9 = self.ListaPedido.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Separadorapp", u"_CD_EMPRESA", None));
        self.lineEdit.setText(QCoreApplication.translate("Separadorapp", u"Alto - Balc\u00e3o", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Separadorapp", u"Medio - MotoBoy", None))
        self.lineEdit_3.setText(QCoreApplication.translate("Separadorapp", u"Baixo - Despache", None))
        self.Empresa.setText("")
        ___qtablewidgetitem10 = self.TW_ordemservico.horizontalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Separadorapp", u"OS", None));
        ___qtablewidgetitem11 = self.TW_ordemservico.horizontalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Separadorapp", u"Veiculo", None));
        ___qtablewidgetitem12 = self.TW_ordemservico.horizontalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Separadorapp", u"Vendedor", None));
        ___qtablewidgetitem13 = self.TW_ordemservico.horizontalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Separadorapp", u"Mecanico", None));
        ___qtablewidgetitem14 = self.TW_ordemservico.horizontalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Separadorapp", u"Item", None));
        ___qtablewidgetitem15 = self.TW_ordemservico.horizontalHeaderItem(5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Separadorapp", u"Qtde", None));
        ___qtablewidgetitem16 = self.TW_ordemservico.horizontalHeaderItem(6)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Separadorapp", u"Separador", None));
        ___qtablewidgetitem17 = self.TW_ordemservico.horizontalHeaderItem(7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Separadorapp", u"_ID", None));
        ___qtablewidgetitem18 = self.TW_ordemservico.horizontalHeaderItem(8)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Separadorapp", u"_CD_EMPRESA", None));
        ___qtablewidgetitem19 = self.TW_ordemservico.horizontalHeaderItem(9)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Separadorapp", u"_CD_ITEM", None));
        ___qtablewidgetitem20 = self.TW_ordemservico.horizontalHeaderItem(10)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Separadorapp", u"_STATUS", None));
        ___qtablewidgetitem21 = self.TW_ordemservico.horizontalHeaderItem(11)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("Separadorapp", u"_CD_FORNECEDOR", None));
        ___qtablewidgetitem22 = self.TW_ordemservico.horizontalHeaderItem(12)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("Separadorapp", u"_CD_VENDEDOR", None));
        ___qtablewidgetitem23 = self.TW_ordemservico.horizontalHeaderItem(13)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("Separadorapp", u"_NM_CLIENTE", None));
        ___qtablewidgetitem24 = self.TW_ordemservico.horizontalHeaderItem(14)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("Separadorapp", u"_SG_UNIMED", None));
        ___qtablewidgetitem25 = self.TW_ordemservico.horizontalHeaderItem(15)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("Separadorapp", u"_LOCALS", None));
        ___qtablewidgetitem26 = self.TW_ordemservico.horizontalHeaderItem(16)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("Separadorapp", u"_MARCA", None));
        ___qtablewidgetitem27 = self.TW_ordemservico.horizontalHeaderItem(17)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("Separadorapp", u"_DT_REGISTRO", None));
        self.usuario.setItemText(0, "")

        self.iniciar.setText(QCoreApplication.translate("Separadorapp", u"Iniciar", None))
        self.cancelar.setText(QCoreApplication.translate("Separadorapp", u"Cancelar", None))
        self.finalizar.setText(QCoreApplication.translate("Separadorapp", u"Finalizar", None))
    # retranslateUi

