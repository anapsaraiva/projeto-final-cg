import tkinter as tk
import tkinter.messagebox as messagebox

# Definições do tamanho da malha
GRID_SIZE = 22  # Número de células na grade (20x20)
CELL_SIZE = 20  # Tamanho de cada célula em pixels
LIMITE_MIN = -11
LIMITE_MAX = 11

# Lista de pontos do polígono inseridos
pontos_poligono = []
pixeis_borda = set()

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

# Função para preencher o polígono usando o algoritmo de varredura (Scanline Fill)
def preenchimento_varredura():
    if not pontos_poligono:
        messagebox.showerror("Erro", "Por favor, adicione pontos ao polígono antes de iniciar o preenchimento.")
        return

    # Encontre os valores máximo e mínimo de Y no polígono
    y_min = min(p[1] for p in pontos_poligono)
    y_max = max(p[1] for p in pontos_poligono)

    # Varra cada linha (scanline) no intervalo de Y do polígono
    for y in range(y_min, y_max + 1):
        intersecoes = []
        
        # Encontrar as interseções do polígono com a linha horizontal y
        for i in range(len(pontos_poligono)):
            x1, y1 = pontos_poligono[i]
            x2, y2 = pontos_poligono[(i + 1) % len(pontos_poligono)]  # Próximo ponto
            
            # Verifica se a linha cruza a scanline
            if y1 != y2:  # Ignorar arestas horizontais
                if y1 < y2:
                    y_inferior, y_superior = y1, y2
                    x_inferior, x_superior = x1, x2
                else:
                    y_inferior, y_superior = y2, y1
                    x_inferior, x_superior = x2, x1
                
                # A scanline cruza o segmento?
                if y_inferior <= y < y_superior:  # Ignora o ponto final superior para evitar duplicação
                    # Interseção com a scanline usando interpolação linear
                    x_intersecao = x_inferior + (y - y_inferior) * (x_superior - x_inferior) / (y_superior - y_inferior)
                    intersecoes.append(int(x_intersecao))

        # Ordenar as interseções por ordem crescente
        intersecoes.sort()

        # Preencher os pixels entre pares de interseções
        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                for x in range(intersecoes[i], intersecoes[i + 1]):
                    if (x, y) not in pixeis_borda:  # Evitar preencher bordas
                        desenhar_pixel(x, y, "red")

# Função para desenhar a malha de fundo
def desenhar_malha():
    # Limpar todo o canvas
    canvas.delete("all")
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x_start = i * CELL_SIZE
            y_start = j * CELL_SIZE
            canvas.create_rectangle(x_start, y_start, x_start + CELL_SIZE, y_start + CELL_SIZE, outline="gray")

# Função para adicionar pontos ao polígono
def adicionar_ponto_poligono():
    try:
        # Obter os valores de entrada
        x = int(entry_x.get())
        y = int(entry_y.get())

        # Validar o ponto inserido
        if LIMITE_MIN < x < LIMITE_MAX and LIMITE_MIN < y < LIMITE_MAX:
            # Adicionar o ponto à lista de pontos do polígono
            pontos_poligono.append((x, y))
            label_status.config(text=f"Ponto ({x}, {y}) adicionado. Total de pontos: {len(pontos_poligono)}")
        else:
            messagebox.showerror("Erro", f"As coordenadas devem estar entre {LIMITE_MIN} e {LIMITE_MAX}.")
    
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

# Função para desenhar o polígono após adicionar os pontos
def desenhar_poligono():
    if len(pontos_poligono) > 2:
        desenhar_poligono_na_malha(pontos_poligono)
    else:
        messagebox.showerror("Erro", "O polígono requer pelo menos 3 pontos.")

# Função para resetar o desenho e os pontos
def resetar_poligono():
    global pontos_poligono, pixeis_borda
    pontos_poligono = []
    pixeis_borda = set()
    
    # Limpar a interface gráfica e reiniciar o estado
    desenhar_malha()
    label_status.config(text="Nenhum ponto adicionado.")

# Configuração da Interface Gráfica com Tkinter
janela = tk.Tk()
janela.title("Preenchimento com Algoritmo de Varredura - Malha de Pixels")

# Criação do Canvas para desenhar a malha
canvas = tk.Canvas(janela, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

# Desenhar a malha inicial
desenhar_malha()

# Label e Campo de entrada para adicionar pontos do polígono (X, Y)
label_x = tk.Label(janela, text=f"Coordenada X ({LIMITE_MIN} < x < {LIMITE_MAX}):")
label_x.grid(row=0, column=1, padx=10, pady=5, sticky="w")
entry_x = tk.Entry(janela)
entry_x.grid(row=0, column=2, padx=10, pady=5)

label_y = tk.Label(janela, text=f"Coordenada Y ({LIMITE_MIN} < y < {LIMITE_MAX}):")
label_y.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entry_y = tk.Entry(janela)
entry_y.grid(row=1, column=2, padx=10, pady=5)

# Botão para adicionar pontos ao polígono
botao_adicionar_ponto = tk.Button(janela, text="Adicionar Ponto", command=adicionar_ponto_poligono)
botao_adicionar_ponto.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# Botão para desenhar o polígono
botao_desenhar_poligono = tk.Button(janela, text="Desenhar Polígono", command=desenhar_poligono)
botao_desenhar_poligono.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Botão para iniciar o preenchimento usando varredura
botao_preenchimento_varredura = tk.Button(janela, text="Preencher (Varredura)", command=preenchimento_varredura)
botao_preenchimento_varredura.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Botão para resetar o polígono e a malha
botao_resetar = tk.Button(janela, text="Resetar", command=resetar_poligono)
botao_resetar.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

# Status
label_status = tk.Label(janela, text="Nenhum ponto adicionado.")
label_status.grid(row=6, column=1, columnspan=2)

# Executa a janela
janela.mainloop()