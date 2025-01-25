SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join raçacor AS T2 ON T1.raçacor = T2.Código
;