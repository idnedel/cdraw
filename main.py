import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CDraw")

        self.create_layout()

        self.original_image = None
        self.transformed_image = None
        self.transformed_image_copy = None

        # Tela cheia ao abrir
        root.state('zoomed')  
    
        
    def create_layout(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # Divida a tela em duas metades com uma borda fina entre elas
        self.original_frame = tk.Frame(self.frame, borderwidth=1, relief="solid")
        self.original_frame.pack(side="left", fill="both", expand=True)

        self.transformed_frame = tk.Frame(self.frame, borderwidth=1, relief="solid")
        self.transformed_frame.pack(side="left", fill="both", expand=True)

        self.original_image_label = tk.Label(self.original_frame)
        self.original_image_label.pack(fill="both", expand=True)

        self.transformed_image_label = tk.Label(self.transformed_frame)
        self.transformed_image_label.pack(fill="both", expand=True)

        self.create_menus()

    def create_menus(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Abrir imagem", command=self.open_image)
        file_menu.add_command(label="Salvar imagem", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Sobre", command=self.show_about)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        geometric_menu = tk.Menu(menubar, tearoff=0)
        geometric_menu.add_command(label="Transladar", command=self.translate_image)
        geometric_menu.add_command(label="Rotacionar", command=self.rotate_image)
        geometric_menu.add_command(label="Espelhar", command=self.mirror_image)
        geometric_menu.add_command(label="Aumentar", command=self.enlarge_image)
        geometric_menu.add_command(label="Diminuir", command=self.reduce_image)
        menubar.add_cascade(label="Transformações Geométricas", menu=geometric_menu)
        
        filters_menu = tk.Menu(menubar, tearoff=0)
        filters_menu.add_command(label="Grayscale", command=self.apply_grayscale)
        
        # Submenu para "Passa Baixa"
        passa_baixa_menu = tk.Menu(filters_menu, tearoff=0)
        passa_baixa_menu.add_command(label="Média", command=lambda: self.apply_low_pass("Média"))
        passa_baixa_menu.add_command(label="Moda", command=lambda: self.apply_low_pass("Moda"))
        passa_baixa_menu.add_command(label="Mediana", command=lambda: self.apply_low_pass("Mediana"))
        passa_baixa_menu.add_command(label="Gauss", command=lambda: self.apply_low_pass("Gauss"))
        
        filters_menu.add_cascade(label="Passa Baixa", menu=passa_baixa_menu)
        filters_menu.add_command(label="Passa Alta", command=self.apply_high_pass)
        filters_menu.add_command(label="Threshold", command=self.apply_threshold)
        menubar.add_cascade(label="Filtros", menu=filters_menu)

        morphology_menu = tk.Menu(menubar, tearoff=0)
        morphology_menu.add_command(label="Dilatação", command=self.apply_dilation)
        morphology_menu.add_command(label="Erosão", command=self.apply_erosion)
        morphology_menu.add_command(label="Abertura", command=self.apply_opening)
        morphology_menu.add_command(label="Fechamento", command=self.apply_closing)
        menubar.add_cascade(label="Morfologia Matemática", menu=morphology_menu)
        
        features_menu = tk.Menu(menubar, tearoff=0)
        features_menu.add_command(label="Desafio", command=self.challenge_feature)
        menubar.add_cascade(label="Extração de Características", menu=features_menu)

        remove_filter = tk.Menu(menubar, tearoff=0)
        remove_filter.add_command(label="Restaurar", command=self.remove_all_filters)
        menubar.add_cascade(label="Restaurar Imagem", menu=remove_filter)
        
        self.root.config(menu=menubar)

    # Funções dos botões    
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)

            # Cria cópia da imagem para aplicar os filtros
            self.transformed_image_copy = self.original_image.copy()
            
            # Dimensionar a imagem
            max_display_width = 600

            # original
            scale_factor = max_display_width / self.original_image.shape[1]
            self.original_image = cv2.resize(self.original_image, (max_display_width, int(self.original_image.shape[0] * scale_factor)))
            
            # copia
            scale_factor = max_display_width / self.transformed_image_copy.shape[1]
            self.transformed_image_copy = cv2.resize(self.transformed_image_copy, (max_display_width, int(self.transformed_image_copy.shape[0] * scale_factor)))
            
            self.display_image(self.original_image, self.original_image_label)
            self.display_image(self.transformed_image_copy, self.transformed_image_label)

    def save_image(self):
        if self.transformed_image_copy is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                cv2.imwrite(file_path, self.transformed_image_copy)
                messagebox.showinfo("Info", "Imagem salva com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem transformada para salvar.")
    
    def show_about(self):
        messagebox.showinfo("Sobre", "CDraw - Ciência da Computação\nProcessamento Digital de Imagens\nCriado Por Matheus Nedel e Nícolas Dapper")
    
    def display_image(self, image, label_widget):
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            label_widget.config(image=photo)
            label_widget.image = photo
        else:
            label_widget.config(image=None)
    
    # transladar - não sei se isso aqui ta certo
    def translate_image(self):
        if self.transformed_image_copy is not None:
        # Cria a janela de dialogo
            dialog = tk.Toplevel(self.root)
            dialog.title("Transladar Imagem")

        x_label = tk.Label(dialog, text="Translação em X (pixels):")
        x_label.pack()
        x_entry = tk.Entry(dialog)
        x_entry.pack()

        y_label = tk.Label(dialog, text="Translação em Y (pixels):")
        y_label.pack()
        y_entry = tk.Entry(dialog)
        y_entry.pack()

        def apply_translation():

            translate_x = int(x_entry.get())
            translate_y = int(y_entry.get())

            dialog.destroy()

            if translate_x != 0 or translate_y != 0:
                #defina a matriz de transformação
                translation_matrix = np.float32([[1, 0, translate_x], [0, 1, translate_y]])

                #aplica a translação na imagem
                self.transformed_image_copy = cv2.warpAffine(self.transformed_image_copy, translation_matrix, (self.transformed_image_copy.shape[1], self.transformed_image_copy.shape[0]))

                #att a exibição da imagem na interface
                self.display_image(self.transformed_image_copy, self.transformed_image_label)

        apply_button = tk.Button(dialog, text="Aplicar", command=apply_translation)
        apply_button.pack()

        pass
    
    def rotate_image(self):
        # rotacionar
        pass
    
    # espelhar - OK
    def mirror_image(self):
        if self.transformed_image_copy is not None:
            self.transformed_image_copy = cv2.flip(self.transformed_image_copy, 1)
            self.display_image(self.transformed_image_copy, self.transformed_image_label)
    
    def enlarge_image(self):
        # aumentar
        pass
    
    def reduce_image(self):
        # diminuir
        pass
    
    # grayscale
    def apply_grayscale(self):
            if self.transformed_image_copy is not None:
                gray_image = cv2.cvtColor(self.transformed_image_copy, cv2.COLOR_BGR2GRAY)
            self.display_image(gray_image, self.transformed_image_label)
            self.transformed_image_copy = gray_image
            pass
    
    # passa baixa
    def apply_low_pass(self, filter_type):
        if self.transformed_image_copy is not None:
            if filter_type == "Média":
                kernel = np.ones((6, 6), np.float32) / 36
                result = cv2.filter2D(self.transformed_image_copy, -1, kernel)
            elif filter_type == "Moda":
                kernel = np.ones((3, 3), np.uint8)
                result = cv2.medianBlur(self.transformed_image_copy, 3)
            elif filter_type == "Mediana":
                result = cv2.GaussianBlur(self.transformed_image_copy, (3, 3), 0)
            elif filter_type == "Gauss":
                result = cv2.GaussianBlur(self.transformed_image_copy, (5, 5), 0)

            self.transformed_image_copy = result
            self.display_image(self.transformed_image_copy, self.transformed_image_label)
    
    def apply_high_pass(self):
        # passa alta
        pass
    
    def apply_threshold(self):
        # threshold
        pass
    
    def apply_dilation(self):
        # dilatação
        pass
    
    def apply_erosion(self):
        # erosão
        pass
    
    def apply_opening(self):
        # abertura
        pass
    
    def apply_closing(self):
        # fechamento
        pass
    
    def challenge_feature(self):
        # desafio
        pass

    def remove_all_filters(self):
        if self.original_image is not None:
            self.transformed_image_copy = self.original_image.copy()
            self.display_image(self.transformed_image_copy, self.transformed_image_label)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()