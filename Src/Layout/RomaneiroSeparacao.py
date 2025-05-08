from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from datetime import datetime

class RomaneioSeparacao:
    def __init__(self, pdf_filename, largura=80 * mm, comprimento=295 * mm):
        """
        Inicializa o gerador de PDF para romaneio de separação.
        :param pdf_filename: Nome do arquivo PDF a ser gerado.
        :param largura: Largura da página (em mm).
        :param comprimento: Comprimento da página (em mm).
        """
        self.pdf_filename = f"{pdf_filename}{self._gerar_timestamp()}.pdf" 
        self.largura = largura
        self.comprimento = comprimento
        self.c = canvas.Canvas(self.pdf_filename, pagesize=(largura, comprimento))
        self.fonte_titulo = ("Helvetica-Bold", 12)
        self.fonte_cabecalho = ("Helvetica-Bold", 8)
        self.fonte_itens = ("Helvetica", 7)
        self.fonte_info = ("Helvetica", 10)
        self.y_atual = self.comprimento - 35 * mm  # Posição inicial para os itens
        self.altura_linha = 12 * mm

    def adicionar_primeira_pagina(self):
        """
        Adiciona a primeira página com informações fixas, como título, cliente e vendedor.
        :param cliente: Nome do cliente.
        :param vendedor: Nome do vendedor.
        """
        # Título no centro da parte superior
        self.c.setFont(*self.fonte_titulo)
        titulo = "Romaneio de Separação"
        self.c.drawCentredString(self.largura / 2, self.comprimento - 6 * mm, titulo)

        # Cabeçalho das colunas
        self.c.setFont(*self.fonte_cabecalho)
        self.c.drawString(1 * mm, self.comprimento  - 21 * mm, "_"*50)
        self.c.drawString(6 * mm, self.comprimento - 25 * mm, "OS")
        self.c.drawString(15 * mm, self.comprimento - 25 * mm, "Vendedor")
        self.c.drawString(38 * mm, self.comprimento - 25 * mm, "Cod Fornecedor")
        self.c.drawString(65 * mm, self.comprimento - 25 * mm, "Marca")
        self.c.drawString(6 * mm, self.comprimento - 30 * mm, "Cod")
        self.c.drawString(15 * mm, self.comprimento - 30 * mm, "Desc")
        self.c.drawString(55 * mm, self.comprimento - 30 * mm, "Qnt.")
        self.c.drawString(65 * mm, self.comprimento - 30 * mm, "Local")
        self.c.drawString(1 * mm, self.comprimento  - 31 * mm, "_"*50)

    def adicionar_itens(self, itens):
        """
        Adiciona os itens ao PDF, criando novas páginas conforme necessário.
        :param itens: Lista de dicionários contendo os dados dos itens.
        """
        self.c.setFont(*self.fonte_itens)  # Definir a fonte para os itens
        print(itens)

        for item in itens:
            # Verificar se há espaço suficiente na página para mais uma linha
            #if self.y_atual < 20 * mm:  # Limite inferior da página
            #    self.c.showPage()  # Finaliza a página atual e inicia uma nova
            #    self.y_atual = self.comprimento - 35 * mm  # Reinicia a posição Y para a nova página
            #    self.c.setFont(*self.fonte_itens)  # Redefinir a fonte após criar uma nova página

            # Adicionar o item
            self.c.drawString(7 * mm, self.y_atual - 1, item[1]) #  Os
            self.c.drawString(16 * mm, self.y_atual - 1, str(item[7])[:10]) # Vendedor
            self.c.drawString(38 * mm, self.y_atual - 1, item[11]) # FORNECDOR
            self.c.drawString(65 * mm, self.y_atual - 1, str(item[10])[:10]) # Marca
            self.c.drawString(7 * mm, self.y_atual - 15, item[2]) # Cod Item
            self.c.drawString(18 * mm, self.y_atual - 15, str(item[5])[:22]) # Desc Item
            self.c.drawString(55 * mm, self.y_atual - 15, item[8]) # Qntidade
            self.c.drawString(58 * mm, self.y_atual - 15, item[9]) # unidade
            self.c.drawString(65 * mm, self.y_atual - 15, item[6]) # Local de estoque
            self.c.drawString(1 * mm, self.y_atual - 25, f"-"*110)

            self.y_atual -= self.altura_linha  # Move para a próxima linha

    def adicionar_assinatura(self, separador):
        """
        Adiciona um campo de assinatura na última página.
        """
        self.c.setFont(*self.fonte_info)
        self.c.drawString(15 * mm, self.y_atual - 20 * mm, "Ass: __________________")
        self.c.drawString(35 * mm, self.y_atual - 25 * mm, f"{separador}")

    def _gerar_timestamp(self):
        """
        Gera uma string no formato -dia-mes-ano-horaminutosegundo com dois dígitos para dia, mês, hora, minuto e segundo.
        :return: String formatada com a data e hora atual.
        """
        # Obter a data e hora atual
        agora = datetime.now()

        # Formatar a string utilizando :02d para garantir dois dígitos
        timestamp = f"-{agora.day:02d}-{agora.month:02d}-{agora.year}-{agora.hour:02d}{agora.minute:02d}{agora.second:02d}"
        return timestamp
    
    def salvar_pdf(self):
        """
        Finaliza e salva o PDF.
        """
        self.c.save()
        return self.pdf_filename
