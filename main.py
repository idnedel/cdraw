import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk,  ImageOps

class AplicativoProcessamentoImagem:
    def __init__(self, root):
        self.root = root
        self.root.title("CDraw")

        self.criar_layout()

        self.imagem_original = None
        self.imagem_transformada = None
        self.copia_imagem_transformada = None 
        self.filtros_aplicados = []  # Lista para rastrear os filtros aplicados

        # Tela cheia ao abrir
        root.state('zoomed')  
    
    def criar_layout(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # Divida a tela em duas metades com uma borda fina entre elas
        self.frame_original = tk.Frame(self.frame, borderwidth=1, relief="solid")
        self.frame_original.pack(side="left", fill="both", expand=True)

        self.frame_transformado = tk.Frame(self.frame, borderwidth=1, relief="solid")
        self.frame_transformado.pack(side="left", fill="both", expand=True)

        self.rotulo_imagem_original = tk.Label(self.frame_original)
        self.rotulo_imagem_original.pack(fill="both", expand=True)

        self.rotulo_imagem_transformada = tk.Label(self.frame_transformado)
        self.rotulo_imagem_transformada.pack(fill="both", expand=True)

        self.criar_menus()

    def criar_menus(self):
        barra_menu = tk.Menu(self.root)
        
        menu_arquivo = tk.Menu(barra_menu, tearoff=0)
        menu_arquivo.add_command(label="Abrir imagem", command=self.abrir_imagem)
        menu_arquivo.add_command(label="Salvar imagem", command=self.salvar_imagem)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sobre", command=self.mostrar_sobre)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.root.quit)
        barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)
        
        menu_geometrico = tk.Menu(barra_menu, tearoff=0)
        menu_geometrico.add_command(label="Transladar", command=self.transladar_imagem)
        menu_geometrico.add_command(label="Rotacionar", command=self.rotacionar_imagem)
        menu_geometrico.add_command(label="Espelhar", command=self.espelhar_imagem)
        menu_geometrico.add_command(label="Aumentar", command=self.aumentar_imagem)
        menu_geometrico.add_command(label="Diminuir", command=self.diminuir_imagem)
        barra_menu.add_cascade(label="Transformações Geométricas", menu=menu_geometrico)

        menu_pre_processamento = tk.Menu(barra_menu, tearoff=0)
        menu_pre_processamento.add_command(label="Grayscale", command=self.aplicar_grayscale)
        menu_pre_processamento.add_command(label="Brilho", command=self.aplicar_brilho)
        menu_pre_processamento.add_command(label="Contraste", command=self.aplicar_contraste)
        barra_menu.add_cascade(label="Pré-Processamento", menu=menu_pre_processamento)
        
        menu_filtro = tk.Menu(barra_menu, tearoff=0)
                # Submenu para "Passa Baixa"
        passa_baixa_menu = tk.Menu(barra_menu, tearoff=0)
        passa_baixa_menu.add_command(label="Média", command=lambda: self.apply_low_pass("Média"))
        passa_baixa_menu.add_command(label="Moda", command=lambda: self.apply_low_pass("Moda"))
        passa_baixa_menu.add_command(label="Mediana", command=lambda: self.apply_low_pass("Mediana"))
        passa_baixa_menu.add_command(label="Gauss", command=lambda: self.apply_low_pass("Gauss"))
        
        barra_menu.add_cascade(label="Passa Baixa", menu=passa_baixa_menu)
        menu_filtro.add_command(label="Passa Alta", command=self.apply_high_pass)
        menu_filtro.add_command(label="Threshold", command=self.apply_threshold)
        barra_menu.add_cascade(label="Filtros", menu=menu_filtro)

        morphology_menu = tk.Menu(barra_menu, tearoff=0)
        morphology_menu.add_command(label="Dilatação", command=self.apply_dilation)
        morphology_menu.add_command(label="Erosão", command=self.apply_erosion)
        morphology_menu.add_command(label="Abertura", command=self.apply_opening)
        morphology_menu.add_command(label="Fechamento", command=self.apply_closing)
        barra_menu.add_cascade(label="Morfologia Matemática", menu=morphology_menu)
        
        
    
        menu_remover_filtro = tk.Menu(barra_menu, tearoff=0)
        menu_remover_filtro.add_command(label="Restaurar", command=self.remover_todos_filtros)
        barra_menu.add_cascade(label="Restaurar Imagem", menu=menu_remover_filtro)
        
        self.root.config(menu=barra_menu)

    # Funções dos botões    
    def abrir_imagem(self):
        caminho_arquivo = filedialog.askopenfilename()
        if caminho_arquivo:
            self.imagem_original = cv2.imread(caminho_arquivo)

            # Cria cópia da imagem para aplicar os filtros
            self.copia_imagem_transformada = self.imagem_original.copy()
            
            # Dimensionar a imagem
            largura_maxima_exibicao = 600

            # original
            fator_escala = largura_maxima_exibicao / self.imagem_original.shape[1]
            self.imagem_original = cv2.resize(self.imagem_original, (largura_maxima_exibicao, int(self.imagem_original.shape[0] * fator_escala)))
            
            # cópia
            fator_escala = largura_maxima_exibicao / self.copia_imagem_transformada.shape[1]
            self.copia_imagem_transformada = cv2.resize(self.copia_imagem_transformada, (largura_maxima_exibicao, int(self.copia_imagem_transformada.shape[0] * fator_escala)))
            
            self.exibir_imagem(self.imagem_original, self.rotulo_imagem_original)
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

    def salvar_imagem(self):
        if self.copia_imagem_transformada is not None:
            caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Arquivos JPEG", "*.jpg")])
            if caminho_arquivo:
                cv2.imwrite(caminho_arquivo, self.copia_imagem_transformada)
                messagebox.showinfo("Informação", "Imagem salva com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem transformada para salvar.")
    
    def mostrar_sobre(self):
        messagebox.showinfo("Sobre", "CDraw - Ciência da Computação\nProcessamento Digital de Imagens\nCriado Por Matheus Nedel e Nícolas Dapper")
    
    def exibir_imagem(self, imagem, rotulo_widget):
        if imagem is not None:
            imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            imagem = Image.fromarray(imagem)
            foto = ImageTk.PhotoImage(image=imagem)
            rotulo_widget.config(image=foto)
            rotulo_widget.image = foto
        else:
            rotulo_widget.config(image=None)
    
    # transladar - não sei se isso aqui ta certo
    def transladar_imagem(self):
        if self.copia_imagem_transformada is not None:
            # Cria a janela de diálogo
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

            def aplicar_translacao():
                translacao_x = int(x_entry.get())
                translacao_y = int(y_entry.get())

                dialog.destroy()

                if translacao_x != 0 or translacao_y != 0:
                    # Define a matriz de transformação
                    matriz_translacao = np.float32([[1, 0, translacao_x], [0, 1, translacao_y]])

                    # Aplica a translação na imagem
                    self.copia_imagem_transformada = cv2.warpAffine(self.copia_imagem_transformada, matriz_translacao, (self.copia_imagem_transformada.shape[1], self.copia_imagem_transformada.shape[0]))

                    # Atualiza a exibição da imagem na interface
                    self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

            botao_aplicar = tk.Button(dialog, text="Aplicar", command=aplicar_translacao)
            botao_aplicar.pack()

    # rotacionar
    def rotacionar_imagem(self):
         if self.copia_imagem_transformada is not None:
            # Gire a imagem em 90 graus
            self.copia_imagem_transformada = cv2.rotate(self.copia_imagem_transformada, cv2.ROTATE_90_CLOCKWISE)

            # Atualize a exibição da imagem na interface
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

    # espelhar - OK
    def espelhar_imagem(self):
        if self.copia_imagem_transformada is not None:
            self.copia_imagem_transformada = cv2.flip(self.copia_imagem_transformada, 1)
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)
    
    def aumentar_imagem(self):
        if self.copia_imagem_transformada is not None:
            pil_img = Image.fromarray(cv2.cvtColor(self.copia_imagem_transformada, cv2.COLOR_BGR2RGB))
            pil_img = ImageOps.fit(pil_img, (2 * pil_img.width, 2 * pil_img.height))
            self.copia_imagem_transformada = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)
            
    def diminuir_imagem(self):
        if self.copia_imagem_transformada is not None:
            pil_img = Image.fromarray(cv2.cvtColor(self.copia_imagem_transformada, cv2.COLOR_BGR2RGB))
            pil_img = ImageOps.fit(pil_img, (int(pil_img.width / 2.0), int(pil_img.height / 2.0)))
            self.copia_imagem_transformada = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)
    
    # grayscale
    def aplicar_grayscale(self):
        if self.imagem_original is not None:
            self.filtros_aplicados.append("Grayscale")
        self.copia_imagem_transformada = cv2.cvtColor(self.copia_imagem_transformada, cv2.COLOR_BGR2GRAY)
        self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

    def aplicar_brilho(self):
        if self.copia_imagem_transformada is not None:
            self.filtros_aplicados.append("Brilho")
        valor_ajuste = 10  # Ajuste o valor do brilho conforme necessário
        self.copia_imagem_transformada = cv2.convertScaleAbs(self.copia_imagem_transformada, alpha=1, beta=valor_ajuste)
        self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)
        
    def aplicar_contraste(self):
        if self.copia_imagem_transformada is not None:
            self.filtros_aplicados.append("Contraste")
        valor_ajuste = 1.5  # Ajuste o valor do contraste conforme necessário
        self.copia_imagem_transformada = cv2.convertScaleAbs(self.copia_imagem_transformada, alpha=valor_ajuste)
        self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)
    
    # passa baixa
    def apply_low_pass(self, filter_type):
        if self.copia_imagem_transformada is not None:
            if filter_type == "Média":
                kernel = np.ones((5, 5), np.float32) / 25
                result = cv2.filter2D(self.copia_imagem_transformada, -1, kernel)
            elif filter_type == "Moda":
                kernel = np.ones((3, 3), np.uint8)
                result = cv2.medianBlur(self.copia_imagem_transformada, 3)
            elif filter_type == "Mediana":
                kernel = np.ones((3, 3), np.uint8)
                result = cv2.medianBlur(self.copia_imagem_transformada, 5)
            elif filter_type == "Gauss":
                result = cv2.GaussianBlur(self.copia_imagem_transformada, (5, 5), 1)

            self.copia_imagem_transformada = result
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)
    
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
        
    def remover_todos_filtros(self):
        if self.imagem_original is not None:
            self.copia_imagem_transformada = self.imagem_original.copy()
            
            # Remova todos os filtros aplicados
            self.filtros_aplicados = []

            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoProcessamentoImagem(root)
    root.mainloop()
