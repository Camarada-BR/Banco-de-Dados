from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkinter import font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import squarify

janelaP = Tk()

fonte_titulo = font.Font(
    family="Arial",
    size=12,
    weight="bold"
)

class Funcs():
    def conect_bd(self):
        self.conn = sqlite3.connect("banco.db")
        self.cursor = self.conn.cursor()

    def desconect_bd(self):
        self.conn.close()

    def map_produtos(self):
        grafico_produtos = Toplevel()
        grafico_produtos.title("Gráfico de Produtos")

        self.cursor.execute("""
            SELECT
                Numero_Nota_Fiscal,
                Quantidade_Produto
            FROM ITEM_NOTA_FISCAL
            ORDER BY Numero_Nota_Fiscal, Codigo_Produto
        """)

        self.cursor.execute("""
            SELECT 
                inf.Numero_Nota_Fiscal,
                p.Nome_Produto,
                inf.Quantidade_Produto
            FROM ITEM_NOTA_FISCAL inf
            JOIN PRODUTO p
                ON inf.Codigo_Produto = p.Codigo_Produto
            ORDER BY inf.Numero_Nota_Fiscal
        """)

        resultado = self.cursor.fetchall()
        dados = {}

        for nota, nome_produto, quantidade in resultado:
            chave = f"NF {nota}"

            if chave not in dados:
                dados[chave] = []

            dados[chave].append((nome_produto, quantidade))

        total_barras = sum(len(produtos) for produtos in dados.values())

        fig, (ax1, ax2) = plt.subplots(
            1, 2,
            figsize=(16, 6),
            gridspec_kw={"width_ratios": [1, 2]}
        )
        fig.tight_layout(rect=[0.10, 0.10, 0.95, 0.95])
        fig.subplots_adjust(wspace=0.5)

        espaco_grupo = 2
        largura = 0.4

        labels_usadas = set()

        cores = plt.cm.tab20.colors
        mapa_cores = {}
        indice_cor = 0

        for i, (nota, produtos) in enumerate(dados.items()):
            n = len(produtos)

            for j, (nome, quantidade) in enumerate(produtos):

                if nome not in mapa_cores:
                    mapa_cores[nome] = cores[indice_cor % len(cores)]
                    indice_cor += 1

                cor = mapa_cores[nome]
                pos = (i * espaco_grupo) + (j - (n - 1) / 2) * largura

                label = nome if nome not in labels_usadas else ""
                barra = ax1.bar(pos, quantidade, largura, label=label, color=cor)
                labels_usadas.add(nome)
                ax1.bar_label(barra, padding=3)

        ax1.set_xticks([i * espaco_grupo for i in range(len(dados))])
        ax1.set_xticklabels(dados.keys())

        ax1.set_ylabel('Quantidade de Produtos')
        ax1.set_xlabel('Notas Fiscais')
        ax1.set_title('Distribuição de Produtos por Nota Fiscal')
        ax1.legend(    
            title="Produtos",
            bbox_to_anchor=(1.02, 1),
            loc="upper left"
        )
        ax1.set_ylim(0, 30)

        self.cursor.execute("""
            SELECT 
                p.Nome_Produto,
                SUM(inf.Quantidade_Produto)
            FROM ITEM_NOTA_FISCAL inf
            JOIN PRODUTO p
                ON inf.Codigo_Produto = p.Codigo_Produto
            GROUP BY p.Nome_Produto
            ORDER BY SUM(inf.Quantidade_Produto) DESC
        """)

        ranking = self.cursor.fetchall()

        nomes = []
        quantidades = []

        for nome, total in ranking:
            nomes.append(nome)
            quantidades.append(total)

        barras_top = ax2.bar(nomes, quantidades)

        ax2.tick_params(axis="x", labelrotation=45)
        plt.setp(ax2.get_xticklabels(), ha="right")
        fig.subplots_adjust(bottom=0.25)
        ax2.bar_label(barras_top, padding=3)

        ax2.set_ylabel("Quantidade Total")
        ax2.set_xlabel("Produtos")
        ax2.set_title("Top Produtos Mais Vendidos")
        ax2.set_ylim(0, 30)

        canvas = FigureCanvasTkAgg(fig, master=grafico_produtos)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def map_desempenho(self):
        grafico_desempenho = Toplevel()
        grafico_desempenho.title("Gráfico de Desempenho Regional")

        self.cursor.execute("""
            SELECT 
                R.Nome_Regiao,
                COUNT(NF.Numero_Nota_Fiscal) AS Total_Notas
            FROM REGIAO R
            JOIN VENDEDOR V 
                ON R.Codigo_Regiao = V.Codigo_Regiao
            JOIN NOTA_FISCAL NF 
                ON V.Codigo_Vendedor = NF.Codigo_Vendedor
            GROUP BY R.Nome_Regiao
        """)

        resultado = self.cursor.fetchall()

        regioes = [row[0] for row in resultado]
        quantidades = [row[1] for row in resultado]

        labels = [
            f"{regioes[i]}\n{quantidades[i]} Nota Fiscai"
            for i in range(len(regioes))
        ]

        # cria a figura
        fig, ax = plt.subplots(figsize=(10, 6))

        # desenha o treemap
        squarify.plot(
            sizes=quantidades,
            label=labels,
            alpha=0.8,
            ax=ax
        )

        ax.set_title("Desempenho Regional: Quantidade de Notas Fiscais")
        ax.axis("off")

        # coloca no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=grafico_desempenho)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def carregar_tabela(self, titulo, consulta, parametros=None):
        # apaga só a tabela antiga
        self.tabela.destroy()

        # executa consulta
        if parametros is not None:
            self.cursor.execute(consulta, parametros)
        else:
            self.cursor.execute(consulta)

        resultado = self.cursor.fetchall()
        print("Resultado:", resultado)
        colunas = [desc[0] for desc in self.cursor.description]

        # recria a tabela dentro do mesmo frame
        self.tabela = ttk.Treeview(
            self.frame_tabela,
            columns=colunas,
            show="headings"
        )

        self.tabela.tag_configure("par", background="#f8f8f8")
        self.tabela.tag_configure("impar", background="#ffffff")

        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=150, anchor="center")

        for i, linha in enumerate(resultado):
            tag = "par" if i % 2 == 0 else "impar"
            self.tabela.insert("", "end", values=linha, tags=(tag,))

        self.tabela.pack(side="left", fill="both", expand=True)

    def mostrar_produtos_ativos(self):
        self.carregar_tabela(
            "Catálogo Ativo",
            """
            SELECT
                Codigo_Produto,
                Nome_Produto,
                CASE 
                    WHEN Produto_Ativo = 1 THEN 'Ativo'
                    ELSE 'Inativo'
                END AS Status
            FROM PRODUTO
            WHERE Produto_Ativo = 1
            ORDER BY Codigo_Produto
            """
        )

    def mostrar_historico_cliente(self):
        nome_cliente = self.entry_nome.get()

        consulta_sql = """
        SELECT DISTINCT
            NF.Codigo_Vendedor AS [Código do Vendedor]
        FROM NOTA_FISCAL NF
        INNER JOIN CLIENTE C
            ON NF.Codigo_Cliente = C.Codigo_Cliente
        WHERE C.Nome_Cliente LIKE ?
        ORDER BY NF.Codigo_Vendedor
        """

        self.carregar_tabela(
            "Histórico do Cliente",
            consulta_sql,
            (f"%{nome_cliente}%",)
        )

    def mostrar_frota(self):
        self.carregar_tabela(
            "Inventário de Frota",
            """
            SELECT 
                Codigo_Veiculo,
                Numero_Placa_Veiculo
            FROM VEICULO
            ORDER BY Codigo_Veiculo
            """
        )
class Aplicação(Funcs):
    def __init__(self):
        self.janelaP = janelaP
        self.tela()
        self.conect_bd()
        self.frames_da_tela()
        self.w_informações1()
        janelaP.mainloop()
    def tela(self):
        self.janelaP.title("esquema FCG")
        self.janelaP.configure(background='#1c2b3c')
        self.janelaP.state("zoomed")
        #self.janelaP.resizable(False, False)
    def frames_da_tela(self):
        width = 0.5
        height = 0.8
        self.frame_1 = Frame(self.janelaP, background='#ebeff0', highlightbackground= '#4b5c6c', highlightthickness=6 )
        self.frame_1.place(
            relx=0.5,
            rely=0.5,
            relwidth=width,
            relheight=height,
            anchor="center"
        )

    def w_informações1(self):
        #Configuração do grid para os botões.
        #Adiciona um frame para os botões e o posiciona na parte superior do frame principal.
        self.frame_botoes = Frame(self.frame_1, background='#ebeff0')
        self.frame_botoes.place(relx=0.5, rely=0.05,relwidth=0.8, anchor="n")

        for i in range(5):
            self.frame_botoes.grid_columnconfigure(i, weight=1)
        #_________________________________________________________________

        self.entry_nome = Entry(self.frame_botoes)
        self.entry_nome.grid(row=0, column=0, padx=5)

        self.bt_clientes = Button(self.frame_botoes, text="Historico de Clientes", command=self.mostrar_historico_cliente)
        self.bt_clientes.grid(row=0, column=0, padx=5, sticky="ew")

        self.bt_produtos = Button(self.frame_botoes, text="Produtos Ativos", command=self.mostrar_produtos_ativos)
        self.bt_produtos.grid(row=0, column=1, padx=5, sticky="ew")

        self.bt_frota = Button(self.frame_botoes, text="Frota de Veículos", command=self.mostrar_frota)
        self.bt_frota.grid(row=0, column=2, padx=5, sticky="ew")

        self.top_produtos = Button(self.frame_botoes, text="top produtos", command=self.map_produtos)
        self.top_produtos.grid(row=0, column=3, padx=5, sticky="ew")

        self.dp_regiao = Button(self.frame_botoes, text="Desempenho Regional", command=self.map_desempenho)
        self.dp_regiao.grid(row=0, column=4, padx=5, sticky="ew")

        #--------------------------------------------

        self.frame_tabela = Frame(self.frame_1, background='#ebeff0')
        self.frame_tabela.place(
            relx=0.5,
            rely=0.15,
            relwidth=0.8,
            relheight=0.7,
            anchor="n"
        )

        style = ttk.Style()

        style.configure(
            "Treeview",
            borderwidth=1,
            relief="solid"
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 11, "bold"),
            relief="raised"
        )

        style.map(
            "Treeview",
            background=[("selected", "#347083")],
            foreground=[("selected", "white")]
        )

        self.tabela = ttk.Treeview(
            self.frame_tabela,
            show="headings"
        )

        self.tabela.tag_configure("par", background="#f8f8f8")
        self.tabela.tag_configure("impar", background="#ffffff")

        self.tabela.pack(side="left", fill="both", expand=True)

Aplicação()