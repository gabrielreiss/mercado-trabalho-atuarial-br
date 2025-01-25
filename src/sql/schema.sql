CREATE TABLE IF NOT EXISTS "CAGEDMOV" (
        "competênciamov" BIGINT,
        "região" BIGINT,
        uf BIGINT,
        "município" BIGINT,
        "seção" TEXT,
        subclasse BIGINT,
        "saldomovimentação" BIGINT,
        "cbo2002ocupação" BIGINT,
        categoria BIGINT,
        "graudeinstrução" BIGINT,
        idade FLOAT,
        horascontratuais TEXT,
        "raçacor" BIGINT,
        sexo BIGINT,
        tipoempregador BIGINT,
        tipoestabelecimento BIGINT,
        "tipomovimentação" BIGINT,
        "tipodedeficiência" BIGINT,
        indtrabintermitente BIGINT,
        indtrabparcial BIGINT,
        "salário" TEXT,
        tamestabjan BIGINT,
        indicadoraprendiz BIGINT,
        "origemdainformação" BIGINT,
        "competênciadec" BIGINT,
        indicadordeforadoprazo BIGINT,
        "unidadesaláriocódigo" BIGINT,
        "valorsaláriofixo" TEXT
);
CREATE TABLE IF NOT EXISTS "região" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE uf (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "município" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "seção" (
        "Código" TEXT,
        "Descrição" TEXT
);
CREATE TABLE subclasse (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE categoria (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "cbo2002ocupação" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "graudeinstrução" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "raçacor" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE sexo (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE tipoempregador (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE tipoestabelecimento (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "tipomovimentação" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "tipodedeficiência" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE indtrabintermitente (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE indtrabparcial (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE tamestabjan (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE indicadoraprendiz (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "origemdainformação" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE IF NOT EXISTS "indicadordeexclusão" (
        "Código" BIGINT,
        "Descrição" TEXT
);
CREATE TABLE indicadordeforadoprazo (
        "Código" BIGINT,
);
CREATE TABLE IF NOT EXISTS "unidadesaláriocódigo" (
        "Código" BIGINT,
        "Descrição" TEXT
);