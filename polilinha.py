import tkinter as tk

# Definições do tamanho da malha
GRID_SIZE = 22  # Número de células na grade (20x20)
CELL_SIZE = 20  # Tamanho de cada célula em pixels
LIMITE_MIN = -11
LIMITE_MAX = 11

# Lista de pontos inseridos
pontos_polilinha = []

# Função para desenhar uma linha usando Bresenham
def bresenham_linha(x1, y1, x2, y2):
    pontos = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    erro = dx - dy
    
    while True:
        pontos.append((x1, y1))  # Adiciona o ponto atual à lista
        if x1 == x2 and y1 == y2:
            break
        
        e2 = 2 * erro
        if e2 > -dy:
            erro -= dy
            x1 += sx
        if e2 < dx:
            erro += dx
            y1 += sy
    
    return pontos

# Função para desenhar a polilinha na malha de pixels
def desenhar_polilinha_na_malha(pontos):
    # Limpa a grade antes de desenhar
    canvas.delete("all")
    desenhar_malha()

    # Desenha cada ponto da polilinha colorindo as células da malha em azul
    for (x1, y1), (x2, y2) in zip(pontos[:-1], pontos[1:]):
        linha = bresenham_linha(x1, y1, x2, y2)
        for (x, y) in linha:
            x_canvas = (x + GRID_SIZE // 2) * CELL_SIZE
            y_canvas = ((-y) + GRID_SIZE // 2) * CELL_SIZE  # Inverte o valor de Y
            canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill="blue")

    # Destacar os pontos da polilinha com um círculo roxo
    for (x, y) in pontos:
        x_canvas = (x + GRID_SIZE // 2) * CELL_SIZE
        y_canvas = ((-y) + GRID_SIZE // 2) * CELL_SIZE  # Inverte o valor de Y
        canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill="purple")

# Função para desenhar a malha de fundo
def desenhar_malha():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x_start = i * CELL_SIZE
            y_start = j * CELL_SIZE
            canvas.create_rectangle(x_start, y_start, x_start + CELL_SIZE, y_start + CELL_SIZE, outline="gray")

# Função para adicionar pontos à polilinha
def adicionar_ponto():
    try:
        # Obter os valores de entrada
        x = int(entry_x.get())
        y = int(entry_y.get())

        # Validar o ponto inserido
        if LIMITE_MIN < x < LIMITE_MAX and LIMITE_MIN < y < LIMITE_MAX:
            # Adicionar o ponto à lista de pontos da polilinha
            pontos_polilinha.append((x, y))
            label_status.config(text=f"Ponto ({x}, {y}) adicionado. Total de pontos: {len(pontos_polilinha)}")
        else:
            tk.messagebox.showerror("Erro", f"As coordenadas devem estar entre {LIMITE_MIN} e {LIMITE_MAX}.")
    
    except ValueError:
        tk.messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Função para desenhar a polilinha após N pontos
def desenhar_polilinha():
    if len(pontos_polilinha) > 3:
        desenhar_polilinha_na_malha(pontos_polilinha)
    else:
        tk.messagebox.showerror("Erro", "A polilinha requer pelo menos 4 pontos.")

# Função para resetar os pontos da polilinha
def resetar_polilinha():
    global pontos_polilinha
    pontos_polilinha = []
    label_status.config(text="Nenhum ponto adicionado.")
    desenhar_malha()

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Desenho de Polilinha - Malha de Pixels")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

# Desenhar a malha inicial
desenhar_malha()

# Label e Campo de entrada para adicionar pontos (X, Y)
label_x = tk.Label(janela, text=f"Coordenada X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_x = tk.Entry(janela)
entry_x.grid(row=0, column=2, padx=10, pady=5)

label_y = tk.Label(janela, text=f"Coordenada Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_y = tk.Entry(janela)
entry_y.grid(row=1, column=2, padx=10, pady=5)

# Botão para adicionar pontos
botao_adicionar = tk.Button(janela, text="Adicionar Ponto", command=adicionar_ponto)
botao_adicionar.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Botão para desenhar a polilinha
botao_desenhar = tk.Button(janela, text="Desenhar Polilinha", command=desenhar_polilinha)
botao_desenhar.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Botão para resetar os pontos
botao_resetar = tk.Button(janela, text="Resetar", command=resetar_polilinha)
botao_resetar.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Status
label_status = tk.Label(janela, text="Nenhum ponto adicionado.")
label_status.grid(row=5, column=1, columnspan=2)

# Executa a janela
janela.mainloop()