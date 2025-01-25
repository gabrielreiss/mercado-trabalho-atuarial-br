SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join seção AS T2
ON T1.seção = T2.Código
;