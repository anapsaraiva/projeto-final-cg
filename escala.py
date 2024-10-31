import tkinter as tk

# Definições da grade
GRID_SIZE = 22  # Número de células na grade (20x20)
CELL_SIZE = 20  # Tamanho de cada célula em pixels

# Função para desenhar um ponto na grade com preenchimento
def desenhar_ponto(x, y, cor="blue"):
    canvas.create_rectangle(
        round((x + GRID_SIZE // 2) * CELL_SIZE),
        round(((-y) + GRID_SIZE // 2) * CELL_SIZE),
        round((x + GRID_SIZE // 2) * CELL_SIZE + CELL_SIZE),
        round(((-y) + GRID_SIZE // 2) * CELL_SIZE + CELL_SIZE),
        fill=cor,
        outline=cor,
    )

# Função para desenhar uma linha usando o algoritmo de Bresenham
def desenhar_linha_bresenham(x1, y1, x2, y2, cor="blue"):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        desenhar_ponto(x1, y1, cor)  # Desenha o ponto com preenchimento

        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# Função para escalar um polígono em relação a um ponto fixo
def escalar_poligono(pontos, sx, sy, ponto_fixo):
    px, py = ponto_fixo
    novos_pontos = [
        (px + (x - px) * sx, py + (y - py) * sy) for x, y in pontos
    ]
    return novos_pontos

# Função para desenhar o polígono na grade usando Bresenham para cada aresta
def desenhar_poligono(pontos, cor="blue"):
    canvas.delete("all")
    desenhar_malha()
    for i in range(len(pontos)):
        x1, y1 = pontos[i]
        x2, y2 = pontos[(i + 1) % len(pontos)]
        desenhar_linha_bresenham(round(x1), round(y1), round(x2), round(y2), cor)

# Função para desenhar a malha de fundo
def desenhar_malha():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x_start = i * CELL_SIZE
            y_start = j * CELL_SIZE
            canvas.create_rectangle(x_start, y_start, x_start + CELL_SIZE, y_start + CELL_SIZE, outline="gray")

# Função para aplicar a transformação de escala e mostrar o resultado
def aplicar_escala():
    try:
        # Verificar se os campos estão preenchidos
        if not entry_sx.get() or not entry_sy.get() or not entry_fixo.get():
            raise ValueError("Por favor, insira valores válidos para os fatores de escala e o ponto fixo.")

        # Converte os valores de entrada para números
        sx = float(entry_sx.get())
        sy = float(entry_sy.get())
        ponto_fixo = tuple(map(float, entry_fixo.get().strip().split(",")))

        # Calcula o polígono escalado
        novos_pontos = escalar_poligono(pontos_poligono, sx, sy, ponto_fixo)

        # Desenha o polígono escalado
        desenhar_poligono(novos_pontos)

    except ValueError as e:
        print(f"Erro: {e}")

# Função para coletar os pontos do polígono a partir das entradas do usuário
def coletar_pontos():
    try:
        pontos = []
        pontos_texto = entry_pontos.get().split(";")
        for ponto in pontos_texto:
            x, y = map(float, ponto.strip().split(","))
            pontos.append((x, y))

        global pontos_poligono
        pontos_poligono = pontos

        # Desenha o polígono inicial
        desenhar_poligono(pontos)

    except ValueError:
        print("Erro: Insira coordenadas válidas no formato x1,y1; x2,y2; ...")

# Função para resetar o estado do aplicativo
def resetar():
    global pontos_poligono
    pontos_poligono = []  # Limpa os pontos do polígono
    canvas.delete("all")  # Limpa o canvas
    desenhar_malha()  # Redesenha a malha
    entry_pontos.delete(0, tk.END)  # Limpa a entrada de pontos
    entry_sx.delete(0, tk.END)  # Limpa a entrada de fator de escala X
    entry_sy.delete(0, tk.END)  # Limpa a entrada de fator de escala Y
    entry_fixo.delete(0, tk.END)  # Limpa a entrada de ponto fixo

# Configuração inicial do polígono (triângulo padrão)
pontos_poligono = []

# Interface Gráfica
root = tk.Tk()
root.title("Escala de Polígono")

# Configurando o layout principal com um Frame para grade e controles
frame_principal = tk.Frame(root)
frame_principal.pack()

# Canvas para desenhar (à esquerda)
canvas = tk.Canvas(frame_principal, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.grid(row=0, column=0, padx=10, pady=10)

# Desenha a malha inicial
desenhar_malha()

# Frame para controle da escala (à direita do canvas)
frame_controle = tk.Frame(frame_principal)
frame_controle.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Entrada para os pontos do polígono
tk.Label(frame_controle, text="Coordenadas do Polígono (x,y):").grid(row=0, column=0, pady=5, sticky="w")
entry_pontos = tk.Entry(frame_controle, width=30)
entry_pontos.grid(row=1, column=0, pady=5, columnspan=2)
tk.Label(frame_controle, text="Exemplo: 0,0; 5,0; 2,5").grid(row=2, column=0, columnspan=2, pady=5)
btn_desenhar = tk.Button(frame_controle, text="Desenhar Polígono", command=coletar_pontos)
btn_desenhar.grid(row=3, column=0, columnspan=2, pady=10)

# Inputs para a escala
tk.Label(frame_controle, text="Fator de Escala X:").grid(row=4, column=0, pady=5, sticky="w")
entry_sx = tk.Entry(frame_controle, width=10)
entry_sx.grid(row=4, column=1, pady=5)

tk.Label(frame_controle, text="Fator de Escala Y:").grid(row=5, column=0, pady=5, sticky="w")
entry_sy = tk.Entry(frame_controle, width=10)
entry_sy.grid(row=5, column=1, pady=5)

tk.Label(frame_controle, text="Ponto Fixo (x,y):").grid(row=6, column=0, pady=5, sticky="w")
entry_fixo = tk.Entry(frame_controle, width=20)
entry_fixo.grid(row=6, column=1, pady=5)

btn_escalar = tk.Button(frame_controle, text="Escalar Polígono", command=aplicar_escala)
btn_escalar.grid(row=7, column=0, columnspan=2, pady=10)

# Botão para resetar
btn_resetar = tk.Button(frame_controle, text="Resetar", command=resetar)
btn_resetar.grid(row=8, column=0, columnspan=2, pady=10)

# Iniciar o loop da interface gráfica
root.mainloop()