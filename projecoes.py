import tkinter as tk

# Configuração da grade e da interface
GRID_SIZE = 22
CELL_SIZE = 20

# Função para projeção ortogonal frontal (descarta o eixo X)
def projecao_ortogonal(x, y, z):
    return y, z

# Função para projeção oblíqua com um fator de inclinação
def projecao_obliqua(x, y, z, alfa=0.5):
    return y + alfa * x, z + alfa * x

# Função para projeção de perspectiva
def projecao_perspectiva(x, y, z, d=5):
    if z + d == 0:  # Para evitar divisão por zero
        return x, y
    return (d * x) / (z + d), (d * y) / (z + d)

# Função para desenhar um ponto na grade
def desenhar_ponto(x, y, cor="blue"):
    x_canvas = (x + GRID_SIZE // 2) * CELL_SIZE
    y_canvas = (GRID_SIZE // 2 - y) * CELL_SIZE
    canvas.create_rectangle(x_canvas, y_canvas, x_canvas + CELL_SIZE, y_canvas + CELL_SIZE, fill=cor, outline="")

# Função para rasterizar uma linha usando o algoritmo de Bresenham
def desenhar_linha_bresenham(x1, y1, x2, y2, cor="blue"):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        desenhar_ponto(x1, y1, cor)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# Função para desenhar o sólido usando a projeção selecionada e Bresenham
def desenhar_solido(vertices, cor="blue"):
    # Conecta os vértices projetados para criar as arestas do objeto
    arestas = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Base inferior
        (4, 5), (5, 6), (6, 7), (7, 4),  # Base superior
        (0, 4), (1, 5), (2, 6), (3, 7)   # Conexões entre as bases
    ]

    # Verifica o tipo de projeção selecionada
    if projecao_var.get() == "Ortogonal":
        vertices_proj = [projecao_ortogonal(*v) for v in vertices]
    elif projecao_var.get() == "Oblíqua":
        vertices_proj = [projecao_obliqua(*v) for v in vertices]
    else:  # Projeção de Perspectiva
        vertices_proj = [projecao_perspectiva(*v) for v in vertices]

    # Rasterizar as linhas usando Bresenham
    for v1, v2 in arestas:
        x1, y1 = vertices_proj[v1]
        x2, y2 = vertices_proj[v2]
        desenhar_linha_bresenham(int(x1), int(y1), int(x2), int(y2), cor)

# Função para coletar os pontos do sólido
def coletar_pontos():
    try:
        vertices = []
        vertices_texto = entry_vertices.get().split(";")
        for vertice in vertices_texto:
            x, y, z = map(int, vertice.strip().split(","))
            vertices.append((x, y, z))

        # Limpa a tela e desenha o sólido com a projeção selecionada
        canvas.delete("all")
        desenhar_malha()
        desenhar_solido(vertices)

    except ValueError:
        print("Erro: Insira coordenadas válidas no formato x,y,z; x2,y2,z2; ...")

# Função para desenhar a malha de fundo
def desenhar_malha():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x_start = i * CELL_SIZE
            y_start = j * CELL_SIZE
            canvas.create_rectangle(x_start, y_start, x_start + CELL_SIZE, y_start + CELL_SIZE, outline="lightgray")

# Interface gráfica
root = tk.Tk()
root.title("Projeção de Sólido 3D e Rasterização")

frame_principal = tk.Frame(root)
frame_principal.pack()

canvas = tk.Canvas(frame_principal, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.grid(row=0, column=0, padx=10, pady=10)
desenhar_malha()

frame_controle = tk.Frame(frame_principal)
frame_controle.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Menu de seleção para escolher a projeção
projecao_var = tk.StringVar(value="Ortogonal")
tk.Label(frame_controle, text="Escolha a Projeção:").grid(row=0, column=0, pady=5, sticky="w")
select_projecao = tk.OptionMenu(frame_controle, projecao_var, "Ortogonal", "Oblíqua", "Perspectiva")
select_projecao.grid(row=1, column=0, pady=5, sticky="w")

# Entrada para os vértices do sólido
tk.Label(frame_controle, text="Vértices do Sólido (x,y,z):").grid(row=2, column=0, pady=5, sticky="w")
entry_vertices = tk.Entry(frame_controle, width=30)
entry_vertices.grid(row=3, column=0, pady=5, columnspan=2)
tk.Label(frame_controle, text="Exemplo: 0,0,0; 5,0,0; 5,5,0; 0,5,0; 0,0,5; 5,0,5; 5,5,5; 0,5,5").grid(row=4, column=0, columnspan=2, pady=5)

# Botão "Aplicar Projeção"
btn_desenhar = tk.Button(frame_controle, text="Aplicar Projeção", command=coletar_pontos)
btn_desenhar.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()