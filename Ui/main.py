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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1350, 750)
        MainWindow.setMinimumSize(QSize(1350, 750))
        MainWindow.setMaximumSize(QSize(1350, 750))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ListaPedido = QTableWidget(self.centralwidget)
        if (self.ListaPedido.columnCount() < 10):
            self.ListaPedido.setColumnCount(10)
        
        # Ocultar
        self.ListaPedido.setColumnHidden(0, True)
        self.ListaPedido.setColumnHidden(1, True)
        self.ListaPedido.setColumnHidden(2, True)

        # Tamanho colunas
        self.ListaPedido.setColumnWidth(5, 200)
        self.ListaPedido.setColumnWidth(6, 200)

        __qtablewidgetitem = QTableWidgetItem()
        self.ListaPedido.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.ListaPedido.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.ListaPedido.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        font = QFont()
        font.setPointSize(10)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem4.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem5.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem6.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setFont(font);
        self.ListaPedido.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        self.ListaPedido.setObjectName(u"ListaPedido")
        self.ListaPedido.setGeometry(QRect(10, 10, 1091, 341))
        self.ListaPedido.setStyleSheet(u"font: 75 10pt \"Arial\";")
        self.ListaPedido.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ListaPedido.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.infos = QLineEdit(self.centralwidget)
        self.infos.setObjectName(u"infos")
        self.infos.setGeometry(QRect(20, 696, 911, 41))
        self.usuario = QComboBox(self.centralwidget)
        self.usuario.addItem("")
        self.usuario.setObjectName(u"usuario")
        self.usuario.setGeometry(QRect(1138, 35, 191, 61))
        self.usuario.setStyleSheet(u"font: 75 12pt \"Arial\";")
        self.iniciar = QPushButton(self.centralwidget)
        self.iniciar.setObjectName(u"iniciar")
        self.iniciar.setGeometry(QRect(1168, 143, 131, 61))
        self.iniciar.setStyleSheet(u"background-color: rgb(0, 255, 0);\n"
"font: 75 12pt \"Arial\";")
        self.cancelar = QPushButton(self.centralwidget)
        self.cancelar.setObjectName(u"cancelar")
        self.cancelar.setGeometry(QRect(1168, 143, 131, 61))
        self.cancelar.setStyleSheet(u"background-color: rgb(255, 255, 0);\n"
"font: 75 12pt \"Arial\";")
        self.finalizar = QPushButton(self.centralwidget)
        self.finalizar.setObjectName(u"finalizar")
        self.finalizar.setGeometry(QRect(1168, 225, 131, 61))
        self.finalizar.setStyleSheet(u"background-color: rgb(255, 0, 0);\n"
"font: 75 12pt \"Arial\";")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(1151, 367, 171, 41))
        self.lineEdit.setStyleSheet(u"font: 75 12pt \"Arial\";")
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(1151, 417, 171, 41))
        self.lineEdit_2.setStyleSheet(u"font: 75 12pt \"Arial\";")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(1151, 467, 171, 41))
        self.lineEdit_3.setStyleSheet(u"font: 75 12pt \"Arial\";")
        self.lineEdit_3.setReadOnly(True)
        self.Empresa = QLineEdit(self.centralwidget)
        self.Empresa.setObjectName(u"Empresa")
        self.Empresa.setGeometry(QRect(1222, 694, 91, 42))
        self.Empresa.setStyleSheet(u"font: 75 10pt \"Arial\";")
        self.Empresa.setReadOnly(True)
        self.TW_ordemservico = QTableWidget(self.centralwidget)
        if (self.TW_ordemservico.columnCount() < 16):
            self.TW_ordemservico.setColumnCount(16)
        
          # Ocultar
        self.TW_ordemservico.setColumnHidden(0, True)
        self.TW_ordemservico.setColumnHidden(1, True)
        self.TW_ordemservico.setColumnHidden(2, True)
        self.TW_ordemservico.setColumnHidden(3, True)
        self.TW_ordemservico.setColumnHidden(4, True)
        self.TW_ordemservico.setColumnHidden(5, True)
        self.TW_ordemservico.setColumnHidden(6, True)
        self.TW_ordemservico.setColumnHidden(7, True)
        self.TW_ordemservico.setColumnHidden(8, True)
        self.TW_ordemservico.setColumnHidden(9, True)

        # Tamanho colunas
        self.TW_ordemservico.setColumnWidth(11, 200)
        self.TW_ordemservico.setColumnWidth(12, 200)
        self.TW_ordemservico.setColumnWidth(13, 340)

        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setTextAlignment(Qt.AlignCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(2, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(3, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(4, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(5, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(6, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(7, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(8, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(9, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setTextAlignment(Qt.AlignCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(10, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setTextAlignment(Qt.AlignHCenter|Qt.AlignBottom);
        self.TW_ordemservico.setHorizontalHeaderItem(11, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(12, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(13, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setTextAlignment(Qt.AlignCenter);
        self.TW_ordemservico.setHorizontalHeaderItem(14, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.TW_ordemservico.setHorizontalHeaderItem(15, __qtablewidgetitem25)
        self.TW_ordemservico.setObjectName(u"TW_ordemservico")
        self.TW_ordemservico.setGeometry(QRect(11, 370, 1091, 310))
        self.TW_ordemservico.setStyleSheet(u"font: 75 10pt \"Arial\";")
        self.TW_ordemservico.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.TW_ordemservico.setDragEnabled(False)
        self.TW_ordemservico.setAlternatingRowColors(False)
        self.TW_ordemservico.setSelectionMode(QAbstractItemView.MultiSelection)
        self.TW_ordemservico.setSelectionBehavior(QAbstractItemView.SelectRows)
        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.ListaPedido, self.usuario)
        QWidget.setTabOrder(self.usuario, self.iniciar)
        QWidget.setTabOrder(self.iniciar, self.cancelar)
        QWidget.setTabOrder(self.cancelar, self.finalizar)
        QWidget.setTabOrder(self.finalizar, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.Empresa)
        QWidget.setTabOrder(self.Empresa, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.infos)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SeparacaoApp", None))
        ___qtablewidgetitem = self.ListaPedido.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Tipo", None));
        ___qtablewidgetitem1 = self.ListaPedido.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem2 = self.ListaPedido.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Empresa", None));
        ___qtablewidgetitem3 = self.ListaPedido.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Urgencia", None));
        ___qtablewidgetitem4 = self.ListaPedido.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Pedido", None));
        ___qtablewidgetitem5 = self.ListaPedido.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Cliente", None));
        ___qtablewidgetitem6 = self.ListaPedido.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Vendedor", None));
        ___qtablewidgetitem7 = self.ListaPedido.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Data", None));
        ___qtablewidgetitem8 = self.ListaPedido.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Hora", None));
        ___qtablewidgetitem9 = self.ListaPedido.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Separador", None));
        self.usuario.setItemText(0, "")

        self.iniciar.setText(QCoreApplication.translate("MainWindow", u"Iniciar", None))
        self.cancelar.setText(QCoreApplication.translate("MainWindow", u"Cancelar", None))
        self.finalizar.setText(QCoreApplication.translate("MainWindow", u"Finalizar", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Alto - Balc\u00e3o", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"Medio - MotoBoy", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"Baixo - Despache", None))
        self.Empresa.setText("")
        ___qtablewidgetitem10 = self.TW_ordemservico.horizontalHeaderItem(0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Tipo", None));
        ___qtablewidgetitem11 = self.TW_ordemservico.horizontalHeaderItem(1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem12 = self.TW_ordemservico.horizontalHeaderItem(2)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Empresa", None));
        ___qtablewidgetitem13 = self.TW_ordemservico.horizontalHeaderItem(3)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"CodItem", None));
        ___qtablewidgetitem14 = self.TW_ordemservico.horizontalHeaderItem(4)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"DescItem", None));
        ___qtablewidgetitem15 = self.TW_ordemservico.horizontalHeaderItem(5)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Locals", None));
        ___qtablewidgetitem16 = self.TW_ordemservico.horizontalHeaderItem(6)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"CodCliente", None));
        ___qtablewidgetitem17 = self.TW_ordemservico.horizontalHeaderItem(7)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"CodVendedor", None));
        ___qtablewidgetitem18 = self.TW_ordemservico.horizontalHeaderItem(8)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Unidade", None));
        ___qtablewidgetitem19 = self.TW_ordemservico.horizontalHeaderItem(9)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Marca", None));
        ___qtablewidgetitem20 = self.TW_ordemservico.horizontalHeaderItem(10)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Or\u00e7amento", None));
        ___qtablewidgetitem21 = self.TW_ordemservico.horizontalHeaderItem(11)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Cliente", None));
        ___qtablewidgetitem22 = self.TW_ordemservico.horizontalHeaderItem(12)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Vendedor", None));
        ___qtablewidgetitem23 = self.TW_ordemservico.horizontalHeaderItem(13)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Item", None));
        ___qtablewidgetitem24 = self.TW_ordemservico.horizontalHeaderItem(14)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Quant.", None));
        ___qtablewidgetitem25 = self.TW_ordemservico.horizontalHeaderItem(15)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"Separador", None));
    # retranslateUi

