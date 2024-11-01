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

# Função para calcular os pontos da curva de Bézier de grau 3
def bezier_cubica(p0, p1, p2, p3, num_points=100):
    pontos = []
    for t in range(num_points + 1):
        t /= num_points
        # Cálculo da curva de Bézier cúbica
        x = ((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] +
             3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0])
        y = ((1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] +
             3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1])
        pontos.append((int(round(x)), int(round(y))))
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
def validar_coordenadas(pontos):
    for (x, y) in pontos:
        if not (LIMITE_MIN < x < LIMITE_MAX and LIMITE_MIN < y < LIMITE_MAX):
            return False
    return True

# Função para capturar os dados da interface e executar o algoritmo
def executar_bezier():
    try:
        # Obter os valores de entrada
        x0 = int(entry_x0.get())
        y0 = int(entry_y0.get())
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())
        x3 = int(entry_x3.get())
        y3 = int(entry_y3.get())
        
        # Coordenadas dos pontos de controle
        p0 = (x0, y0)
        p1 = (x1, y1)
        p2 = (x2, y2)
        p3 = (x3, y3)
        
        # Calcular a curva de Bézier cúbica
        pontos = bezier_cubica(p0, p1, p2, p3)

        # Validar limites
        if validar_coordenadas(pontos):
            # Executa o algoritmo e desenha a curva na malha de pixels
            desenhar_linha_na_malha(pontos)
        else:
            tk.messagebox.showerror("Erro", f"As coordenadas devem estar entre {LIMITE_MIN} e {LIMITE_MAX}.")
    
    except ValueError:
        tk.messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Curva de Bézier de Grau 3 - Malha de Pixels")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

# Desenhar a malha inicial
desenhar_malha()

# Labels e Campos de entrada para os pontos de controle
label_x0 = tk.Label(janela, text=f"Ponto Inicial X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x0.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_x0 = tk.Entry(janela)
entry_x0.grid(row=0, column=2, padx=10, pady=5)

label_y0 = tk.Label(janela, text=f"Ponto Inicial Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y0.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_y0 = tk.Entry(janela)
entry_y0.grid(row=1, column=2, padx=10, pady=5)

label_x1 = tk.Label(janela, text=f"Ponto de Controle 1 X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x1.grid(row=2, column=1, padx=10, pady=5, sticky="w")
entry_x1 = tk.Entry(janela)
entry_x1.grid(row=2, column=2, padx=10, pady=5)

label_y1 = tk.Label(janela, text=f"Ponto de Controle 1 Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y1.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry_y1 = tk.Entry(janela)
entry_y1.grid(row=3, column=2, padx=10, pady=5)

label_x2 = tk.Label(janela, text=f"Ponto de Controle 2 X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x2.grid(row=4, column=1, padx=10, pady=5, sticky="w")
entry_x2 = tk.Entry(janela)
entry_x2.grid(row=4, column=2, padx=10, pady=5)

label_y2 = tk.Label(janela, text=f"Ponto de Controle 2 Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y2.grid(row=5, column=1, padx=10, pady=5, sticky="w")
entry_y2 = tk.Entry(janela)
entry_y2.grid(row=5, column=2, padx=10, pady=5)

label_x3 = tk.Label(janela, text=f"Ponto Final X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x3.grid(row=6, column=1, padx=10, pady=5, sticky="w")
entry_x3 = tk.Entry(janela)
entry_x3.grid(row=6, column=2, padx=10, pady=5)

label_y3 = tk.Label(janela, text=f"Ponto Final Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y3.grid(row=7, column=1, padx=10, pady=5, sticky="w")
entry_y3 = tk.Entry(janela)
entry_y3.grid(row=7, column=2, padx=10, pady=5)

# Botão para executar o algoritmo de Bézier
botao_executar = tk.Button(janela, text="Desenhar Curva de Bézier", command=executar_bezier)
botao_executar.grid(row=8, column=1, columnspan=2, pady=10)

# Iniciar a interface gráfica
janela.mainloop()