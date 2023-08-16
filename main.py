import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

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

        self.original_frame = tk.Frame(self.frame)
        self.original_frame.pack(side="left", fill="both", expand=True)

        self.transformed_frame = tk.Frame(self.frame)
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
        geometric_menu.add_command(label="Espelhar", command=self.flip_image)
        geometric_menu.add_command(label="Aumentar", command=self.enlarge_image)
        geometric_menu.add_command(label="Diminuir", command=self.reduce_image)
        menubar.add_cascade(label="Transformações Geométricas", menu=geometric_menu)
        
        filters_menu = tk.Menu(menubar, tearoff=0)
        filters_menu.add_command(label="Grayscale", command=self.apply_grayscale)
        filters_menu.add_command(label="Passa Baixa", command=self.apply_low_pass)
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
            scale_factor = max_display_width / self.original_image.shape[1]
            self.original_image = cv2.resize(self.original_image, (max_display_width, int(self.original_image.shape[0] * scale_factor)))
            
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
    
    def translate_image(self):
        # transladar
        pass
    
    def rotate_image(self):
        # rotacionar
        pass
    
    def flip_image(self):
        # espelhar
        pass
    
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
    
    def apply_low_pass(self):
        # passa baixa
        pass
    
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

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()