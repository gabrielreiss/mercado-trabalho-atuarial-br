SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join categoria AS T2
ON T1.categoria = T2.Código
;