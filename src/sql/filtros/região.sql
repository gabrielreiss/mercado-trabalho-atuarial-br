SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join região AS T2
ON T1.região = T2.Código
;