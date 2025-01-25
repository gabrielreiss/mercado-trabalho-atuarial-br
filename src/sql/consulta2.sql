SELECT 
    T1.tipomovimentação,
    T23.Descrição,
    count(*)
    --*

FROM CAGEDMOV AS T1

LEFT JOIN região AS T2                  ON T1.região = T2.Código
LEFT JOIN uf AS T3                      ON T1.uf = T3.Código
LEFT JOIN município AS T4               ON T1.município = T4.Código
LEFT JOIN seção AS T5                   ON T1.seção = T5.Código
LEFT JOIN subclasse AS T6               ON T1.subclasse = T6.Código
LEFT JOIN categoria AS T7               ON T1.categoria = T7.Código
LEFT JOIN cbo2002ocupação AS T8         ON T1.cbo2002ocupação = T8.Código
LEFT JOIN graudeinstrução AS T9         ON T1.graudeinstrução = T9.Código
LEFT JOIN raçacor AS T10                ON T1.raçacor = T10.Código
LEFT JOIN sexo AS T11                   ON T1.sexo = T11.Código
LEFT JOIN tipoempregador AS T12         ON T1.tipoempregador = T12.Código
LEFT JOIN tipoestabelecimento AS T13    ON T1.tipoestabelecimento = T13.Código
LEFT JOIN tipomovimentação AS T14       ON T1.tipomovimentação = T14.Código
LEFT JOIN tipodedeficiência AS T15      ON T1.tipodedeficiência = T15.Código
LEFT JOIN indtrabintermitente AS T16    ON T1.indtrabintermitente = T16.Código
LEFT JOIN indtrabparcial AS T17         ON T1.indtrabparcial = T17.Código
LEFT JOIN tamestabjan AS T18            ON T1.tamestabjan = T18.Código
LEFT JOIN indicadoraprendiz AS T19      ON T1.indicadoraprendiz = T19.Código
LEFT JOIN origemdainformação AS T20     ON T1.origemdainformação = T20.Código
LEFT JOIN unidadesaláriocódigo AS T23   ON T1.unidadesaláriocódigo = T23.Código

--where T9.Código IN (3,4,5,6)

group by T1.unidadesaláriocódigo

--order by count(*) DESC

order by T1.unidadesaláriocódigo ASC

;

