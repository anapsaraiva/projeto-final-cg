import tkinter as tk
import tkinter.messagebox as messagebox

# Definições do tamanho da malha
GRID_SIZE = 20  # Número de células na grade (20x20)
CELL_SIZE = 30  # Tamanho de cada célula em pixels
LIMITE_MIN = -11
LIMITE_MAX = 11

# Variável para armazenar os pixels preenchidos
pixeis_preenchidos = set()
pixeis_borda = set()

# Padrão de um polígono já desenhado (um polígono irregular qualquer)
pontos_poligono = [
    (-5, -5), (5, -5), (6, 0), (2, 5), (-3, 6), (-7, 1)
]

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

# Função para desenhar o polígono na malha de pixels
def desenhar_poligono_na_malha(pontos):
    global pixeis_borda
    pixeis_borda = set()

    # Desenha cada linha do polígono
    for (x1, y1), (x2, y2) in zip(pontos[:-1], pontos[1:]):
        linha = bresenham_linha(x1, y1, x2, y2)
        for (x, y) in linha:
            desenhar_pixel(x, y, "blue")
            pixeis_borda.add((x, y))  # Armazena o pixel como parte da borda

    # Conecta o último ponto ao primeiro para fechar o polígono
    x1, y1 = pontos[-1]
    x2, y2 = pontos[0]
    linha = bresenham_linha(x1, y1, x2, y2)
    for (x, y) in linha:
        desenhar_pixel(x, y, "blue")
        pixeis_borda.add((x, y))  # Armazena o pixel como parte da borda

# Função para desenhar um pixel na malha
def desenhar_pixel(x, y, cor):
    x_canvas = (x + GRID_SIZE // 2) * CELL_SIZE
    y_canvas = ((-y) + GRID_SIZE // 2) * CELL_SIZE  # Inverte o valor de Y
    canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill=cor)

# Função de preenchimento recursivo (flood fill)
def preenchimento_recursivo(x, y):
    # Se o pixel já foi preenchido ou está fora dos limites, interrompe
    if (x, y) in pixeis_preenchidos or (x, y) in pixeis_borda:
        return
    if not (LIMITE_MIN < x < LIMITE_MAX and LIMITE_MIN < y < LIMITE_MAX):
        return

    # Preenche o pixel atual
    desenhar_pixel(x, y, "red")
    pixeis_preenchidos.add((x, y))

    # Recursivamente chama para os vizinhos
    preenchimento_recursivo(x + 1, y)  # Direita
    preenchimento_recursivo(x - 1, y)  # Esquerda
    preenchimento_recursivo(x, y + 1)  # Acima
    preenchimento_recursivo(x, y - 1)  # Abaixo

# Função para desenhar a malha de fundo
def desenhar_malha():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x_start = i * CELL_SIZE
            y_start = j * CELL_SIZE
            canvas.create_rectangle(x_start, y_start, x_start + CELL_SIZE, y_start + CELL_SIZE, outline="gray")

# Função para desenhar o polígono ao iniciar o programa
def desenhar_poligono_inicial():
    desenhar_poligono_na_malha(pontos_poligono)

# Função para iniciar o preenchimento
def iniciar_preenchimento():
    try:
        # Obter os valores de entrada para o ponto de preenchimento
        x = int(entry_x_fill.get())
        y = int(entry_y_fill.get())

        # Validar o ponto de preenchimento
        if LIMITE_MIN < x < LIMITE_MAX and LIMITE_MIN < y < LIMITE_MAX:
            preenchimento_recursivo(x, y)
        else:
            messagebox.showerror("Erro", f"As coordenadas devem estar entre {LIMITE_MIN} e {LIMITE_MAX}.")
    
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Função para resetar a tela e os preenchimentos
def resetar_preenchimento():
    global pixeis_preenchidos
    pixeis_preenchidos = set()
    desenhar_malha()
    desenhar_poligono_inicial()  # Redesenha o polígono inicial

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Preenchimento Recursivo - Malha de Pixels")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

# Desenhar a malha inicial
desenhar_malha()

# Desenhar o polígono inicial ao iniciar o programa
desenhar_poligono_inicial()

# Label e Campo de entrada para o ponto de preenchimento (X, Y)
label_x_fill = tk.Label(janela, text=f"Ponto de Preenchimento X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x_fill.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_x_fill = tk.Entry(janela)
entry_x_fill.grid(row=0, column=2, padx=10, pady=5)

label_y_fill = tk.Label(janela, text=f"Ponto de Preenchimento Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y_fill.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_y_fill = tk.Entry(janela)
entry_y_fill.grid(row=1, column=2, padx=10, pady=5)

# Botão para iniciar o preenchimento
botao_preenchimento = tk.Button(janela, text="Iniciar Preenchimento", command=iniciar_preenchimento)
botao_preenchimento.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Botão para resetar
botao_resetar = tk.Button(janela, text="Resetar", command=resetar_preenchimento)
botao_resetar.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Executa a janela
janela.mainloop()