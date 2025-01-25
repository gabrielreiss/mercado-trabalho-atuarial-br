SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join graudeinstrução AS T2 ON T1.graudeinstrução = T2.Código
;