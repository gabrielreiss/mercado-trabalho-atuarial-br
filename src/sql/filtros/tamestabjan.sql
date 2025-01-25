SELECT 
    DISTINCT Descrição AS coluna

FROM CAGEDMOV AS T1

left join tamestabjan AS T2 ON T1.tamestabjan = T2.Código
;


