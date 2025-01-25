SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join subclasse AS T2
ON T1.subclasse = T2.Código
;