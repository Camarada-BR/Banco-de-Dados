import sqlite3

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()

cursor.execute("PRAGMA foreign_keys = ON")
cursor.executescript("""          
    CREATE TABLE IF NOT EXISTS PRODUTO (
        Codigo_Produto INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Nome_Produto  TEXT NOT NULL,
        Produto_Ativo BOOLEAN NOT NULL
    );
                
    CREATE TABLE IF NOT EXISTS CLIENTE (
        Codigo_Cliente INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Nome_Cliente TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS REGIAO (
        Codigo_Regiao INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Nome_Regiao TEXT NOT NULL
    );
                                    
    CREATE TABLE IF NOT EXISTS VENDEDOR (
        Codigo_Vendedor INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Codigo_Regiao INTEGER NOT NULL,
        FOREIGN KEY (Codigo_Regiao) REFERENCES REGIAO(Codigo_Regiao)
    );
                     
    CREATE TABLE IF NOT EXISTS PONTO_ESTRATEGICO (
        Codigo_Ponto_Estrategico INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Codigo_Regiao INTEGER NOT NULL,
        FOREIGN KEY (Codigo_Regiao) REFERENCES REGIAO(Codigo_Regiao)
    );
                     
    CREATE TABLE IF NOT EXISTS VEICULO (
        Codigo_Veiculo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Numero_Placa_Veiculo TEXT NOT NULL
    );
                     
    CREATE TABLE IF NOT EXISTS UTILIZACAO_VEICULO (
        Data_Utilizacao_Veiculo DATE NOT NULL,
        Codigo_Veiculo INTEGER NOT NULL,
        Codigo_Vendedor INTEGER NOT NULL,
        FOREIGN KEY (Codigo_Veiculo) REFERENCES VEICULO(Codigo_Veiculo),
        FOREIGN KEY (Codigo_Vendedor) REFERENCES VENDEDOR(Codigo_Vendedor)
    );
                     
    CREATE TABLE IF NOT EXISTS NOTA_FISCAL  (
        Numero_Nota_Fiscal INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Codigo_Cliente INTEGER NOT NULL,
        Codigo_Vendedor INTEGER NOT NULL,
        FOREIGN KEY (Codigo_Cliente) REFERENCES CLIENTE(Codigo_Cliente),
        FOREIGN KEY (Codigo_Vendedor) REFERENCES VENDEDOR(Codigo_Vendedor)
    );
                     
    CREATE TABLE IF NOT EXISTS ITEM_NOTA_FISCAL (
        Numero_Nota_Fiscal INTEGER NOT NULL,
        Numero_Item_Nota_Fiscal INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Codigo_Produto INTEGER NOT NULL,
        Quantidade_Produto INTEGER NOT NULL,
        FOREIGN KEY (Numero_Nota_Fiscal) REFERENCES NOTA_FISCAL(Numero_Nota_Fiscal),
        FOREIGN KEY (Codigo_Produto) REFERENCES PRODUTO(Codigo_Produto)
    );
""")

cursor.executescript("""
    -- PRODUTOS (Total: 10)
    INSERT INTO PRODUTO (Nome_Produto, Produto_Ativo) VALUES
    ('Arroz', 1),
    ('Feijao', 1),
    ('Macarrao', 1),
    ('Oleo de Soja', 1),
    ('Açúcar', 1),
    ('Sal', 1),
    ('Café', 1),
    ('Leite', 1),
    ('Farinha de Trigo', 1),
    ('Biscoito', 1);

    -- CLIENTES (Total: 10)
    INSERT INTO CLIENTE (Nome_Cliente) VALUES
    ('Joao Silva'),
    ('Maria Souza'),
    ('Pedro Santos'),
    ('Ana Oliveira'),
    ('Lucas Rodrigues'),
    ('Julia Almeida'),
    ('Carlos Pereira'),
    ('Beatriz Costa'),
    ('Marcos Fernandes'),
    ('Camila Ribeiro');

    -- REGIOES (Total: 10)
    INSERT INTO REGIAO (Nome_Regiao) VALUES
    ('Norte'),
    ('Sul'),
    ('Nordeste'),
    ('Centro-Oeste'),
    ('Sudeste'),
    ('Metropolitana'),
    ('Litoral Norte'),
    ('Litoral Sul'),
    ('Interior Velho'),
    ('Fronteira');

    -- VENDEDORES (Total: 10 - referenciando as regiões de 1 a 10)
    INSERT INTO VENDEDOR (Codigo_Regiao) VALUES
    (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

    -- PONTOS ESTRATEGICOS (Total: 10 - referenciando as regiões de 1 a 10)
    INSERT INTO PONTO_ESTRATEGICO (Codigo_Regiao) VALUES
    (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

    -- VEICULOS (Total: 10)
    INSERT INTO VEICULO (Numero_Placa_Veiculo) VALUES
    ('ABC1D23'),
    ('XYZ9K87'),
    ('KGB2J34'),
    ('MHX4F56'),
    ('NOP7R89'),
    ('QWE1A23'),
    ('ZXC5V67'),
    ('VUT9B88'),
    ('PLM3N21'),
    ('OKI8U76');

    -- UTILIZACAO DE VEICULOS (Total: 10 - relacionando veículos 1-10 e vendedores 1-10)
    INSERT INTO UTILIZACAO_VEICULO (
        Data_Utilizacao_Veiculo,
        Codigo_Veiculo,
        Codigo_Vendedor
    ) VALUES
    ('2026-06-10', 1, 1),
    ('2026-06-11', 2, 2),
    ('2026-06-12', 3, 3),
    ('2026-06-12', 4, 4),
    ('2026-06-13', 5, 5),
    ('2026-06-13', 6, 6),
    ('2026-06-14', 7, 7),
    ('2026-06-14', 8, 8),
    ('2026-06-15', 9, 9),
    ('2026-06-15', 10, 10);

    -- NOTAS FISCAIS (Total: 10 - gerando IDs de nota de 1 a 10)
    INSERT INTO NOTA_FISCAL (
        Codigo_Cliente,
        Codigo_Vendedor
    ) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);

    -- ITENS DAS NOTAS (Total: 10 - distribuídos entre as notas fiscais criadas acima)
    INSERT INTO ITEM_NOTA_FISCAL (
        Numero_Nota_Fiscal,
        Codigo_Produto,
        Quantidade_Produto
    ) VALUES
    (1, 1, 10),
    (1, 2, 5),
    (1, 7, 3),

    (2, 3, 8),
    (2, 8, 12),

    (3, 4, 2),
    (3, 5, 6),
    (3, 1, 9),
    (3, 10, 4),

    (4, 5, 12),

    (5, 6, 1),
    (5, 2, 14),
    (5, 9, 7),
    (5, 3, 11),
    (5, 8, 2);
""")

conexao.commit()
cursor.close()
conexao.close()