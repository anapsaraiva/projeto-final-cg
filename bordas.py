import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

class ConversorImagem:
    def __init__(self, root):
        self.root = root
        self.root.title("Detecção de Bordas em Imagem")
        
        # Configurações de imagem e parâmetros
        self.image = None
        self.image_display = None

        # Interface do lado esquerdo para exibir a imagem
        self.image_label = tk.Label(self.root)
        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        # Interface do lado direito para parâmetros e controle
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        
        # Botão de carregamento de imagem
        self.load_button = tk.Button(self.control_frame, text="Carregar Imagem", command=self.carregar_imagem)
        self.load_button.grid(row=0, column=0, columnspan=2, pady=5)

        # Opção de filtro para detecção de borda
        tk.Label(self.control_frame, text="Filtro de Detecção de Bordas:").grid(row=1, column=0, pady=5, sticky="w")
        self.edge_var = tk.StringVar()
        self.edge_options = ["Sobel", "Prewitt", "Canny"]
        self.edge_menu = ttk.Combobox(self.control_frame, textvariable=self.edge_var, values=self.edge_options)
        self.edge_menu.grid(row=1, column=1, pady=5)

        # Botão de aplicação de filtro
        self.apply_button = tk.Button(self.control_frame, text="Aplicar Detecção de Bordas", command=self.aplicar_filtro)
        self.apply_button.grid(row=2, column=0, columnspan=2, pady=10)

    def carregar_imagem(self):
        # Seleciona a imagem e a exibe na interface
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if filepath:
            self.image = Image.open(filepath)
            self.display_image(self.image)

    def display_image(self, img):
        # Redimensiona a imagem para exibição na interface
        img = img.resize((250, 250))
        self.image_display = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.image_display)
    
    def aplicar_filtro(self):
        if self.image is None:
            tk.messagebox.showerror("Erro", "Carregue uma imagem primeiro!")
            return
        
        # Converte a imagem do PIL para o formato do OpenCV e para tons de cinza
        img_cv = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2GRAY)
        
        # Aplicação do filtro de detecção de bordas
        if self.edge_var.get() == "Sobel":
            sobelx = cv2.Sobel(img_cv, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(img_cv, cv2.CV_64F, 0, 1, ksize=3)
            img_edges = cv2.magnitude(sobelx, sobely)
            img_edges = np.uint8(np.absolute(img_edges))  # Converte para uint8 para exibir
        elif self.edge_var.get() == "Prewitt":
            # Aplica o filtro Prewitt nas direções x e y
            kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
            kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
            prewittx = cv2.filter2D(img_cv, cv2.CV_32F, kernelx)
            prewitty = cv2.filter2D(img_cv, cv2.CV_32F, kernely)
            img_edges = cv2.magnitude(prewittx, prewitty)
            img_edges = np.uint8(np.absolute(img_edges))  # Converte para uint8 para exibir
        elif self.edge_var.get() == "Canny":
            img_edges = cv2.Canny(img_cv, 100, 200)  # Limiar inferior e superior para o Canny

        # Conversão da imagem processada para o formato do PIL para exibição
        img_pil = Image.fromarray(img_edges)
        self.display_image(img_pil)  # Exibe a imagem processada

# Inicializa a interface gráfica
root = tk.Tk()
app = ConversorImagem(root)
root.mainloop()