from .Connection import db

def pedidos_nao_separados(empresa:str = '50'):
    _querie = f"""
    WITH PEDIDOS_SEPARACAO
    AS (
        SELECT
            'P' TIPO_TABLE,
            COALESCE(ES.STATUS, 'N') STATUS,
            P.CD_EMPRESA,
            CASE P.CD_TIPOPEDIDO
                WHEN 1 THEN 'BALCÃO'
                WHEN 2 THEN 'MOTOBOY'
                WHEN 3 THEN 'DESPACHE'
                ELSE 'NENHUM'
             END NIVEL ,
            P.NR_PEDIDO,PE.NM_PESSOA, PV.NM_PESSOA NM_VENDEDOR, P.DT_PEDIDO, P.HR_PEDIDO,
            COALESCE(ES.NM_USUARIO, '') SEPARADOR
            
        FROM
            PEDIDO P
            LEFT JOIN ITEMCONFERENCIAPEDIDO ICP ON (ICP.CD_EMPRESA = P.CD_EMPRESA
                AND ICP.NR_PEDIDO = P.NR_PEDIDO
                AND ICP.TP_PEDIDO = P.TP_PEDIDO)
            LEFT JOIN EXTEND_SEPARACAO ES ON (ES.CD_EMPRESA = P.CD_EMPRESA
                AND ES.NR_PEDIDO = P.NR_PEDIDO)
            INNER JOIN PESSOA PE ON (PE.CD_PESSOA = P.CD_PESSOA)
            INNER JOIN PESSOA PV ON (PV.CD_PESSOA = P.CD_VENDEDOR)
        WHERE
            P.TP_PEDIDO = 'S'
            AND P.DT_PEDIDO >= CURRENT_DATE - 10
            AND P.CD_EMPRESA IN ({empresa})
            AND ICP.NR_PEDIDO IS NULL
            AND P.ST_PEDIDO NOT IN ('A', 'P', 'C')
            AND P.CD_TIPOPEDIDO IS NOT NULL
            AND P.NR_ORDEMSERVICO IS NULL
        ORDER BY
            COALESCE(P.CD_TIPOPEDIDO, 4)
    )
    SELECT *
    FROM PEDIDOS_SEPARACAO PE
    WHERE PE.STATUS <> 'F'
    """
    return db.execute_queries(query=_querie)

def inserir_inicio(empresa, pedido, status, usuario):
    _querie = f"""
    INSERT INTO EXTEND_SEPARACAO (CD_EMPRESA, NR_PEDIDO, NM_USUARIO, STATUS, DT_INICIO, DT_FIM)
                      VALUES ({empresa}, {pedido}, '{usuario}', '{status}', CURRENT_TIMESTAMP, NULL);
    """
    db.execute_UDI(query=_querie)

def cancelar(empresa, pedido):
    _querie = f"""
    DELETE FROM extend_separacao E
    WHERE E.cd_empresa = {empresa}
        AND e.nr_pedido = {pedido}
    """
    db.execute_UDI(query=_querie)

def finalizar(empresa, pedido):
    _querie = f"""
    UPDATE EXTEND_SEPARACAO SET 
        STATUS = 'F',
        DT_FIM = CURRENT_TIMESTAMP
    WHERE (CD_EMPRESA = {empresa}) AND
        (NR_PEDIDO = {pedido});
    """
    db.execute_UDI(query=_querie)

def orcamentos_separacao(cd_empresa):
    _querie = f"""
    SELECT *
    FROM (
        SELECT
            'O' TIPO_TABLE,
            COALESCE(EO.STATUS, 'N') STATUS,
            OS.CD_EMPRESA, SI.CD_ITEM, I.DS_ITEM DESCR, LIST(LE.DS_LOCAL, ',') LOCALS,
            OS.CD_PESSOA, SI.CD_VENDEDOR, I.SG_UNIDMED, M.DS_MARCA,
            OS.NR_ORDEMSERVICO, PC.NM_PESSOA NM_CLIENTE,
            PV.NM_PESSOA NM_VENDEDOR,
            SI.CD_ITEM||' - '||I.DS_ITEM||' ('||LIST(LE.DS_LOCAL, ', ')||')' DS_ITEM,
            CAST(COALESCE(EO.PS_PEDIDO, EO.QT_PEDIDA, SI.PS_SERVICOITEM, SI.QT_SERVICOITEM)AS NUMERIC(15, 2)) QNT,
            COALESCE(EO.NM_SEPARADOR, '') NM_SEPARADOR,
            EO.ID
        FROM ORDEMSERVICO OS
        INNER JOIN SERVICOITEM SI ON (SI.CD_EMPRESA = OS.CD_EMPRESA
            AND SI.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO)
        INNER JOIN PESSOA PC ON (PC.CD_PESSOA = OS.CD_PESSOA)
        INNER JOIN PESSOA PV ON (PV.CD_PESSOA = SI.CD_VENDEDOR)
        INNER JOIN ITEM I ON (I.CD_ITEM = SI.CD_ITEM)
        INNER JOIN ITEMLOCAL IL ON (IL.CD_ITEM = I.CD_ITEM
            AND IL.CD_TIPOLOCAL = CASE {cd_empresa}
                                    WHEN 7 THEN 7
                                    WHEN 40 THEN 1
                                    WHEN 50 THEN 2
                                    WHEN 60 THEN 3
                                    END)
        INNER JOIN LOCALESTOQUE LE ON (LE.CD_TIPOLOCAL = IL.CD_TIPOLOCAL
            AND LE.CD_LOCAL = IL.CD_LOCAL)
        LEFT JOIN EXTEND_ORDERMSERVICO EO ON (EO.CD_EMPRESA = SI.CD_EMPRESA
            AND EO.NR_ORDERMSERVICO = SI.NR_ORDEMSERVICO
            AND EO.CD_ITEM = SI.CD_ITEM)
        LEFT JOIN ITEMCONFERENCIAORDEM ICO ON (ICO.CD_EMPRESA = OS.CD_EMPRESA
            AND ICO.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO
            AND ICO.CD_ITEM = SI.CD_ITEM)
        INNER JOIN MARCA M ON (M.CD_MARCA = I.CD_MARCA)
        WHERE OS.ST_ORDEMSERVICO = 'A'
            AND OS.CD_EMPRESA IN ({cd_empresa})
            AND ICO.NR_ORDEMSERVICO IS NULL
            AND COALESCE(EO.STATUS, 'I') NOT IN ('F')
            AND OS.DT_EMISSAO >= CURRENT_DATE - 30
        GROUP BY
            TIPO_TABLE, STATUS, CD_EMPRESA,
            CD_ITEM, CD_PESSOA, CD_VENDEDOR,
            NR_ORDEMSERVICO, NM_CLIENTE, NM_VENDEDOR,
            SI.CD_ITEM,I.DS_ITEM, QNT, NM_SEPARADOR, ID, M.DS_MARCA, I.SG_UNIDMED
        
        UNION ALL
        
        SELECT *
        FROM (
            SELECT
                'O' TIPO_TABLE,
                'P' STATUS,
                OS.CD_EMPRESA, SI.CD_ITEM, I.DS_ITEM DESCR, LIST(LE.DS_LOCAL, ',') LOCALS,
                OS.CD_PESSOA, SI.CD_VENDEDOR, I.SG_UNIDMED, M.DS_MARCA,
                OS.NR_ORDEMSERVICO, PC.NM_PESSOA NM_CLIENTE,
                PV.NM_PESSOA NM_VENDEDOR,
                SI.CD_ITEM||' - '||I.DS_ITEM||' ('||LIST(LE.DS_LOCAL, ', ')||')' DS_ITEM,
                CAST(SUM(COALESCE(SI.PS_SERVICOITEM, SI.QT_SERVICOITEM)) - SUM(COALESCE(EO.PS_PEDIDO, EO.QT_PEDIDA)) AS NUMERIC(15,2)) QNT,
                '' NM_SEPARADOR,
                EO.ID
            FROM ORDEMSERVICO OS
            INNER JOIN SERVICOITEM SI ON (SI.CD_EMPRESA = OS.CD_EMPRESA
                AND SI.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO)
            INNER JOIN PESSOA PC ON (PC.CD_PESSOA = OS.CD_PESSOA)
            INNER JOIN PESSOA PV ON (PV.CD_PESSOA = SI.CD_VENDEDOR)
            INNER JOIN ITEM I ON (I.CD_ITEM = SI.CD_ITEM)
            INNER JOIN ITEMLOCAL IL ON (IL.CD_ITEM = I.CD_ITEM
                AND IL.CD_TIPOLOCAL = CASE {cd_empresa}
                                        WHEN 7 THEN 7
                                        WHEN 40 THEN 1
                                        WHEN 50 THEN 2
                                        WHEN 60 THEN 3
                                      END)
            INNER JOIN LOCALESTOQUE LE ON (LE.CD_TIPOLOCAL = IL.CD_TIPOLOCAL
                AND LE.CD_LOCAL = IL.CD_LOCAL)
            LEFT JOIN EXTEND_ORDERMSERVICO EO ON (EO.CD_EMPRESA = SI.CD_EMPRESA
                AND EO.NR_ORDERMSERVICO = SI.NR_ORDEMSERVICO
                AND EO.CD_ITEM = SI.CD_ITEM)
            LEFT JOIN ITEMCONFERENCIAORDEM ICO ON (ICO.CD_EMPRESA = OS.CD_EMPRESA
                AND ICO.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO
                AND ICO.CD_ITEM = SI.CD_ITEM)
            INNER JOIN MARCA M ON (M.CD_MARCA = I.CD_MARCA)
            WHERE OS.ST_ORDEMSERVICO = 'A' 
                AND OS.CD_EMPRESA IN ({cd_empresa})
                AND ICO.NR_ORDEMSERVICO IS NULL
                AND OS.DT_EMISSAO >= CURRENT_DATE - 30
            GROUP BY
                TIPO_TABLE, STATUS, OS.CD_EMPRESA, SI.CD_ITEM,
                OS.CD_PESSOA, SI.CD_VENDEDOR, OS.NR_ORDEMSERVICO,
                NM_CLIENTE, NM_VENDEDOR, SI.CD_ITEM, I.DS_ITEM,
                NM_SEPARADOR, EO.ID, M.DS_MARCA, I.SG_UNIDMED
            )X
        WHERE X.QNT > 0
    )Y
    ORDER BY Y.CD_EMPRESA, Y.NR_ORDEMSERVICO
    
    """
    return db.execute_queries(query=_querie)


def inserir_orcamento(cd_empresa, nr_orcamento, cd_item, separador):
    _querie = f"""EXECUTE PROCEDURE EXTEND_ORDEMSERVICO({cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'I')"""
    db.execute_UDI(query=_querie)

def cacelar_orcamento(cd_empresa, nr_orcamento, cd_item, separador):
    _querie = f"""EXECUTE PROCEDURE EXTEND_ORDEMSERVICO({cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'C')"""
    db.execute_UDI(query=_querie)

def finalizar_orcamento(cd_empresa, nr_orcamento, cd_item, separador):
    _querie = f"""EXECUTE PROCEDURE EXTEND_ORDEMSERVICO({cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'F')"""
    db.execute_UDI(query=_querie)

