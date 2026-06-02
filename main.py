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

# comando_sql = "DROP TABLE IF EXISTS sqlite_sequence"
# cursor.execute(comando_sql)

conexao.commit()
cursor.close()
conexao.close()