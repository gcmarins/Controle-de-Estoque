#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
from prettytable import PrettyTable
import tkinter as tk
from tkinter import messagebox, ttk

# Funções do banco de dados

def criar_banco_dados():
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        );
        """)
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        conn.close()

def executar_query(query, params=()):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        print(f"Erro na operação do banco de dados: {e}")
        messagebox.showerror("Erro", f"Erro na operação do banco de dados: {e}")
    finally:
        conn.close()

def adicionar_produto(nome, quantidade):
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO produtos (nome, quantidade)
        VALUES (?, ?);
        """, (nome, quantidade))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao adicionar o produto: {e}")
        messagebox.showerror("Erro", f"Erro ao adicionar o produto: {e}")
    finally:
        conn.close()

def remover_produto(id_produto):
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        DELETE FROM produtos WHERE id = ?;
        """, (id_produto,))
        
        if cursor.rowcount == 0:
            messagebox.showwarning("Aviso", "Produto não encontrado.")
        else:
            messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao remover o produto: {e}")
        messagebox.showerror("Erro", f"Erro ao remover o produto: {e}")
    finally:
        conn.close()

def atualizar_quantidade(id_produto, nova_quantidade):
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        if produto_existe(id_produto):
            cursor.execute("""
            UPDATE produtos SET quantidade = ? WHERE id = ?;
            """, (nova_quantidade, id_produto))
            
            messagebox.showinfo("Sucesso", "Quantidade atualizada com sucesso.")
        else:
            messagebox.showwarning("Aviso", "Produto não encontrado.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar a quantidade: {e}")
        messagebox.showerror("Erro", f"Erro ao atualizar a quantidade: {e}")
    finally:
        conn.close()

def adicionar_unidades(id_produto, quantidade):
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        if produto_existe(id_produto):
            cursor.execute("""
            SELECT quantidade FROM produtos WHERE id = ?;
            """, (id_produto,))
            
            quantidade_atual = cursor.fetchone()[0]
            nova_quantidade = quantidade_atual + quantidade
            
            cursor.execute("""
            UPDATE produtos SET quantidade = ? WHERE id = ?;
            """, (nova_quantidade, id_produto))
            
            messagebox.showinfo("Sucesso", "Unidades adicionadas com sucesso.")
        else:
            messagebox.showwarning("Aviso", "Produto não encontrado.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao adicionar unidades: {e}")
        messagebox.showerror("Erro", f"Erro ao adicionar unidades: {e}")
    finally:
        conn.close()

def remover_unidades(id_produto, quantidade):
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        if produto_existe(id_produto):
            cursor.execute("""
            SELECT quantidade FROM produtos WHERE id = ?;
            """, (id_produto,))
            
            quantidade_atual = cursor.fetchone()[0]
            
            if quantidade > quantidade_atual:
                messagebox.showwarning("Aviso", "Quantidade a remover é maior do que a quantidade em estoque.")
                return
            
            nova_quantidade = quantidade_atual - quantidade
            cursor.execute("""
            UPDATE produtos SET quantidade = ? WHERE id = ?;
            """, (nova_quantidade, id_produto))
            
            messagebox.showinfo("Sucesso", "Unidades removidas com sucesso.")
        else:
            messagebox.showwarning("Aviso", "Produto não encontrado.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao remover unidades: {e}")
        messagebox.showerror("Erro", f"Erro ao remover unidades: {e}")
    finally:
        conn.close()

def produto_existe(id_produto):
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM produtos WHERE id = ?;
        """, (id_produto,))
        
        produto = cursor.fetchone()
        
        conn.close()
        
        return produto is not None
    except sqlite3.Error as e:
        print(f"Erro ao verificar a existência do produto: {e}")
        return False

def listar_produtos():
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM produtos;
        """)
        
        produtos = cursor.fetchall()
        
        conn.close()

        table = PrettyTable()
        table.field_names = ["ID", "Nome", "Quantidade"]
        for produto in produtos:
            table.add_row([produto[0], produto[1], produto[2]])
        
        messagebox.showinfo("Lista de Produtos", table.get_string())
    except sqlite3.Error as e:
        print(f"Erro ao listar os produtos: {e}")
        messagebox.showerror("Erro", f"Erro ao listar os produtos: {e}")

def gerar_planilha_excel():
    try:
        conn = sqlite3.connect('estoque.db')
        df = pd.read_sql_query("SELECT * FROM produtos", conn)
        df.to_excel('estoque_atualizado.xlsx', index=False)
        messagebox.showinfo("Sucesso", "Planilha Excel gerada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao gerar a planilha Excel: {e}")
    finally:
        conn.close()

def exit_program(root):
    if messagebox.askokcancel("Sair", "Deseja sair do programa?"):
        root.destroy()

# Função principal

def main_window():
    root = tk.Tk()
    root.title("Controle de Estoque")
    root.geometry("1920x1080")
    

    img = tk.PhotoImage(file="logo.gif")
    logo_label = tk.Label(root, image=img, bg='#f0f0f0')
    logo_label.pack(pady=20)
    
    ttk.Button(root, text="Cadastrar Produto", command=adicionar_produto_window).pack(pady=10)
    ttk.Button(root, text="Remover Produto", command=remover_produto_window).pack(pady=10)
    ttk.Button(root, text="Atualizar Quantidade de um Produto", command=atualizar_quantidade_window).pack(pady=10)
    ttk.Button(root, text="Adicionar Unidades", command=adicionar_unidades_window).pack(pady=10)
    ttk.Button(root, text="Remover Unidades", command=remover_unidades_window).pack(pady=10)
    ttk.Button(root, text="Listar Produtos", command=listar_produtos).pack(pady=10)
    ttk.Button(root, text="Gerar Planilha Excel", command=gerar_planilha_excel).pack(pady=10)
    ttk.Button(root, text="Sair", command=lambda: exit_program(root)).pack(pady=20)
    
    root.mainloop()

def adicionar_produto_window():
    def adicionar():
        nome = nome_entry.get()
        quantidade = quantidade_entry.get()
        
        if nome.strip() == "":
            messagebox.showwarning("Aviso", "O nome do produto não pode estar vazio.")
            return
        
        if not validar_numero(quantidade):
            messagebox.showwarning("Aviso", "A quantidade deve ser um número.")
            return
        
        adicionar_produto(nome, int(quantidade))
        window.destroy()

    window = tk.Toplevel()
    window.title("Adicionar Produto")
    
    nome_label = tk.Label(window, text="Nome do Produto:")
    nome_label.pack(pady=10)
    
    nome_entry = tk.Entry(window)
    nome_entry.pack(pady=10)
    
    quantidade_label = tk.Label(window, text="Quantidade:")
    quantidade_label.pack(pady=10)
    
    quantidade_entry = tk.Entry(window)
    quantidade_entry.pack(pady=10)
    
    adicionar_button = tk.Button(window, text="Adicionar", command=adicionar)
    adicionar_button.pack(pady=20)

def remover_produto_window():
    def remover():
        id_produto = id_entry.get()
        
        if not validar_numero(id_produto):
            messagebox.showwarning("Aviso", "O ID do produto deve ser um número.")
            return
        
        remover_produto(int(id_produto))
        window.destroy()

    window = tk.Toplevel()
    window.title("Remover Produto")
    
    id_label = tk.Label(window, text="ID do Produto:")
    id_label.pack(pady=10)
    
    id_entry = tk.Entry(window)
    id_entry.pack(pady=10)
    
    remover_button = tk.Button(window, text="Remover", command=remover)
    remover_button.pack(pady=20)

def atualizar_quantidade_window():
    def atualizar():
        id_produto = id_entry.get()
        nova_quantidade = nova_quantidade_entry.get()
        
        if not validar_numero(id_produto):
            messagebox.showwarning("Aviso", "O ID do produto deve ser um número.")
            return
        
        if not validar_numero(nova_quantidade):
            messagebox.showwarning("Aviso", "A nova quantidade deve ser um número.")
            return
        
        atualizar_quantidade(int(id_produto), int(nova_quantidade))
        window.destroy()

    window = tk.Toplevel()
    window.title("Atualizar Quantidade")
    
    id_label = tk.Label(window, text="ID do Produto:")
    id_label.pack(pady=10)
    
    id_entry = tk.Entry(window)
    id_entry.pack(pady=10)
    
    nova_quantidade_label = tk.Label(window, text="Nova Quantidade:")
    nova_quantidade_label.pack(pady=10)
    
    nova_quantidade_entry = tk.Entry(window)
    nova_quantidade_entry.pack(pady=10)
    
    atualizar_button = tk.Button(window, text="Atualizar", command=atualizar)
    atualizar_button.pack(pady=20)

def adicionar_unidades_window():
    def adicionar():
        id_produto = id_entry.get()
        quantidade = quantidade_entry.get()
        
        if not validar_numero(id_produto):
            messagebox.showwarning("Aviso", "O ID do produto deve ser um número.")
            return
        
        if not validar_numero(quantidade):
            messagebox.showwarning("Aviso", "A quantidade a adicionar deve ser um número.")
            return
        
        adicionar_unidades(int(id_produto), int(quantidade))
        window.destroy()

    window = tk.Toplevel()
    window.title("Adicionar Unidades")
    
    id_label = tk.Label(window, text="ID do Produto:")
    id_label.pack(pady=10)
    
    id_entry = tk.Entry(window)
    id_entry.pack(pady=10)
    
    quantidade_label = tk.Label(window, text="Quantidade a Adicionar:")
    quantidade_label.pack(pady=10)
    
    quantidade_entry = tk.Entry(window)
    quantidade_entry.pack(pady=10)
    
    adicionar_button = tk.Button(window, text="Adicionar", command=adicionar)
    adicionar_button.pack(pady=20)

def remover_unidades_window():
    def remover():
        id_produto = id_entry.get()
        quantidade = quantidade_entry.get()
        
        if not validar_numero(id_produto):
            messagebox.showwarning("Aviso", "O ID do produto deve ser um número.")
            return
        
        if not validar_numero(quantidade):
            messagebox.showwarning("Aviso", "A quantidade a remover deve ser um número.")
            return
        
        remover_unidades(int(id_produto), int(quantidade))
        window.destroy()

    window = tk.Toplevel()
    window.title("Remover Unidades")
    
    id_label = tk.Label(window, text="ID do Produto:")
    id_label.pack(pady=10)
    
    id_entry = tk.Entry(window)
    id_entry.pack(pady=10)
    
    quantidade_label = tk.Label(window, text="Quantidade a Remover:")
    quantidade_label.pack(pady=10)
    
    quantidade_entry = tk.Entry(window)
    quantidade_entry.pack(pady=10)
    
    remover_button = tk.Button(window, text="Remover", command=remover)
    remover_button.pack(pady=20)

def validar_numero(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    criar_banco_dados()
    main_window()


# In[ ]:




