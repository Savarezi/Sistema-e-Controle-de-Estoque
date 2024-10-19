# Importando tkinter para criar a interface gráfica
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Funções do banco de dados (as mesmas usadas antes)
def connect_db():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL
    )
    ''')
    conn.commit()
    return conn

def close_db(conn):
    conn.close()

def adicionar_produto(nome, quantidade, preco):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)', (nome, quantidade, preco))
    conn.commit()
    close_db(conn)

def listar_produtos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    close_db(conn)
    return produtos

def atualizar_produto(id_produto, nome, quantidade, preco):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?', (nome, quantidade, preco, id_produto))
    conn.commit()
    close_db(conn)

def remover_produto(id_produto):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id_produto,))
    conn.commit()
    close_db(conn)

# Função para exibir os produtos na interface
def exibir_produtos():
    produtos = listar_produtos()
    texto_produtos.delete(1.0, tk.END)  # Limpa o texto anterior
    if produtos:
        for produto in produtos:
            texto_produtos.insert(tk.END, f"ID: {produto[0]} | Nome: {produto[1]} | Quantidade: {produto[2]} | Preço: R${produto[3]:.2f}\n")
    else:
        texto_produtos.insert(tk.END, "Nenhum produto cadastrado.\n")

# Funções para o CRUD
def adicionar_produto_interface():
    nome = nome_entry.get()
    quantidade = int(quantidade_entry.get())
    preco = float(preco_entry.get())
    if nome and quantidade and preco:
        adicionar_produto(nome, quantidade, preco)
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        exibir_produtos()
    else:
        messagebox.showwarning("Erro", "Todos os campos devem ser preenchidos!")

def atualizar_produto_interface():
    id_produto = int(id_entry.get())
    nome = nome_entry.get()
    quantidade = int(quantidade_entry.get())
    preco = float(preco_entry.get())
    if id_produto and nome and quantidade and preco:
        atualizar_produto(id_produto, nome, quantidade, preco)
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        exibir_produtos()
    else:
        messagebox.showwarning("Erro", "Todos os campos devem ser preenchidos!")

def remover_produto_interface():
    id_produto = int(id_entry.get())
    if id_produto:
        remover_produto(id_produto)
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
        exibir_produtos()
    else:
        messagebox.showwarning("Erro", "O ID do produto deve ser preenchido!")

# Criando a interface gráfica com tkinter
root = tk.Tk()
root.title("Sistema de Controle de Estoque")

# Labels e campos de entrada para o formulário
tk.Label(root, text="ID do Produto (para Atualizar/Remover)").grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

tk.Label(root, text="Nome do Produto").grid(row=1, column=0)
nome_entry = tk.Entry(root)
nome_entry.grid(row=1, column=1)

tk.Label(root, text="Quantidade").grid(row=2, column=0)
quantidade_entry = tk.Entry(root)
quantidade_entry.grid(row=2, column=1)

tk.Label(root, text="Preço").grid(row=3, column=0)
preco_entry = tk.Entry(root)
preco_entry.grid(row=3, column=1)

# Botões para as funções CRUD
tk.Button(root, text="Adicionar Produto", command=adicionar_produto_interface).grid(row=4, column=0)
tk.Button(root, text="Atualizar Produto", command=atualizar_produto_interface).grid(row=4, column=1)
tk.Button(root, text="Remover Produto", command=remover_produto_interface).grid(row=4, column=2)

# Área de texto para exibir os produtos
texto_produtos = tk.Text(root, height=10, width=50)
texto_produtos.grid(row=5, column=0, columnspan=3)

# Botão para listar os produtos
tk.Button(root, text="Listar Produtos", command=exibir_produtos).grid(row=6, column=0, columnspan=3)

# Exibe a janela
root.mainloop()
