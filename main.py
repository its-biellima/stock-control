# Importar bibliotecas  
import pg8000
import tkinter as tk
from tkinter import messagebox

# Configurações de conexão com o banco de dados
DB_HOST = "127.0.0.1" # Endereço local do Banco
DB_NAME = "Lagoinha Book Store"
DB_USER = "postgres"
DB_PASSWORD = "31415"

# Função para conectar ao banco de dados
def connect_db():
    return pg8000.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

# Função para cadastrar um novo item
def cadastrar_item():
    conn = connect_db()
    cursor = conn.cursor()
    
    product_id = entry_id.get()
    product_name = entry_name.get()
    product_value = float(entry_value.get())
    product_quantity = int(entry_quantity.get())

    cursor.execute(
        "INSERT INTO itens (id, nome, valor, quantidade) VALUES (%s, %s, %s, %s)",
        (product_id, product_name, product_value, product_quantity)
    )
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Item cadastrado com sucesso")
    limpar_campos()

# Função para consultar um item
def consultar_item():
    conn = connect_db()
    cursor = conn.cursor()
    
    product_id = entry_id.get()
    
    cursor.execute("SELECT * FROM itens WHERE id = %s", (product_id,))
    item = cursor.fetchone()
    
    if item:
        total_value = item[2] * item[3]
        messagebox.showinfo("Consulta", f"ID: {item[0]}\nNome: {item[1]}\nValor Unitário: R$ {item[2]:.2f}\nQuantidade: {item[3]}\nValor Total do Estoque: R$ {total_value:.2f}")
    else:
        messagebox.showerror("Erro", "Item não encontrado")

    conn.close()

# Função para fazer uma venda
def fazer_venda():
    conn = connect_db()
    cursor = conn.cursor()
    
    product_id = entry_id.get()
    venda_quantidade = int(entry_quantity.get())
    
    cursor.execute("SELECT quantidade FROM itens WHERE id = %s", (product_id,))
    item = cursor.fetchone()
    
    if item and item[0] >= venda_quantidade:
        nova_quantidade = item[0] - venda_quantidade
        cursor.execute("UPDATE itens SET quantidade = %s WHERE id = %s", (nova_quantidade, product_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Venda realizada com sucesso")
    else:
        messagebox.showerror("Erro", "Quantidade insuficiente ou item não encontrado")

    conn.close()
    limpar_campos()

# Função para fazer uma devolução
def fazer_devolucao():
    conn = connect_db()
    cursor = conn.cursor()
    
    product_id = entry_id.get()
    devolucao_quantidade = int(entry_quantity.get())
    
    cursor.execute("SELECT quantidade FROM itens WHERE id = %s", (product_id,))
    item = cursor.fetchone()
    
    if item:
        nova_quantidade = item[0] + devolucao_quantidade
        cursor.execute("UPDATE itens SET quantidade = %s WHERE id = %s", (nova_quantidade, product_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Devolução realizada com sucesso")
    else:
        messagebox.showerror("Erro", "Item não encontrado")

    conn.close()
    limpar_campos()

# Função para visualizar o estoque de forma macro com barra de rolagem
def visualizar_estoque():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nome, quantidade, valor FROM itens ORDER BY id ASC")
    itens = cursor.fetchall()
    
    total_estoque = 0
    estoque_detalhes = ""
    
    for item in itens:
        item_total = item[2] * item[3]
        estoque_detalhes += f"ID: {item[0]}\nNome: {item[1]}\nQuantidade: {item[2]}\nValor Total: R$ {item_total:.2f}\n\n"
        total_estoque += item_total
    
    estoque_detalhes += f"Valor Total do Estoque: R$ {total_estoque:.2f}"
    
    # Criando uma nova janela para exibir o estoque
    top = tk.Toplevel(root)
    top.title("Estoque Completo")

    # Adicionando um frame para o Text widget e a barra de rolagem
    text_frame = tk.Frame(top)
    text_frame.pack(fill="both", expand=True)
    
    # Criando a barra de rolagem
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    # Criando o Text widget
    text_widget = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap="word", font=("Arial", 12))
    text_widget.pack(fill="both", expand=True)
    
    # Configurando a barra de rolagem para o Text widget
    scrollbar.config(command=text_widget.yview)
    
    # Inserindo os detalhes do estoque no Text widget
    text_widget.insert(tk.END, estoque_detalhes)
    text_widget.config(state="disabled")  # Tornando o Text widget somente leitura

    conn.close()

# Função para limpar os campos de entrada
def limpar_campos():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_value.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Lagoinha Bookstore")
root.configure(bg="white")

# Labels e campos de entrada
tk.Label(root, text="ID do Produto:", bg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_id = tk.Entry(root, font=("Arial", 12))
entry_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nome do Produto:", bg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_name = tk.Entry(root, font=("Arial", 12))
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Valor Unitário:", bg="white", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_value = tk.Entry(root, font=("Arial", 12))
entry_value.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Quantidade:", bg="white", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_quantity = tk.Entry(root, font=("Arial", 12))
entry_quantity.grid(row=3, column=1, padx=10, pady=5)

# Botões de ação
button_frame = tk.Frame(root, bg="white")
button_frame.grid(row=4, column=0, columnspan=2, pady=10)

tk.Button(button_frame, text="Cadastrar Item", bg="blue", fg="white", command=cadastrar_item, font=("Arial", 12)).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Consultar Item", bg="blue", fg="white", command=consultar_item, font=("Arial", 12)).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Fazer Venda", bg="blue", fg="white", command=fazer_venda, font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Fazer Devolução", bg="blue", fg="white", command=fazer_devolucao, font=("Arial", 12)).grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Visualizar Estoque", bg="blue", fg="white", command=visualizar_estoque, font=("Arial", 12)).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(button_frame, text="Limpar Campos", bg="blue", fg="white", command=limpar_campos, font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
