CREATE TABLE aluno (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200),
    email VARCHAR(255) UNIQUE,
    cpf VARCHAR(14) UNIQUE,
    data_ingresso DATE
);

CREATE TABLE curso (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200),
    carga_horaria INT,
    valor_inscricao NUMERIC(10,2),
    status VARCHAR(10)
);

CREATE TABLE matricula (
    id SERIAL PRIMARY KEY,
    aluno_id INT REFERENCES aluno(id),
    curso_id INT REFERENCES curso(id),
    valor NUMERIC(10,2),
    data DATE,
    status_pagamento VARCHAR(10),
    UNIQUE (aluno_id, curso_id)
);

