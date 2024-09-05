CREATE TABLE itens (
    id SERIAL PRIMARY KEY,         -- ID único para cada item, gerado automaticamente
    nome VARCHAR(255) NOT NULL,    -- Nome do item, obrigatório
    valor DECIMAL(10, 2) NOT NULL, -- Valor unitário do item, obrigatório, com duas casas decimais
    quantidade INT NOT NULL        -- Quantidade em estoque, obrigatório
);
