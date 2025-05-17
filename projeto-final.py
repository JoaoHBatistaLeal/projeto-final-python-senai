import sqlite3  # banco de dados
import tkinter as tk  # interface básica
from tkinter import messagebox  # caixas de mensagens
from tkinter import ttk  # interface gráfica avançada

# Conexão com o banco de dados
def conectar():
    return sqlite3.connect('advocacia.db')

# Função para criar tabelas
def criar_tabelas():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS colaboradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS horas_trabalhadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colaborador TEXT NOT NULL,
            cliente TEXT NOT NULL,
            tarefa TEXT NOT NULL,
            horas REAL NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para atualizar a lista de colaboradores e clientes no Combobox
def atualizar_listas():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT nome FROM colaboradores')
    colaboradores = [row[0] for row in c.fetchall()]
    c.execute('SELECT nome FROM clientes')
    clientes = [row[0] for row in c.fetchall()]
    conn.close()
    combobox_colaborador['values'] = colaboradores
    combobox_cliente['values'] = clientes
    combobox_cliente_calculo['values'] = clientes
    combobox_colaborador_calculo['values'] = colaboradores

# Função para registrar colaboradores
def registrar_colaborador():
    nome = entry_nome_colaborador.get()
    if nome:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO colaboradores (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Colaborador registrado com sucesso!")
        atualizar_listas()
    else:
        messagebox.showerror("Erro", "O campo nome deve ser preenchido.")

# Função para registrar clientes
def registrar_cliente():
    nome = entry_nome_cliente.get()
    if nome:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO clientes (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente registrado com sucesso!")
        atualizar_listas()
    else:
        messagebox.showerror("Erro", "O campo nome deve ser preenchido.")

# Função para registrar horas trabalhadas
def registrar_horas():
    colaborador = combobox_colaborador.get()
    cliente = combobox_cliente.get()
    tarefa = combobox_tarefa.get()
    horas = entry_horas.get()
    data = entry_data.get()

    if colaborador and cliente and tarefa and horas and data:
        try:
            horas = float(horas)
            conn = conectar()
            c = conn.cursor()
            c.execute('INSERT INTO horas_trabalhadas (colaborador, cliente, tarefa, horas, data) VALUES (?, ?, ?, ?, ?)',
                      (colaborador, cliente, tarefa, horas, data))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Horas registradas com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "O campo de horas deve ser um número.")
    else:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

# Função para calcular total de horas por cliente
def calcular_por_cliente():
    cliente = combobox_cliente_calculo.get()
    if cliente:
        conn = conectar()
        c = conn.cursor()
        c.execute('SELECT SUM(horas) FROM horas_trabalhadas WHERE cliente = ?', (cliente,))
        total = c.fetchone()[0]
        conn.close()
        if total:
            messagebox.showinfo("Total de Horas", f"Total de horas para o cliente '{cliente}': {total:.2f}")
        else:
            messagebox.showinfo("Total de Horas", f"Nenhuma hora registrada para o cliente '{cliente}'.")
    else:
        messagebox.showerror("Erro", "Selecione um cliente.")

# Função para calcular total de horas por colaborador
def calcular_por_colaborador():
    colaborador = combobox_colaborador_calculo.get()
    if colaborador:
        conn = conectar()
        c = conn.cursor()
        c.execute('SELECT SUM(horas) FROM horas_trabalhadas WHERE colaborador = ?', (colaborador,))
        total = c.fetchone()[0]
        conn.close()
        if total:
            messagebox.showinfo("Total de Horas", f"Total de horas para o colaborador '{colaborador}': {total:.2f}")
        else:
            messagebox.showinfo("Total de Horas", f"Nenhuma hora registrada para o colaborador '{colaborador}'.")
    else:
        messagebox.showerror("Erro", "Selecione um colaborador.")

# Função para calcular total de horas por dia
def calcular_por_dia():
    data = entry_data_calculo.get()
    if data:
        conn = conectar()
        c = conn.cursor()
        c.execute('SELECT SUM(horas) FROM horas_trabalhadas WHERE data = ?', (data,))
        total = c.fetchone()[0]
        conn.close()
        if total:
            messagebox.showinfo("Total de Horas", f"Total de horas no dia '{data}': {total:.2f}")
        else:
            messagebox.showinfo("Total de Horas", f"Nenhuma hora registrada no dia '{data}'.")
    else:
        messagebox.showerror("Erro", "Preencha a data.")

# Função para calcular total de horas por mês
def calcular_por_mes():
    mes = entry_mes_calculo.get()
    if mes:
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT SUM(horas) FROM horas_trabalhadas WHERE strftime('%m', data) = ?", (mes.zfill(2),))
        total = c.fetchone()[0]
        conn.close()
        if total:
            messagebox.showinfo("Total de Horas", f"Total de horas no mês '{mes}': {total:.2f}")
        else:
            messagebox.showinfo("Total de Horas", f"Nenhuma hora registrada no mês '{mes}'.")
    else:
        messagebox.showerror("Erro", "Preencha o mês.")

# Função para calcular total de horas por ano
def calcular_por_ano():
    ano = entry_ano_calculo.get()
    if ano:
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT SUM(horas) FROM horas_trabalhadas WHERE strftime('%Y', data) = ?", (ano,))
        total = c.fetchone()[0]
        conn.close()
        if total:
            messagebox.showinfo("Total de Horas", f"Total de horas no ano '{ano}': {total:.2f}")
        else:
            messagebox.showinfo("Total de Horas", f"Nenhuma hora registrada no ano '{ano}'.")
    else:
        messagebox.showerror("Erro", "Preencha o ano.")

# Interface gráfica
root = tk.Tk()
root.title("Controle de Horas Trabalhadas")

# Campos para registrar colaboradores
tk.Label(root, text="Nome do Colaborador:").grid(row=0, column=0)
entry_nome_colaborador = tk.Entry(root)
entry_nome_colaborador.grid(row=0, column=1)

btn_registrar_colaborador = tk.Button(root, text="Registrar Colaborador", command=registrar_colaborador)
btn_registrar_colaborador.grid(row=1, column=0, columnspan=2, pady=10)

# Campos para registrar clientes
tk.Label(root, text="Nome do Cliente:").grid(row=2, column=0)
entry_nome_cliente = tk.Entry(root)
entry_nome_cliente.grid(row=2, column=1)

btn_registrar_cliente = tk.Button(root, text="Registrar Cliente", command=registrar_cliente)
btn_registrar_cliente.grid(row=3, column=0, columnspan=2, pady=10)

# Campos para registrar horas trabalhadas
tk.Label(root, text="Colaborador:").grid(row=4, column=0)
combobox_colaborador = ttk.Combobox(root)
combobox_colaborador.grid(row=4, column=1)

tk.Label(root, text="Cliente:").grid(row=5, column=0)
combobox_cliente = ttk.Combobox(root)
combobox_cliente.grid(row=5, column=1)

tk.Label(root, text="Tarefa:").grid(row=6, column=0)
combobox_tarefa = ttk.Combobox(root, values=["Reunião", "Pesquisa Jurídica", "Redação de Documentos", "Audiência"])
combobox_tarefa.grid(row=6, column=1)

tk.Label(root, text="Horas:").grid(row=7, column=0)
entry_horas = tk.Entry(root)
entry_horas.grid(row=7, column=1)

tk.Label(root, text="Data (YYYY-MM-DD):").grid(row=8, column=0)
entry_data = tk.Entry(root)
entry_data.grid(row=8, column=1)

btn_registrar = tk.Button(root, text="Registrar Horas", command=registrar_horas)
btn_registrar.grid(row=9, column=0, columnspan=2, pady=10)

# Interface gráfica para cálculos
tk.Label(root, text="Cálculos").grid(row=10, column=0, columnspan=2, pady=10)

# Cálculo por cliente
tk.Label(root, text="Cliente:").grid(row=11, column=0)
combobox_cliente_calculo = ttk.Combobox(root)
combobox_cliente_calculo.grid(row=11, column=1)

btn_calcular_cliente = tk.Button(root, text="Calcular por Cliente", command=calcular_por_cliente)
btn_calcular_cliente.grid(row=12, column=0, columnspan=2, pady=5)

# Cálculo por colaborador
tk.Label(root, text="Colaborador:").grid(row=13, column=0)
combobox_colaborador_calculo = ttk.Combobox(root)
combobox_colaborador_calculo.grid(row=13, column=1)

btn_calcular_colaborador = tk.Button(root, text="Calcular por Colaborador", command=calcular_por_colaborador)
btn_calcular_colaborador.grid(row=14, column=0, columnspan=2, pady=5)

# Cálculo por dia
tk.Label(root, text="Data (YYYY-MM-DD):").grid(row=15, column=0)
entry_data_calculo = tk.Entry(root)
entry_data_calculo.grid(row=15, column=1)

btn_calcular_dia = tk.Button(root, text="Calcular por Dia", command=calcular_por_dia)
btn_calcular_dia.grid(row=16, column=0, columnspan=2, pady=5)

# Cálculo por mês
tk.Label(root, text="Mês (MM):").grid(row=17, column=0)
entry_mes_calculo = tk.Entry(root)
entry_mes_calculo.grid(row=17, column=1)

btn_calcular_mes = tk.Button(root, text="Calcular por Mês", command=calcular_por_mes)
btn_calcular_mes.grid(row=18, column=0, columnspan=2, pady=5)

# Cálculo por ano
tk.Label(root, text="Ano (YYYY):").grid(row=19, column=0)
entry_ano_calculo = tk.Entry(root)
entry_ano_calculo.grid(row=19, column=1)

btn_calcular_ano = tk.Button(root, text="Calcular por Ano", command=calcular_por_ano)
btn_calcular_ano.grid(row=20, column=0, columnspan=2, pady=5)

# Criar tabelas no banco de dados e atualizar listas
criar_tabelas()
atualizar_listas()

root.mainloop()