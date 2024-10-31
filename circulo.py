import tkinter as tk

# Definições do tamanho da malha
GRID_SIZE = 22  # Número de células na grade (20x20)
CELL_SIZE = 20  # Tamanho de cada célula em pixels
LIMITE_MIN = -11
LIMITE_MAX = 11

# Função para desenhar um círculo usando o Algoritmo de Bresenham
def bresenham_circulo(centro_x, centro_y, raio):
    pontos = []
    x = 0
    y = raio
    d = 3 - 2 * raio

    # Adiciona os pontos simétricos para o círculo
    while y >= x:
        pontos.extend([
            (centro_x + x, centro_y + y), (centro_x - x, centro_y + y),
            (centro_x + x, centro_y - y), (centro_x - x, centro_y - y),
            (centro_x + y, centro_y + x), (centro_x - y, centro_y + x),
            (centro_x + y, centro_y - x), (centro_x - y, centro_y - x)
        ])
        if d <= 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1
    
    return pontos

# Função para desenhar o círculo e o "raio" (um único pixel no centro) na malha de pixels
def desenhar_circulo_na_malha(pontos_circulo, centro_x, centro_y):
    # Limpa a grade antes de desenhar
    canvas.delete("all")
    desenhar_malha()

    # Desenha cada ponto do círculo colorindo as células da malha em azul
    for (x, y) in pontos_circulo:
        x_canvas = (x + GRID_SIZE // 2) * CELL_SIZE
        y_canvas = ((-y) + GRID_SIZE // 2) * CELL_SIZE  # Inverte o valor de Y
        canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill="blue")

    # Desenha o centro do círculo (representando o "raio") em roxo
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

# Função para validar as coordenadas
def validar_dados(centro_x, centro_y, raio):
    if (LIMITE_MIN < centro_x < LIMITE_MAX and LIMITE_MIN < centro_y < LIMITE_MAX and
        raio > 0 and raio <= 11):
        return True
    else:
        return False

# Função para capturar os dados da interface e executar o algoritmo
def executar_circulo():
    try:
        # Obter os valores de entrada
        centro_x = int(entry_centro_x.get())
        centro_y = int(entry_centro_y.get())
        raio = int(entry_raio.get())
        
        # Validar os valores de entrada
        if validar_dados(centro_x, centro_y, raio):
            # Executa o algoritmo para desenhar o círculo
            pontos_circulo = bresenham_circulo(centro_x, centro_y, raio)

            # Desenha o círculo e o pixel representando o centro (raio)
            desenhar_circulo_na_malha(pontos_circulo, centro_x, centro_y)
        else:
            tk.messagebox.showerror("Erro", f"As coordenadas devem estar entre {LIMITE_MIN} e {LIMITE_MAX}, e o raio deve ser maior que 0 e menor ou igual a 11.")
    
    except ValueError:
        tk.messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Algoritmo de Bresenham para Círculos - Malha de Pixels")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

# Desenhar a malha inicial
desenhar_malha()

# Label e Campo de entrada para o centro do círculo (Centro X, Centro Y)
label_centro_x = tk.Label(janela, text=f"Centro X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_centro_x.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_centro_x = tk.Entry(janela)
entry_centro_x.grid(row=0, column=2, padx=10, pady=5)

label_centro_y = tk.Label(janela, text=f"Centro Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_centro_y.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_centro_y = tk.Entry(janela)
entry_centro_y.grid(row=1, column=2, padx=10, pady=5)

# Label e Campo de entrada para o raio do círculo
label_raio = tk.Label(janela, text="Raio (0 < r <= 11):")
label_raio.grid(row=2, column=1, padx=10, pady=5, sticky="w")
entry_raio = tk.Entry(janela)
entry_raio.grid(row=2, column=2, padx=10, pady=5)

# Botão para executar o algoritmo de Bresenham para Círculos
botao_executar = tk.Button(janela, text="Desenhar Círculo", command=executar_circulo)
botao_executar.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Executa a janela
janela.mainloop()
