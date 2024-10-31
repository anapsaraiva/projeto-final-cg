import tkinter as tk
import tkinter.messagebox as messagebox

# Definições do tamanho da malha
GRID_SIZE = 22  # Número de células na grade (20x20)
CELL_SIZE = 20  # Tamanho de cada célula em pixels
LIMITE_MIN = -11
LIMITE_MAX = 11

# Variáveis para armazenar linhas e a janela de recorte
linhas = []
janela_recorte = (-5, -5, 5, 5)  # (xmin, ymin, xmax, ymax)

# Códigos de região para o algoritmo de Cohen-Sutherland
ACIMA = 1  # 0001
ABAIXO = 2  # 0010
DIREITA = 4  # 0100
ESQUERDA = 8  # 1000

# Função para desenhar um pixel na malha
def desenhar_pixel(x, y, cor):
    x_canvas = (x + GRID_SIZE // 2) * CELL_SIZE
    y_canvas = ((-y) + GRID_SIZE // 2) * CELL_SIZE  # Inverte o valor de Y
    canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill=cor)

# Função para desenhar uma linha usando Bresenham
def bresenham_linha(x1, y1, x2, y2, cor="black"):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    erro = dx - dy

    while True:
        desenhar_pixel(x1, y1, cor)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * erro
        if e2 > -dy:
            erro -= dy
            x1 += sx
        if e2 < dx:
            erro += dx
            y1 += sy

# Função para obter o código de região de um ponto (x, y)
def calcular_codigo(x, y):
    xmin, ymin, xmax, ymax = janela_recorte
    codigo = 0
    if x < xmin:  # Esquerda da janela
        codigo |= ESQUERDA
    elif x > xmax:  # Direita da janela
        codigo |= DIREITA
    if y < ymin:  # Abaixo da janela
        codigo |= ABAIXO
    elif y > ymax:  # Acima da janela
        codigo |= ACIMA
    return codigo

# Função para recortar uma linha usando o algoritmo de Cohen-Sutherland
def recorte_cohen_sutherland(x1, y1, x2, y2):
    codigo1 = calcular_codigo(x1, y1)
    codigo2 = calcular_codigo(x2, y2)
    xmin, ymin, xmax, ymax = janela_recorte
    dentro = False

    while True:
        if codigo1 == 0 and codigo2 == 0:  # Completamente dentro
            dentro = True
            break
        elif (codigo1 & codigo2) != 0:  # Completamente fora
            break
        else:
            x, y = 0, 0
            if codigo1 != 0:
                codigo_out = codigo1
            else:
                codigo_out = codigo2

            # Interseções com as bordas da janela
            if codigo_out & ACIMA:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif codigo_out & ABAIXO:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif codigo_out & DIREITA:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif codigo_out & ESQUERDA:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Atualizar o ponto de interseção e o código
            if codigo_out == codigo1:
                x1, y1 = int(x), int(y)
                codigo1 = calcular_codigo(x1, y1)
            else:
                x2, y2 = int(x), int(y)
                codigo2 = calcular_codigo(x2, y2)

    if dentro:
        bresenham_linha(x1, y1, x2, y2, cor="red")  # Desenha linha recortada em verde

# Função para desenhar todas as linhas normalmente
def desenhar_linhas():
    canvas.delete("all")
    desenhar_malha()
    desenhar_janela_recorte()  # Desenha a janela de recorte
    for linha in linhas:
        x1, y1, x2, y2 = linha
        bresenham_linha(x1, y1, x2, y2, cor="black")  # Linhas originais em preto

# Função para aplicar o recorte e exibir apenas as linhas dentro da janela de recorte
def aplicar_recorte():
    canvas.delete("all")
    desenhar_malha()
    desenhar_janela_recorte()  # Desenha a janela de recorte
    for linha in linhas:
        x1, y1, x2, y2 = linha
        recorte_cohen_sutherland(x1, y1, x2, y2)

# Função para desenhar a janela de recorte na malha
def desenhar_janela_recorte():
    xmin, ymin, xmax, ymax = janela_recorte
    for x in range(xmin, xmax + 1):
        desenhar_pixel(x, ymin, "blue")
        desenhar_pixel(x, ymax, "blue")
    for y in range(ymin, ymax + 1):
        desenhar_pixel(xmin, y, "blue")
        desenhar_pixel(xmax, y, "blue")

# Função para desenhar a malha de fundo
def desenhar_malha():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x_start = i * CELL_SIZE
            y_start = j * CELL_SIZE
            canvas.create_rectangle(x_start, y_start, x_start + CELL_SIZE, y_start + CELL_SIZE, outline="gray")

# Função para adicionar uma linha
def adicionar_linha():
    try:
        # Obter os valores de entrada
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())

        # Validar os pontos inseridos
        if LIMITE_MIN < x1 < LIMITE_MAX and LIMITE_MIN < y1 < LIMITE_MAX and LIMITE_MIN < x2 < LIMITE_MAX and LIMITE_MIN < y2 < LIMITE_MAX:
            # Adicionar a linha à lista de linhas e desenhar
            linhas.append((x1, y1, x2, y2))
            desenhar_linhas()
            label_status.config(text=f"Linha ({x1}, {y1}) - ({x2}, {y2}) adicionada.")
        else:
            messagebox.showerror("Erro", f"As coordenadas devem estar entre {LIMITE_MIN} e {LIMITE_MAX}.")
    
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira todos os valores primeiro.")

# Função para redefinir a janela e as linhas
def resetar():
    global linhas
    linhas = []
    canvas.delete("all")
    desenhar_malha()
    desenhar_janela_recorte()
    label_status.config(text="Nenhuma linha adicionada.")

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Recorte de Linha - Algoritmo de Cohen-Sutherland")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=8, padx=10, pady=10)

# Desenhar a malha inicial e a janela de recorte
desenhar_malha()
desenhar_janela_recorte()

# Labels e Entradas para coordenadas da linha
label_x1 = tk.Label(janela, text=f"X1 ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x1.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_x1 = tk.Entry(janela)
entry_x1.grid(row=0, column=2, padx=10, pady=5)

label_y1 = tk.Label(janela, text=f"Y1 ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y1.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_y1 = tk.Entry(janela)
entry_y1.grid(row=1, column=2, padx=10, pady=5)

label_x2 = tk.Label(janela, text=f"X2 ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x2.grid(row=2, column=1, padx=10, pady=5, sticky="w")
entry_x2 = tk.Entry(janela)
entry_x2.grid(row=2, column=2, padx=10, pady=5)

label_y2 = tk.Label(janela, text=f"Y2 ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y2.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entry_y2 = tk.Entry(janela)
entry_y2.grid(row=3, column=2, padx=10, pady=5)

# Botão para adicionar linha
botao_adicionar_linha = tk.Button(janela, text="Adicionar Linha", command=adicionar_linha)
botao_adicionar_linha.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Botão para aplicar recorte
botao_aplicar_recorte = tk.Button(janela, text="Aplicar Recorte", command=aplicar_recorte)
botao_aplicar_recorte.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

# Botão para resetar a interface
botao_resetar = tk.Button(janela, text="Resetar", command=resetar)
botao_resetar.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

# Status
label_status = tk.Label(janela, text="Nenhuma linha adicionada.")
label_status.grid(row=7, column=1, columnspan=2)

# Executa a janela
janela.mainloop()