from .Connection import db

def pedidos_nao_separados(empresa:str = '50'):
    _querie = f"""
    SELECT
        E.TIPO_TABLE, E.STATUS, E.CD_EMPRESA, E.NIVEL,
        E.NR_PEDIDO, E.NM_PESSOA, E.NM_VENDEDOR,
        E.DT_PEDIDO, E.HR_PEDIDO, E.SEPARADOR
    FROM EXTEND_PEDIDO_SEPARACAO({empresa}) E
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
    SELECT  
        E.TIPO_TABLE, E.STATUS, E.CD_EMPRESA, E.CD_ITEM, E.DESCR, 
        E.LOCALS, E.CD_PESSOA, E.CD_VENDEDOR,
        E.SG_UNIDMED, E.DS_MARCA, E.NR_ORDEMSERVICO, E.NM_CLIENTE, 
        E.NM_VENDEDOR, E.DS_ITEM, E.QNT, E.NM_SEPARADOR, E.ID,
        COALESCE(E.CD_FORNECEDOR1, ' ') CD_FORNECEDOR1
    FROM EXTEND_ORDEMSERVICO_SEPARACAO({cd_empresa}) E
    
    """
    return db.execute_queries(query=_querie)


def inserir_orcamento(cd_empresa, nr_orcamento, cd_item, separador, id):
    _querie = f"""EXECUTE PROCEDURE EXTEND_ORDEMSERVICO({cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'I', {id})"""
    db.execute_UDI(query=_querie)

def cacelar_orcamento(cd_empresa, nr_orcamento, cd_item, separador, id):
    _querie = f"""EXECUTE PROCEDURE EXTEND_ORDEMSERVICO({cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'C', {id})"""
    db.execute_UDI(query=_querie)

def finalizar_orcamento(cd_empresa, nr_orcamento, cd_item, separador, id):
    _querie = f"""EXECUTE PROCEDURE EXTEND_ORDEMSERVICO({cd_empresa}, {nr_orcamento}, {cd_item}, '{separador}', 'F', {id})"""
    db.execute_UDI(query=_querie)

