SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join sexo AS T2
ON T1.sexo = T2.Código
;