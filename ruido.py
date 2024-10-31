import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

class ConversorImagem:
    def __init__(self, root):
        self.root = root
        self.root.title("Remoção de Ruído em Imagem")
        
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

        # Opção de filtro para remoção de ruído
        tk.Label(self.control_frame, text="Filtro:").grid(row=1, column=0, pady=5, sticky="w")
        self.filter_var = tk.StringVar()
        self.filter_options = ["Média", "Mediana", "Gaussiano"]
        self.filter_menu = ttk.Combobox(self.control_frame, textvariable=self.filter_var, values=self.filter_options)
        self.filter_menu.grid(row=1, column=1, pady=5)

        # Botão de aplicação de filtro
        self.apply_button = tk.Button(self.control_frame, text="Aplicar Remoção de Ruído", command=self.aplicar_filtro)
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
        
        # Converte a imagem do PIL para o formato do OpenCV
        img_cv = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
        
        # Aplicação do filtro de remoção de ruído
        if self.filter_var.get() == "Média":
            img_cv = cv2.blur(img_cv, (5, 5))
        elif self.filter_var.get() == "Mediana":
            img_cv = cv2.medianBlur(img_cv, 5)
        elif self.filter_var.get() == "Gaussiano":
            img_cv = cv2.GaussianBlur(img_cv, (5, 5), 0)

        # Conversão da imagem processada para o formato do PIL para exibição
        img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        self.display_image(img_pil)  # Exibe a imagem processada

# Inicializa a interface gráfica
root = tk.Tk()
app = ConversorImagem(root)
root.mainloop()