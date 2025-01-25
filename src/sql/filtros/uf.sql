SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join uf AS T2
ON T1.uf = T2.Código
;