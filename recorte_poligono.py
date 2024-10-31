import tkinter as tk
import tkinter.messagebox as messagebox

# Definições do tamanho da malha
GRID_SIZE = 22  # Número de células na grade (20x20)
CELL_SIZE = 20  # Tamanho de cada célula em pixels
LIMITE_MIN = -11
LIMITE_MAX = 11

# Variáveis para armazenar pontos do polígono atual e a janela de recorte
pontos_poligono = []
janela_recorte = (-5, -5, 5, 5)  # (xmin, ymin, xmax, ymax)

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

# Função para desenhar o polígono na malha de pixels
def desenhar_poligono_na_malha(pontos, cor="black"):
    for i in range(len(pontos)):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % len(pontos)]
        bresenham_linha(x1, y1, x2, y2, cor)

# Função para calcular a interseção entre uma aresta do polígono e uma borda de recorte
def calcular_interseccao(ponto1, ponto2, borda):
    x1, y1 = ponto1
    x2, y2 = ponto2
    xmin, ymin, xmax, ymax = janela_recorte
    x, y = 0, 0

    if borda == "esquerda":
        y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
        x = xmin
    elif borda == "direita":
        y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
        x = xmax
    elif borda == "inferior":
        x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
        y = ymin
    elif borda == "superior":
        x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
        y = ymax

    return (int(x), int(y))

# Função para verificar se um ponto está dentro da janela de recorte
def dentro_janela(ponto, borda):
    x, y = ponto
    xmin, ymin, xmax, ymax = janela_recorte
    if borda == "esquerda":
        return x >= xmin
    elif borda == "direita":
        return x <= xmax
    elif borda == "inferior":
        return y >= ymin
    elif borda == "superior":
        return y <= ymax

# Função para recortar o polígono usando o algoritmo de Sutherland-Hodgman
def recorte_poligono(poligono):
    bordas = ["esquerda", "direita", "inferior", "superior"]
    for borda in bordas:
        novo_poligono = []
        for i in range(len(poligono)):
            ponto1 = poligono[i]
            ponto2 = poligono[(i + 1) % len(poligono)]
            dentro1 = dentro_janela(ponto1, borda)
            dentro2 = dentro_janela(ponto2, borda)

            if dentro1 and dentro2:
                novo_poligono.append(ponto2)
            elif dentro1 and not dentro2:
                intersecao = calcular_interseccao(ponto1, ponto2, borda)
                novo_poligono.append(intersecao)
            elif not dentro1 and dentro2:
                intersecao = calcular_interseccao(ponto1, ponto2, borda)
                novo_poligono.append(intersecao)
                novo_poligono.append(ponto2)

        poligono = novo_poligono

    return poligono

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

# Função para adicionar pontos ao polígono
def adicionar_ponto():
    try:
        x = int(entry_x.get())
        y = int(entry_y.get())

        # Validar o ponto inserido
        if LIMITE_MIN < x < LIMITE_MAX and LIMITE_MIN < y < LIMITE_MAX:
            pontos_poligono.append((x, y))
            label_status.config(text=f"Ponto ({x}, {y}) adicionado. Total de pontos: {len(pontos_poligono)}")
        else:
            messagebox.showerror("Erro", f"As coordenadas devem estar entre {LIMITE_MIN} e {LIMITE_MAX}.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Função para desenhar o polígono
def desenhar_poligono():
    if len(pontos_poligono) > 2:
        desenhar_poligono_na_malha(pontos_poligono, cor="black")
    else:
        messagebox.showerror("Erro", "O polígono requer pelo menos 3 pontos.")

# Função para aplicar o recorte e desenhar apenas o polígono recortado
def aplicar_recorte():
    canvas.delete("all")  # Limpa a tela
    desenhar_malha()  # Redesenha apenas a malha
    if len(pontos_poligono) > 2:
        poligono_recortado = recorte_poligono(pontos_poligono)
        desenhar_poligono_na_malha(poligono_recortado, cor="green")  # Desenha o polígono recortado em verde
    else:
        messagebox.showerror("Erro", "O polígono requer pelo menos 3 pontos para aplicar o recorte.")

# Função para redefinir a janela e os pontos do polígono
def resetar():
    global pontos_poligono
    pontos_poligono = []  # Limpa a lista de pontos do polígono
    canvas.delete("all")  # Limpa completamente o canvas
    desenhar_malha()  # Redesenha a malha inicial
    desenhar_janela_recorte()  # Redesenha a janela de recorte
    label_status.config(text="Nenhum ponto adicionado.")  # Atualiza o status

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Recorte de Polígono - Algoritmo de Sutherland-Hodgman")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=8, padx=10, pady=10)

# Desenhar a malha inicial e a janela de recorte
desenhar_malha()
desenhar_janela_recorte()

# Labels e Entradas para coordenadas dos pontos do polígono
label_x = tk.Label(janela, text=f"Coordenada X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_x = tk.Entry(janela)
entry_x.grid(row=0, column=2, padx=10, pady=5)

label_y = tk.Label(janela, text=f"Coordenada Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_y = tk.Entry(janela)
entry_y.grid(row=1, column=2, padx=10, pady=5)

# Botão para adicionar pontos ao polígono
botao_adicionar_ponto = tk.Button(janela, text="Adicionar Ponto", command=adicionar_ponto)
botao_adicionar_ponto.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Botão para desenhar o polígono
botao_desenhar_poligono = tk.Button(janela, text="Desenhar Polígono", command=desenhar_poligono)
botao_desenhar_poligono.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Botão para aplicar recorte
botao_aplicar_recorte = tk.Button(janela, text="Aplicar Recorte", command=aplicar_recorte)
botao_aplicar_recorte.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Botão para resetar a interface
botao_resetar = tk.Button(janela, text="Resetar", command=resetar)
botao_resetar.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

# Status
label_status = tk.Label(janela, text="Nenhum ponto adicionado.")
label_status.grid(row=6, column=1, columnspan=2)

# Executa a janela
janela.mainloop()