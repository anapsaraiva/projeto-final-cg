import tkinter as tk

# Definições do tamanho da malha
GRID_SIZE = 22  # Número de células na grade (22x22)
CELL_SIZE = 20  # Tamanho de cada célula em pixels
LIMITE_MIN = -11
LIMITE_MAX = 11

# Função para o algoritmo de Bresenham
def bresenham(x1, y1, x2, y2):
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

# Função para desenhar a linha na malha de pixels
def desenhar_linha_na_malha(pontos):
    # Limpa a grade antes de desenhar
    canvas.delete("all")
    desenhar_malha()

    # Desenha cada ponto da linha colorindo as células da malha
    for (x, y) in pontos:
        # Ajusta a coordenada Y para inverter o eixo (topo da tela é Y positivo)
        x_canvas = (x + GRID_SIZE // 2) * CELL_SIZE
        y_canvas = ((-y) + GRID_SIZE // 2) * CELL_SIZE  # Inverte o valor de Y
        canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill="blue")

# Função para desenhar a malha de fundo
def desenhar_malha():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x_start = i * CELL_SIZE
            y_start = j * CELL_SIZE
            canvas.create_rectangle(x_start, y_start, x_start + CELL_SIZE, y_start + CELL_SIZE, outline="gray")

# Função para validar as coordenadas
def validar_coordenadas(x1, y1, x2, y2):
    if (LIMITE_MIN < x1 < LIMITE_MAX and LIMITE_MIN < y1 < LIMITE_MAX and 
        LIMITE_MIN < x2 < LIMITE_MAX and LIMITE_MIN < y2 < LIMITE_MAX):
        return True
    else:
        return False

# Função para capturar os dados da interface e executar o algoritmo
def executar_bresenham():
    try:
        # Obter os valores de entrada
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())
        
        # Validar limites
        if validar_coordenadas(x1, y1, x2, y2):
            # Executa o algoritmo e desenha a linha na malha de pixels
            pontos = bresenham(x1, y1, x2, y2)
            desenhar_linha_na_malha(pontos)
        else:
            tk.messagebox.showerror("Erro", f"As coordenadas devem estar entre {LIMITE_MIN} e {LIMITE_MAX}.")
    
    except ValueError:
        tk.messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Algoritmo de Bresenham - Malha de Pixels")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

# Desenhar a malha inicial
desenhar_malha()

# Label e Campo de entrada para o ponto inicial (X1, Y1)
label_x1 = tk.Label(janela, text=f"Coordenada X1 ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x1.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_x1 = tk.Entry(janela)
entry_x1.grid(row=0, column=2, padx=10, pady=5)

label_y1 = tk.Label(janela, text=f"Coordenada Y1 ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y1.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_y1 = tk.Entry(janela)
entry_y1.grid(row=1, column=2, padx=10, pady=5)

# Label e Campo de entrada para o ponto final (X2, Y2)
label_x2 = tk.Label(janela, text=f"Coordenada X2 ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x2.grid(row=2, column=1, padx=10, pady=5, sticky="w")
entry_x2 = tk.Entry(janela)
entry_x2.grid(row=2, column=2, padx=10, pady=5)

label_y2 = tk.Label(janela, text=f"Coordenada Y2 ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y2.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry_y2 = tk.Entry(janela)
entry_y2.grid(row=3, column=2, padx=10, pady=5)

# Botão para executar o algoritmo de Bresenham
botao_executar = tk.Button(janela, text="Desenhar Linha", command=executar_bresenham)
botao_executar.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Executa a janela
janela.mainloop()
