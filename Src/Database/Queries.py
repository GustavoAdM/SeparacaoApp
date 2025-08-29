from .Connection import db


def encerrar_conexao():
    db.close_all()


def pedidos_nao_separados(empresas: int = 50):
    _query = f"""
        WITH PEDIDOS_SEPARACAO AS (
            SELECT
                'P' TIPO_TABLE,
                COALESCE(ES.STATUS, 'N') STATUS,
                P.CD_EMPRESA,
                CASE P.CD_TIPOPEDIDO
                    WHEN 0 THEN 'MB DEDICADO'
                    WHEN 1 THEN 'BALCÃO'
                    WHEN 2 THEN 'MOTOBOY'
                    WHEN 3 THEN 'DESPACHE'
                    ELSE 'NENHUM'
                 END NIVEL,
                P.NR_PEDIDO, PE.NM_PESSOA, PV.NM_PESSOA NM_VENDEDOR,
                P.DT_PEDIDO, P.HR_PEDIDO,
                COALESCE(ES.NM_USUARIO, '') SEPARADOR
            FROM PEDIDO P
                LEFT JOIN ITEMCONFERENCIAPEDIDO ICP ON (
                    ICP.CD_EMPRESA = P.CD_EMPRESA
                    AND ICP.NR_PEDIDO = P.NR_PEDIDO
                    AND ICP.TP_PEDIDO = P.TP_PEDIDO)
                LEFT JOIN EXTEND_SEPARACAO ES ON (
                    ES.CD_EMPRESA = P.CD_EMPRESA
                    AND ES.NR_PEDIDO = P.NR_PEDIDO)
                INNER JOIN PESSOA PE ON (PE.CD_PESSOA = P.CD_PESSOA)
                INNER JOIN PESSOA PV ON (PV.CD_PESSOA = P.CD_VENDEDOR)
            WHERE
                P.TP_PEDIDO = 'S'
                AND P.DT_PEDIDO = CURRENT_DATE
                AND P.CD_EMPRESA = {empresas}
                AND ICP.NR_PEDIDO IS NULL
                AND P.ST_PEDIDO NOT IN ('A', 'P', 'C')
                AND P.CD_TIPOPEDIDO IS NOT NULL
                AND P.NR_ORDEMSERVICO IS NULL
            ORDER BY P.CD_TIPOPEDIDO
        )
        SELECT
            NIVEL, DT_PEDIDO, HR_PEDIDO, NR_PEDIDO, 
            NM_PESSOA, NM_VENDEDOR, SEPARADOR, 
            TIPO_TABLE, STATUS, CD_EMPRESA
        FROM PEDIDOS_SEPARACAO PE
        WHERE PE.STATUS <> 'F'
        ORDER BY NR_PEDIDO
    """
    # Executa a consulta com os parâmetros
    resultado = db.execute_query(_query, params=empresas)
    return resultado


def inserir_inicio(empresa: int, pedido: int, status: str, usuario: str):
    """Insere início da separação com status e usuário"""
    _query = """
        INSERT INTO EXTEND_SEPARACAO (
            CD_EMPRESA, NR_PEDIDO, NM_USUARIO, STATUS, DT_INICIO, DT_FIM
        ) VALUES (
            ?, ?, ?, ?, CURRENT_TIMESTAMP, NULL
        )
    """
    db.execute_udi(query=_query, params=[empresa, pedido, usuario, status])


def cancelar(empresa: int, pedido: int):
    """Cancela uma separação (deleta o registro)"""
    _query = """
        DELETE FROM EXTEND_SEPARACAO
        WHERE CD_EMPRESA = ? AND NR_PEDIDO = ?
    """
    db.execute_udi(query=_query, params=[empresa, pedido])


def finalizar(empresa: int, pedido: int):
    """Finaliza a separação atualizando status e data de fim"""
    _query = """
        UPDATE EXTEND_SEPARACAO
        SET STATUS = 'F', DT_FIM = CURRENT_TIMESTAMP
        WHERE CD_EMPRESA = ? AND NR_PEDIDO = ?
    """
    db.execute_udi(query=_query, params=[empresa, pedido])


def orcamentos_separacao(empresas: int = 50):
    _query = f"""
    SELECT
    Y.NR_ORDEMSERVICO,
    Y.DS_VEICULO,
    Y.NM_VENDEDOR,
    Y.NM_MECANICO,
    Y.DS_ITEM,
    Y.QNT,
    Y.NM_SEPARADOR,
    Y.ID,
    Y.CD_EMPRESA,
    Y.CD_ITEM,
    Y.STATUS,
    Y.CD_FORNECEDOR1,
    Y.CD_VENDEDOR,
    Y.NM_CLIENTE,
    Y.SG_UNIDMED,
    Y.LOCALS,
    Y.DS_MARCA,
    Y.DT_REGISTRO


    FROM (
    WITH SERVICOCALCULADO AS (
        SELECT
            SI.CD_EMPRESA,
            SI.NR_ORDEMSERVICO,
            SI.CD_ITEM,
            MAX(COALESCE(SI.PS_SERVICOITEM, SI.QT_SERVICOITEM)) AS QT_SOLICITADA,
            SUM(COALESCE(EO.PS_PEDIDO, EO.QT_PEDIDA, 0)) AS QT_PEDIDA_E
        FROM SERVICOITEM SI
        LEFT JOIN EXTEND_ORDERMSERVICO EO 
            ON EO.CD_EMPRESA = SI.CD_EMPRESA 
            AND EO.NR_ORDERMSERVICO = SI.NR_ORDEMSERVICO 
            AND EO.CD_ITEM = SI.CD_ITEM
        WHERE SI.DT_REGISTRO BETWEEN CURRENT_TIMESTAMP-2 AND CURRENT_TIMESTAMP
            AND SI.CD_EMPRESA = {empresas}
        GROUP BY SI.CD_EMPRESA, SI.NR_ORDEMSERVICO, SI.CD_ITEM
        HAVING MAX(COALESCE(SI.PS_SERVICOITEM, SI.QT_SERVICOITEM)) >= SUM(COALESCE(EO.PS_PEDIDO, EO.QT_PEDIDA, 0))
        PLAN JOIN (SI ORDER PK_SERVICOITEM INDEX (SERVICOITEM_IDX40), EO INDEX (EXTEND_ORDERMSERVICO_IDX1))
    )
    SELECT
        'O' TIPO_TABLE,
        COALESCE(EO.STATUS, 'N') STATUS,
        OS.CD_EMPRESA,
        SI.CD_ITEM,
        I.DS_ITEM DESCR,
        LIST(DISTINCT LE.DS_LOCAL, ',') LOCALS,
        OS.CD_PESSOA,
        SI.CD_VENDEDOR,
        M.DS_MARCA,
        I.SG_UNIDMED,
        OS.NR_ORDEMSERVICO,
        PC.NM_PESSOA NM_CLIENTE,
        PV.NM_PESSOA NM_VENDEDOR,
        SI.CD_ITEM||' - '||I.DS_ITEM||' ('||LIST(DISTINCT LE.DS_LOCAL, ', ')||')' DS_ITEM,
        CAST(COALESCE(EO.PS_PEDIDO, EO.QT_PEDIDA, SI.PS_SERVICOITEM, SI.QT_SERVICOITEM)AS NUMERIC(15, 2)) QNT,
        COALESCE(EO.NM_SEPARADOR, '') NM_SEPARADOR,
        COALESCE(EO.ID, 1) ID, I.CD_FORNECEDOR1,
        COALESCE(MV.DS_MARCAVEICULO, '')||'-'||COALESCE(ML.DS_MODELOVEICULO, '')||'-'||COALESCE(V.NR_ANO, '')
            ||'-'||COALESCE(CV.DS_CORVEICULO, '') DS_VEICULO,
        PM.NM_PESSOA NM_MECANICO,
        SI.DT_REGISTRO
    FROM ORDEMSERVICO OS
    INNER JOIN SERVICOITEM SI ON (SI.CD_EMPRESA = OS.CD_EMPRESA
        AND SI.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO)
    INNER JOIN PESSOA PC ON (PC.CD_PESSOA = OS.CD_PESSOA)
    INNER JOIN PESSOA PV ON (PV.CD_PESSOA = SI.CD_VENDEDOR)
    INNER JOIN PESSOA PM ON (PM.CD_PESSOA = SI.CD_MECANICO)
    INNER JOIN ITEM I ON (I.CD_ITEM = SI.CD_ITEM)
    INNER JOIN MARCA M ON (M.CD_MARCA = I.CD_MARCA)
    INNER JOIN ITEMEMPRESA IL
        ON (IL.CD_ITEM = I.CD_ITEM
        AND IL.CD_EMPRESA = {empresas})
    INNER JOIN LOCALESTOQUE LE ON (LE.CD_TIPOLOCAL = IL.CD_TIPOLOCAL
        AND LE.CD_LOCAL = IL.CD_LOCAL)
    LEFT JOIN EXTEND_ORDERMSERVICO EO ON (EO.CD_EMPRESA = SI.CD_EMPRESA
        AND EO.NR_ORDERMSERVICO = SI.NR_ORDEMSERVICO
        AND EO.CD_ITEM = SI.CD_ITEM)
    LEFT JOIN ITEMCONFERENCIAORDEM ICO ON (ICO.CD_EMPRESA = OS.CD_EMPRESA
        AND ICO.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO
        AND ICO.CD_ITEM = SI.CD_ITEM)
    LEFT JOIN VEICULO V ON (V.NR_PLACA = OS.NR_PLACA)
    LEFT JOIN MODELOVEICULO ML ON (ML.CD_MODELOVEICULO = V.CD_MODELOVEICULO
        AND ML.CD_MARCAVEICULO = V.CD_MARCAVEICULO)
    LEFT JOIN MARCAVEICULO MV ON (MV.CD_MARCAVEICULO = V.CD_MARCAVEICULO)
    LEFT JOIN CORVEICULO CV ON (CV.CD_CORVEICULO = V.CD_CORVEICULO)
    LEFT JOIN ITEMREQUISICAOOFICINA IRQ ON (IRQ.CD_EMPRESAOS = OS.CD_EMPRESA
            AND IRQ.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO
            AND IRQ.CD_ITEM = SI.CD_ITEM)
    WHERE OS.ST_ORDEMSERVICO = 'A'
        AND OS.CD_EMPRESA = {empresas}
        AND ICO.NR_ORDEMSERVICO IS NULL
        AND COALESCE(EO.STATUS, 'I') NOT IN ('F')
        AND OS.DT_EMISSAO BETWEEN CURRENT_DATE - 60 AND CURRENT_DATE
        AND IRQ.CD_EMPRESA IS NULL
    GROUP BY
        TIPO_TABLE, STATUS, CD_EMPRESA,
        CD_ITEM, CD_PESSOA, CD_VENDEDOR,
        NR_ORDEMSERVICO, NM_CLIENTE, NM_VENDEDOR, I.CD_FORNECEDOR1,
        SI.CD_ITEM,I.DS_ITEM, QNT, NM_SEPARADOR, ID, I.SG_UNIDMED,
        DS_VEICULO,NM_MECANICO, SI.DT_REGISTRO, M.DS_MARCA
    
    UNION ALL
    
    SELECT
        'O' AS TIPO_TABLE,
        'N' AS STATUS,
        OS.CD_EMPRESA,
        SI.CD_ITEM,
        I.DS_ITEM AS DESCR,
        LIST(DISTINCT LE.DS_LOCAL, ', ') AS LOCALS,
        OS.CD_PESSOA,
        SI.CD_VENDEDOR,
        M.DS_MARCA,
        I.SG_UNIDMED,
        OS.NR_ORDEMSERVICO,
        PC.NM_PESSOA AS NM_CLIENTE,
        PV.NM_PESSOA AS NM_VENDEDOR,
        SI.CD_ITEM || ' - ' || I.DS_ITEM || ' (' || LIST(DISTINCT LE.DS_LOCAL, ', ') || ')' AS DS_ITEM,
        CAST(QT_SOLICITADA - QT_PEDIDA_E AS NUMERIC(15, 2)) AS QNT,
        '' AS NM_SEPARADOR,
        MAX(COALESCE(EO.ID, 0)) + 1 ID,
        I.CD_FORNECEDOR1,
        COALESCE(MV.DS_MARCAVEICULO, '')||'-'||COALESCE(ML.DS_MODELOVEICULO, '')||'-'||COALESCE(V.NR_ANO, '')
            ||'-'||COALESCE(CV.DS_CORVEICULO, '') DS_VEICULO,
        PM.NM_PESSOA NM_MECANICO, SI.DT_REGISTRO
    FROM ORDEMSERVICO OS
    INNER JOIN SERVICOITEM SI 
        ON SI.CD_EMPRESA = OS.CD_EMPRESA 
        AND SI.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO
    INNER JOIN PESSOA PC ON (PC.CD_PESSOA = OS.CD_PESSOA)
    INNER JOIN PESSOA PV ON (PV.CD_PESSOA = SI.CD_VENDEDOR)
    INNER JOIN PESSOA PM ON (PM.CD_PESSOA = SI.CD_MECANICO)
    INNER JOIN ITEM I ON I.CD_ITEM = SI.CD_ITEM
    INNER JOIN MARCA M ON (M.CD_MARCA = I.CD_MARCA)
    INNER JOIN ITEMEMPRESA IL
        ON (IL.CD_ITEM = I.CD_ITEM
        AND IL.CD_EMPRESA = {empresas})
    INNER JOIN LOCALESTOQUE LE 
        ON LE.CD_TIPOLOCAL = IL.CD_TIPOLOCAL
        AND LE.CD_LOCAL = IL.CD_LOCAL
    LEFT JOIN EXTEND_ORDERMSERVICO EO 
        ON (EO.CD_EMPRESA = SI.CD_EMPRESA
        AND EO.NR_ORDERMSERVICO = SI.NR_ORDEMSERVICO 
        AND EO.CD_ITEM = SI.CD_ITEM )
    LEFT JOIN ITEMCONFERENCIAORDEM ICO 
        ON (ICO.CD_EMPRESA = OS.CD_EMPRESA
        AND ICO.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO 
        AND ICO.CD_ITEM = SI.CD_ITEM)
    LEFT JOIN MODELOVEICULO ML ON (ML.CD_MODELOVEICULO = OS.CD_MODELOVEICULO
        AND ML.CD_MARCAVEICULO = OS.CD_MARCAVEICULO)
    LEFT JOIN VEICULO V ON (V.NR_PLACA = OS.NR_PLACA)
    LEFT JOIN MARCAVEICULO MV ON (MV.CD_MARCAVEICULO = V.CD_MARCAVEICULO)
    LEFT JOIN CORVEICULO CV ON (CV.CD_CORVEICULO = V.CD_CORVEICULO)
    LEFT JOIN ITEMREQUISICAOOFICINA IRQ 
        ON IRQ.CD_EMPRESAOS = OS.CD_EMPRESA 
        AND IRQ.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO 
        AND IRQ.CD_ITEM = SI.CD_ITEM
    INNER JOIN SERVICOCALCULADO SC
        ON SC.CD_EMPRESA = SI.CD_EMPRESA
        AND SC.NR_ORDEMSERVICO = SI.NR_ORDEMSERVICO 
        AND SC.CD_ITEM = SI.CD_ITEM
    WHERE OS.ST_ORDEMSERVICO = 'A'
        AND OS.CD_EMPRESA = {empresas}
        AND COALESCE(EO.STATUS, 'N') IN ('I', 'F')
        AND OS.DT_EMISSAO >= CURRENT_DATE - 60
        AND IRQ.CD_EMPRESA IS NULL
    GROUP BY
        TIPO_TABLE, STATUS, CD_EMPRESA, CD_ITEM, DESCR,
        CD_PESSOA, CD_VENDEDOR, SG_UNIDMED,
        NR_ORDEMSERVICO, NM_CLIENTE, NM_VENDEDOR, QNT,
        DS_VEICULO, NM_MECANICO, SI.DT_REGISTRO,M.DS_MARCA,
        NM_SEPARADOR, CD_FORNECEDOR1, SC.QT_SOLICITADA, SC.QT_PEDIDA_E
    HAVING SC.QT_SOLICITADA <> SC.QT_PEDIDA_E
    PLAN SORT (HASH (JOIN (JOIN (JOIN (JOIN (JOIN (JOIN (JOIN (JOIN (HASH (JOIN
    (OS INDEX (ORDEMSERVICO_IDX40, ORDEMSERVICO_IDX5), PC INDEX (PK_PESSOA), SI INDEX (RSERVICOITEM_ORDEMSERVICO),
    PV INDEX (PK_PESSOA), PM INDEX (PK_PESSOA), I INDEX (PK_ITEM)), M NATURAL), IL INDEX (PK_ITEMEMPRESA),
    LE INDEX (PK_LOCALESTOQUE)), EO INDEX (EXTEND_ORDERMSERVICO_IDX1)), ICO INDEX (PK_ITEMCONFERENCIAORDEM)),
    ML INDEX (PK_MODELOVEICULO)), V INDEX (PK_VEICULO)), MV INDEX (PK_MARCAVEICULO)), CV INDEX (PK_CORVEICULO)),
    IRQ INDEX (IDX001_ITEMREQUISICAOOFICINA))))

    )Y
    ORDER BY Y.NR_ORDEMSERVICO, Y.CD_ITEM
    """

    # A ordem dos parâmetros corresponde à ordem de aparição dos `?` no SQL
    resultado = db.execute_query(_query, params=[])
    return resultado


def inserir_orcamento(cd_empresa: int, nr_orcamento: int, cd_item: int, separador: str, id: int):
    """
    Insere um item no orçamento (EXTEND_ORDEMSERVICO) com status 'I' (Inserido).

    :param cd_empresa: Código da empresa
    :param nr_orcamento: Número do orçamento (ordem de serviço)
    :param cd_item: Código do item
    :param separador: Nome do separador
    :param id: Identificador interno
    """
    query = f"""
        EXECUTE PROCEDURE EXTEND_ORDEMSERVICO(
            {cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'I', {id}
        )
    """
    db.execute_udi(query=query, params={
        "empresa": cd_empresa,
        "orcamento": nr_orcamento,
        "item": cd_item,
        "separador": separador,
        "id": id
    })


def cancelar_orcamento(cd_empresa: int, nr_orcamento: int, cd_item: int, separador: str, id: int):
    """
    Cancela um item do orçamento (EXTEND_ORDEMSERVICO) com status 'C' (Cancelado).

    :param cd_empresa: Código da empresa
    :param nr_orcamento: Número do orçamento (ordem de serviço)
    :param cd_item: Código do item
    :param separador: Nome do separador
    :param id: Identificador interno
    """
    query = f"""
        EXECUTE PROCEDURE EXTEND_ORDEMSERVICO(
            {cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'C', {id}
        )
    """
    db.execute_udi(query=query, params={
        "empresa": cd_empresa,
        "orcamento": nr_orcamento,
        "item": cd_item,
        "separador": separador,
        "id": id
    })


def finalizar_orcamento(cd_empresa: int, nr_orcamento: int, cd_item: int, separador: str, id: int):
    """
    Finaliza um item do orçamento (EXTEND_ORDEMSERVICO) com status 'F' (Finalizado).

    :param cd_empresa: Código da empresa
    :param nr_orcamento: Número do orçamento (ordem de serviço)
    :param cd_item: Código do item
    :param separador: Nome do separador
    :param id: Identificador interno
    """
    query = f"""
        EXECUTE PROCEDURE EXTEND_ORDEMSERVICO(
            {cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'F', {id}
        )
    """
    db.execute_udi(query=query, params={
        "empresa": cd_empresa,
        "orcamento": nr_orcamento,
        "item": cd_item,
        "separador": separador,
        "id": id
    })
