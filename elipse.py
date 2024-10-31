import tkinter as tk

# Definições do tamanho da malha
GRID_SIZE = 22  # Número de células na grade (20x20)
CELL_SIZE = 20  # Tamanho de cada célula em pixels
LIMITE_MIN = -11
LIMITE_MAX = 11

# Função para desenhar uma elipse usando o Algoritmo de Bresenham
def bresenham_elipse(centro_x, centro_y, raio_hor, raio_ver):
    pontos = []
    x = 0
    y = raio_ver
    raio_hor2 = raio_hor * raio_hor
    raio_ver2 = raio_ver * raio_ver
    d1 = raio_ver2 - raio_hor2 * raio_ver + (raio_hor2 / 4)
    dx = 2 * raio_ver2 * x
    dy = 2 * raio_hor2 * y

    # Região 1
    while dx < dy:
        pontos.extend([
            (centro_x + x, centro_y + y), (centro_x - x, centro_y + y),
            (centro_x + x, centro_y - y), (centro_x - x, centro_y - y)
        ])
        if d1 < 0:
            x += 1
            dx += 2 * raio_ver2
            d1 += dx + raio_ver2
        else:
            x += 1
            y -= 1
            dx += 2 * raio_ver2
            dy -= 2 * raio_hor2
            d1 += dx - dy + raio_ver2

    # Região 2
    d2 = raio_ver2 * (x + 0.5) * (x + 0.5) + raio_hor2 * (y - 1) * (y - 1) - raio_hor2 * raio_ver2
    while y >= 0:
        pontos.extend([
            (centro_x + x, centro_y + y), (centro_x - x, centro_y + y),
            (centro_x + x, centro_y - y), (centro_x - x, centro_y - y)
        ])
        if d2 > 0:
            y -= 1
            dy -= 2 * raio_hor2
            d2 += raio_hor2 - dy
        else:
            x += 1
            y -= 1
            dx += 2 * raio_ver2
            dy -= 2 * raio_hor2
            d2 += dx - dy + raio_hor2

    return pontos

# Função para desenhar a elipse e o "raio" (um único pixel no centro) na malha de pixels
def desenhar_elipse_na_malha(pontos_elipse, centro_x, centro_y):
    # Limpa a grade antes de desenhar
    canvas.delete("all")
    desenhar_malha()

    # Desenha cada ponto da elipse colorindo as células da malha em azul
    for (x, y) in pontos_elipse:
        x_canvas = (x + GRID_SIZE // 2) * CELL_SIZE
        y_canvas = ((-y) + GRID_SIZE // 2) * CELL_SIZE  # Inverte o valor de Y
        canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill="blue")

    # Desenha o centro da elipse (representando o "raio") em roxo
    x_canvas = (centro_x + GRID_SIZE // 2) * CELL_SIZE
    y_canvas = ((-centro_y) + GRID_SIZE // 2) * CELL_SIZE  # Inverte o valor de Y
    canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill="purple")

# Função para desenhar a malha de fundo
def desenhar_malha():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x_start = i * CELL_SIZE
            y_start = j * CELL_SIZE
            canvas.create_rectangle(x_start, y_start, x_start + CELL_SIZE, y_start + CELL_SIZE, outline="gray")

# Função para validar as coordenadas e os raios da elipse
def validar_dados(centro_x, centro_y, raio_hor, raio_ver):
    if (LIMITE_MIN < centro_x < LIMITE_MAX and LIMITE_MIN < centro_y < LIMITE_MAX and
        raio_hor > 0 and raio_hor <= 11 and raio_ver > 0 and raio_ver <= 11):
        return True
    else:
        return False

# Função para capturar os dados da interface e executar o algoritmo
def executar_elipse():
    try:
        # Obter os valores de entrada
        centro_x = int(entry_centro_x.get())
        centro_y = int(entry_centro_y.get())
        raio_hor = int(entry_raio_hor.get())
        raio_ver = int(entry_raio_ver.get())
        
        # Validar os valores de entrada
        if validar_dados(centro_x, centro_y, raio_hor, raio_ver):
            # Executa o algoritmo para desenhar a elipse
            pontos_elipse = bresenham_elipse(centro_x, centro_y, raio_hor, raio_ver)

            # Desenha a elipse e o pixel representando o centro (raio)
            desenhar_elipse_na_malha(pontos_elipse, centro_x, centro_y)
        else:
            tk.messagebox.showerror("Erro", f"As coordenadas e raios devem estar entre {LIMITE_MIN} e {LIMITE_MAX}, e os raios devem ser maiores que 0 e menores ou iguais a 11.")
    
    except ValueError:
        tk.messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Algoritmo de Bresenham para Elipses - Malha de Pixels")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

# Desenhar a malha inicial
desenhar_malha()

# Label e Campo de entrada para o centro da elipse (Centro X, Centro Y)
label_centro_x = tk.Label(janela, text=f"Centro X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_centro_x.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_centro_x = tk.Entry(janela)
entry_centro_x.grid(row=0, column=2, padx=10, pady=5)

label_centro_y = tk.Label(janela, text=f"Centro Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_centro_y.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_centro_y = tk.Entry(janela)
entry_centro_y.grid(row=1, column=2, padx=10, pady=5)

# Label e Campo de entrada para o raio horizontal e vertical da elipse
label_raio_hor = tk.Label(janela, text="Raio Horizontal (0 < r <= 11):")
label_raio_hor.grid(row=2, column=1, padx=10, pady=5, sticky="w")
entry_raio_hor = tk.Entry(janela)
entry_raio_hor.grid(row=2, column=2, padx=10, pady=5)

label_raio_ver = tk.Label(janela, text="Raio Vertical (0 < r <= 11):")
label_raio_ver.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry_raio_ver = tk.Entry(janela)
entry_raio_ver.grid(row=3, column=2, padx=10, pady=5)

# Botão para executar o algoritmo de Bresenham para Elipses
botao_executar = tk.Button(janela, text="Desenhar Elipse", command=executar_elipse)
botao_executar.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Executa a janela
janela.mainloop()
