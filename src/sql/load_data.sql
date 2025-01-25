SELECT 
    T1.competênciamov AS 'competencia',
    T2.Descrição AS 'regiao',
    T3.Descrição AS 'uf',
    T4.Descrição AS 'municipio',
    T5.Descrição AS 'seção',
    T6.Descrição AS 'subclasse',
    T7.Descrição AS 'categoria',
    T9.Descrição AS 'graudeinstrução',
    T10.Descrição AS 'raçacor',
    T11.Descrição AS 'sexo',
    T1.idade AS 'idade',
    T14.Descrição AS 'tipomovimentacao',
    T18.Descrição AS 'tamanho',
    T23.Descrição AS 'unidadesalarariocodigo',
    T1.salário AS 'salario',
    T1.horascontratuais AS 'horascontratuais',
    T1.saldomovimentação AS 'saldomovimentação'

FROM CAGEDMOV AS T1

LEFT JOIN região AS T2                  ON T1.região = T2.Código
LEFT JOIN uf AS T3                      ON T1.uf = T3.Código
LEFT JOIN município AS T4               ON T1.município = T4.Código
LEFT JOIN seção AS T5                   ON T1.seção = T5.Código
LEFT JOIN subclasse AS T6               ON T1.subclasse = T6.Código
LEFT JOIN categoria AS T7               ON T1.categoria = T7.Código
LEFT JOIN graudeinstrução AS T9         ON T1.graudeinstrução = T9.Código
LEFT JOIN raçacor AS T10                ON T1.raçacor = T10.Código
LEFT JOIN sexo AS T11                   ON T1.sexo = T11.Código
LEFT JOIN tipomovimentação AS T14       ON T1.tipomovimentação = T14.Código
LEFT JOIN tamestabjan AS T18            ON T1.tamestabjan = T18.Código
LEFT JOIN unidadesaláriocódigo AS T23   ON T1.unidadesaláriocódigo = T23.Código;