import tkinter as tk

def option_selected(menu_name, option):
    print(f"Opção {option} do menu {menu_name} selecionada")

def create_window():
    window = tk.Tk()
    window.title("CDraw")
    window.config(padx=100, pady=300)

    def create_submenu(parent_menu, options):
        submenu = tk.Menu(parent_menu, tearoff=0)
        for option in options:
            submenu.add_command(label=option, command=lambda o=option: option_selected(parent_menu, o))
        return submenu

    # Frame para os botões
    button_frame = tk.Frame(window)
    button_frame.pack(pady=1)

    button1 = tk.Menubutton(button_frame, text="Arquivo")
    button1.menu = create_submenu(button1, ["Abrir", "Salvar", "Sobre", "Sair"])
    button1["menu"] = button1.menu

    button2 = tk.Menubutton(button_frame, text="Transformações Geométricas")
    button2.menu = create_submenu(button2, ["Transladar", "Rotacionar", "Espelhar", "Aumentar", "Diminuir"])
    button2["menu"] = button2.menu

    button3 = tk.Menubutton(button_frame, text="Filtros")
    button3.menu = create_submenu(button3, ["Grayscale", "Passa Baixa", "Passa Alta", "Threshold"])
    button3["menu"] = button3.menu

    button4 = tk.Menubutton(button_frame, text="Morfologia Matemática")
    button4.menu = create_submenu(button4, ["Dilatação", "Erosão", "Abertura", "Fechamento"])
    button4["menu"] = button4.menu

    button5 = tk.Menubutton(button_frame, text="Desafio")
    button5.menu = create_submenu(button5, ["Não Definido"])
    button5["menu"] = button5.menu

    button1.pack(side=tk.LEFT, padx=0)
    button2.pack(side=tk.LEFT, padx=0)
    button3.pack(side=tk.LEFT, padx=0)
    button4.pack(side=tk.LEFT, padx=0)
    button5.pack(side=tk.LEFT, padx=0)

    window.mainloop()

if __name__ == "__main__":
    create_window()
