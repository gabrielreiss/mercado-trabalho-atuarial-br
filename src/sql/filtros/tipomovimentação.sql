SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join tipomovimentação AS T2 ON T1.tipomovimentação = T2.Código
;