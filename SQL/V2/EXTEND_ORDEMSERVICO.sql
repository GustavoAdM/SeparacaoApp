SET TERM ^ ;

CREATE OR ALTER PROCEDURE EXTEND_ORDEMSERVICO (
    I_CD_EMPRESA DOM_INTEGER,
    I_NR_ORCAMENTO DOM_INTEGER,
    I_CD_ITEM DOM_INTEGER,
    I_NM_SEPARADOR DOM_VARCHAR120,
    I_TP_OPERACAO DOM_CHAR1,
    I_ID DOM_INTEGER = 0)
AS
DECLARE VARIABLE V_CD_CLIENTE INTEGER;
DECLARE VARIABLE V_CD_VENDEDOR INTEGER;
DECLARE VARIABLE V_CD_ITEM INTEGER;
DECLARE VARIABLE V_DS_ITEM DOM_VARCHAR100;
DECLARE VARIABLE V_PS_SERVICOITEM DOM_NUMERIC15_3;
DECLARE VARIABLE V_QT_SERVICOITEM DOM_NUMERIC15_3;
DECLARE VARIABLE V_ID INTEGER;
BEGIN
    SELECT FIRST 1
        IIF(:I_TP_OPERACAO IN ('C', 'F'), MAX(EO.ID), COALESCE(MAX(EO.ID), 0) + 1) ID,
        IT.CD_ITEM, I.DS_ITEM,
        IT.PS_SERVICOITEM - SUM(COALESCE(EO.PS_PEDIDO, 0)) PS_PEDIDO,
        IT.QT_SERVICOITEM - SUM(COALESCE(EO.QT_PEDIDA, 0)) QT_PEDIDA,
        IT.CD_VENDEDOR, OS.CD_PESSOA
    FROM ORDEMSERVICO OS
    INNER JOIN SERVICOITEM IT ON (IT.CD_EMPRESA = OS.CD_EMPRESA
        AND IT.NR_ORDEMSERVICO = OS.NR_ORDEMSERVICO)
    INNER JOIN ITEM I ON (I.CD_ITEM = IT.CD_ITEM)
    LEFT JOIN EXTEND_ORDERMSERVICO EO ON (EO.CD_EMPRESA = IT.CD_EMPRESA
        AND EO.NR_ORDERMSERVICO = IT.NR_ORDEMSERVICO
        AND EO.CD_ITEM = IT.CD_ITEM)
    WHERE OS.CD_EMPRESA = :I_CD_EMPRESA
        AND OS.NR_ORDEMSERVICO = :I_NR_ORCAMENTO
        AND IT.CD_ITEM = :I_CD_ITEM
    GROUP BY IT.CD_ITEM, I.DS_ITEM, IT.CD_VENDEDOR, OS.CD_PESSOA, IT.PS_SERVICOITEM, IT.QT_SERVICOITEM
    INTO :V_ID, :V_CD_ITEM, :V_DS_ITEM, :V_PS_SERVICOITEM, :V_QT_SERVICOITEM, :V_CD_VENDEDOR, :V_CD_CLIENTE;

    /*INSERIR O REGISTRO NA TABELA*/
    IF (:I_TP_OPERACAO = 'I') THEN
    BEGIN
       INSERT INTO EXTEND_ORDERMSERVICO (ID,CD_EMPRESA, NR_ORDERMSERVICO, CD_ITEM, DS_ITEM, CD_VENDEDOR, CD_CLIENTE, QT_PEDIDA, PS_PEDIDO, NM_SEPARADOR, STATUS, DT_INICIO, DT_FIM)
       VALUES (:I_ID, :I_CD_EMPRESA, :I_NR_ORCAMENTO, :V_CD_ITEM, :V_DS_ITEM, :V_CD_VENDEDOR, :V_CD_CLIENTE, :V_QT_SERVICOITEM, :V_PS_SERVICOITEM, :I_NM_SEPARADOR, 'I', CURRENT_TIMESTAMP, NULL);
    END

    /*VALIDA SE O REGISTRO EXISTE NA TABELA*/
    IF (:I_ID <> 0 AND :I_ID IS NOT NULL) THEN
    BEGIN
        /*FINALIZAR - ATUALIZA O REGISTRO PARA FINALIZADO*/
        IF (:I_TP_OPERACAO = 'F') THEN
        BEGIN
           UPDATE EXTEND_ORDERMSERVICO E
           SET E.STATUS = 'F',
               E.DT_FIM = CURRENT_TIMESTAMP
           WHERE E.CD_EMPRESA = :I_CD_EMPRESA
             AND E.NR_ORDERMSERVICO = :I_NR_ORCAMENTO
             AND E.CD_ITEM = :V_CD_ITEM
             AND E.ID = :I_ID;
        END
    
        /*CANCELAR - DELETA DA TABELA PARA QUE POSSA SER INICIADO NOVAMENTE*/
        IF (:I_TP_OPERACAO = 'C') THEN
        BEGIN
           DELETE FROM EXTEND_ORDERMSERVICO E
           WHERE E.CD_EMPRESA = :I_CD_EMPRESA
             AND E.NR_ORDERMSERVICO = :I_NR_ORCAMENTO
             AND E.CD_ITEM = :V_CD_ITEM
             AND E.ID = :I_ID;
        END
    END
END^

SET TERM ; ^

COMMENT ON PARAMETER EXTEND_ORDEMSERVICO.I_TP_OPERACAO IS
'I = INSERIR, F = FINALIZAR, C = CANCELAR';

/* Following GRANT statements are generated automatically */

GRANT SELECT ON ORDEMSERVICO TO PROCEDURE EXTEND_ORDEMSERVICO;
GRANT SELECT ON SERVICOITEM TO PROCEDURE EXTEND_ORDEMSERVICO;
GRANT SELECT ON ITEM TO PROCEDURE EXTEND_ORDEMSERVICO;
GRANT SELECT,INSERT,DELETE,UPDATE ON EXTEND_ORDERMSERVICO TO PROCEDURE EXTEND_ORDEMSERVICO;

/* Existing privileges on this procedure */

GRANT EXECUTE ON PROCEDURE EXTEND_ORDEMSERVICO TO SYSDBA;