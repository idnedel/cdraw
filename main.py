import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        
        self.original_image_label = tk.Label(root)
        self.original_image_label.pack()
        
        self.transformed_image_label = tk.Label(root)
        self.transformed_image_label.pack()
        
        self.create_menus()
        
        self.original_image = None
        self.transformed_image = None

        root.attributes('-fullscreen', True)
        root.bind('<Escape>', lambda event: root.attributes('-fullscreen', False))
        
    def create_menus(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Abrir imagem", command=self.open_image)
        file_menu.add_command(label="Salvar imagem", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Sobre", command=self.show_about)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        menubar.add_cascade(label="ARQUIVO", menu=file_menu)
        
        geometric_menu = tk.Menu(menubar, tearoff=0)
        geometric_menu.add_command(label="Transladar", command=self.translate_image)
        geometric_menu.add_command(label="Rotacionar", command=self.rotate_image)
        geometric_menu.add_command(label="Espelhar", command=self.flip_image)
        geometric_menu.add_command(label="Aumentar", command=self.enlarge_image)
        geometric_menu.add_command(label="Diminuir", command=self.reduce_image)
        menubar.add_cascade(label="TRANSFORMAÇÕES GEOMÉTRICAS", menu=geometric_menu)
        
        filters_menu = tk.Menu(menubar, tearoff=0)
        filters_menu.add_command(label="Grayscale", command=self.apply_grayscale)
        filters_menu.add_command(label="Passa Baixa", command=self.apply_low_pass)
        filters_menu.add_command(label="Passa Alta", command=self.apply_high_pass)
        filters_menu.add_command(label="Threshold", command=self.apply_threshold)
        menubar.add_cascade(label="FILTROS", menu=filters_menu)
        
        morphology_menu = tk.Menu(menubar, tearoff=0)
        morphology_menu.add_command(label="Dilatação", command=self.apply_dilation)
        morphology_menu.add_command(label="Erosão", command=self.apply_erosion)
        morphology_menu.add_command(label="Abertura", command=self.apply_opening)
        morphology_menu.add_command(label="Fechamento", command=self.apply_closing)
        menubar.add_cascade(label="MORFOLOGIA MATEMÁTICA", menu=morphology_menu)
        
        features_menu = tk.Menu(menubar, tearoff=0)
        features_menu.add_command(label="DESAFIO", command=self.challenge_feature)
        menubar.add_cascade(label="EXTRAÇÃO DE CARACTERÍSTICAS", menu=features_menu)
        
        self.root.config(menu=menubar)
        
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.display_image(self.original_image, self.original_image_label)
    
    def save_image(self):
        if self.transformed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                cv2.imwrite(file_path, self.transformed_image)
                messagebox.showinfo("Info", "Imagem salva com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem transformada para salvar.")
    
    def show_about(self):
        messagebox.showinfo("Sobre", "Image Processing App\nCriado por [Seu Nome]")
    
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
        # Implement translation transformation
        pass
    
    def rotate_image(self):
        # Implement rotation transformation
        pass
    
    def flip_image(self):
        # Implement flip transformation
        pass
    
    def enlarge_image(self):
        # Implement image enlargement transformation
        pass
    
    def reduce_image(self):
        # Implement image reduction transformation
        pass
    
    def apply_grayscale(self):
        # Implement grayscale filter
        pass
    
    def apply_low_pass(self):
        # Implement low-pass filter
        pass
    
    def apply_high_pass(self):
        # Implement high-pass filter
        pass
    
    def apply_threshold(self):
        # Implement threshold filter
        pass
    
    def apply_dilation(self):
        # Implement dilation operation
        pass
    
    def apply_erosion(self):
        # Implement erosion operation
        pass
    
    def apply_opening(self):
        # Implement opening operation
        pass
    
    def apply_closing(self):
        # Implement closing operation
        pass
    
    def challenge_feature(self):
        # Implement your challenge feature here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', lambda event: root.attributes('-fullscreen', False))
    
    app = ImageProcessingApp(root)
    root.mainloop()