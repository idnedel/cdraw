import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import Scale
from tkinter import simpledialog

class AplicativoProcessamentoDeImagens:
    def __init__(self, root):
        self.root = root
        self.root.title("CDraw")

        self.criar_layout()

        self.imagem_original = None
        self.imagem_transformada = None
        self.copia_imagem_transformada = None

        # Tela cheia ao abrir
        root.state('zoomed')

    def criar_layout(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # Divida a tela em duas metades com uma borda fina entre elas
        self.frame_original = tk.Frame(self.frame, borderwidth=1, relief="solid")
        self.frame_original.pack(side="left", fill="both", expand=True)

        self.frame_transformada = tk.Frame(self.frame, borderwidth=1, relief="solid")
        self.frame_transformada.pack(side="left", fill="both", expand=True)

        self.rotulo_imagem_original = tk.Label(self.frame_original)
        self.rotulo_imagem_original.pack(fill="both", expand=True)

        self.rotulo_imagem_transformada = tk.Label(self.frame_transformada)
        self.rotulo_imagem_transformada.pack(fill="both", expand=True)

        self.criar_menus()

    def criar_menus(self):
        barra_de_menu = tk.Menu(self.root)

        menu_arquivo = tk.Menu(barra_de_menu, tearoff=0)
        menu_arquivo.add_command(label="Abrir imagem", command=self.abrir_imagem)
        menu_arquivo.add_command(label="Salvar imagem", command=self.salvar_imagem)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sobre", command=self.mostrar_sobre)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.root.quit)
        barra_de_menu.add_cascade(label="Arquivo", menu=menu_arquivo)

        menu_geometrico = tk.Menu(barra_de_menu, tearoff=0)
        menu_geometrico.add_command(label="Transladar", command=self.transladar_imagem)
        menu_geometrico.add_command(label="Rotacionar", command=self.rotacionar_imagem)
        menu_geometrico.add_command(label="Espelhar", command=self.espelhar_imagem)
        menu_geometrico.add_command(label="Aumentar", command=self.aumentar_imagem)
        menu_geometrico.add_command(label="Diminuir", command=self.reduzir_imagem)
        barra_de_menu.add_cascade(label="Transformações Geométricas", menu=menu_geometrico)

        menu_pre_proc = tk.Menu(barra_de_menu, tearoff=0)
        menu_pre_proc.add_command(label="Grayscale", command=self.aplicar_grayscale)
        menu_pre_proc.add_command(label="Brilho", command=self.aplicar_brilho)
        menu_pre_proc.add_command(label="Contraste", command=self.aplicar_contraste)
        barra_de_menu.add_cascade(label="Pré-Processamento", menu=menu_pre_proc)

        menu_remover_filtro = tk.Menu(barra_de_menu, tearoff=0)
        menu_remover_filtro.add_command(label="Restaurar", command=self.remover_todos_os_filtros)
        barra_de_menu.add_cascade(label="Restaurar Imagem", menu=menu_remover_filtro)

        self.root.config(menu=barra_de_menu)

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

    # Transladar - não sei se isso aqui está certo
    def transladar_imagem(self):
        if self.copia_imagem_transformada is not None:
            dialogo = tk.Toplevel(self.root)
            dialogo.title("Transladar Imagem")

            x_label = tk.Label(dialogo, text="Translação em X (pixels):")
            x_label.pack()
            x_entry = tk.Entry(dialogo)
            x_entry.pack()

            y_label = tk.Label(dialogo, text="Translação em Y (pixels):")
            y_label.pack()
            y_entry = tk.Entry(dialogo)
            y_entry.pack()

            def aplicar_translacao():
                translacao_x = int(x_entry.get())
                translacao_y = int(y_entry.get())

                dialogo.destroy()

                if translacao_x != 0 or translacao_y != 0:
                    # Defina a matriz de transformação
                    matriz_translacao = np.float32([[1, 0, translacao_x], [0, 1, translacao_y]])

                    # Aplica a translação na imagem
                    self.copia_imagem_transformada = cv2.warpAffine(self.copia_imagem_transformada, matriz_translacao, (self.copia_imagem_transformada.shape[1], self.copia_imagem_transformada.shape[0]))

                    # Atualiza a exibição da imagem na interface
                    self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

            botao_aplicar = tk.Button(dialogo, text="Aplicar", command=aplicar_translacao)
            botao_aplicar.pack()

    def rotacionar_imagem(self):
        if self.copia_imagem_transformada is not None:
            # Gire a imagem em 90 graus
            self.copia_imagem_transformada = cv2.rotate(self.copia_imagem_transformada, cv2.ROTATE_90_CLOCKWISE)

            # Atualize a exibição da imagem na interface
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)


    # Espelhar - OK
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

    def reduzir_imagem(self):
        if self.copia_imagem_transformada is not None:
            pil_img = Image.fromarray(cv2.cvtColor(self.copia_imagem_transformada, cv2.COLOR_BGR2RGB))
            pil_img = ImageOps.fit(pil_img, (int(pil_img.width / 2.0), int(pil_img.height / 2.0)))
            self.copia_imagem_transformada = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

    # Grayscale
    def aplicar_grayscale(self):
        if self.copia_imagem_transformada is not None:
            imagem_em_escala_de_cinza = cv2.cvtColor(self.copia_imagem_transformada, cv2.COLOR_BGR2GRAY)
            self.exibir_imagem(imagem_em_escala_de_cinza, self.rotulo_imagem_transformada)
            self.copia_imagem_transformada = imagem_em_escala_de_cinza

    # Brilho
    def aplicar_brilho(self):
        if self.copia_imagem_transformada is not None:
            dialogo = tk.Toplevel(self.root)
            dialogo.title("Ajustar Brilho")

            escala_brilho = Scale(dialogo, from_=-100, to=100, resolution=1, orient="horizontal", label="Brilho")
            escala_brilho.set(0)  # Valor padrão inicial
            escala_brilho.pack()

            def aplicar_ajuste_brilho():
                fator_brilho = escala_brilho.get()

                imagem_ajustada = cv2.convertScaleAbs(self.copia_imagem_transformada, alpha=1.0, beta=fator_brilho)

                self.copia_imagem_transformada = imagem_ajustada
                self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

                dialogo.destroy()

            botao_aplicar = tk.Button(dialogo, text="Aplicar", command=aplicar_ajuste_brilho)
            botao_aplicar.pack()

    # Contraste
    def aplicar_contraste(self):
        if self.copia_imagem_transformada is not None:
            dialogo = tk.Toplevel(self.root)
            dialogo.title("Ajustar Contraste")

            escala_contraste = Scale(dialogo, from_=1.0, to=10, resolution=0.01, orient="horizontal", label="Contraste")
            escala_contraste.set(1.0)  # Valor padrão inicial
            escala_contraste.pack()

            def aplicar_ajuste_contraste():
                fator_contraste = escala_contraste.get()

                imagem_ajustada = cv2.convertScaleAbs(self.copia_imagem_transformada, alpha=fator_contraste, beta=0)

                self.copia_imagem_transformada = imagem_ajustada
                self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

                dialogo.destroy()

            botao_aplicar = tk.Button(dialogo, text="Aplicar", command=aplicar_ajuste_contraste)
            botao_aplicar.pack()

   
    def remover_todos_os_filtros(self):
        if self.imagem_original is not None:
            self.copia_imagem_transformada = self.imagem_original.copy()
            self.exibir_imagem(self.copia_imagem_transformada, self.rotulo_imagem_transformada)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoProcessamentoDeImagens(root)
    root.mainloop()
