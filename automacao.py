import time
import pyautogui
import tkinter as tk
import cv2
import numpy as np
import threading

# Inicialização das coordenadas
area_cor = None
area_comprar = None
area_vender = None
gravando = False
frames_gravacao = []

def selecionar_area(area):
    def on_click(event, x, y, flags, param):
        nonlocal area
        if event == cv2.EVENT_LBUTTONDOWN:
            area = (x, y)
            cv2.destroyAllWindows()

    cv2.namedWindow('Selecione a Área')
    cv2.setMouseCallback('Selecione a Área', on_click)

    while area is None:  # Continue o loop até que uma área seja selecionada
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        cv2.imshow('Selecione a Área', screenshot)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return area

def verificar_cor(pixel):
    r, g, b = pixel
    if g > r and g > b:
        return "verde"
    else:
        return "vermelho"

def iniciar_automacao(area_cor):
    global gravando, frames_gravacao
    gravando = True
    while gravando:
        screenshot = pyautogui.screenshot()
        cor = screenshot.getpixel(area_cor)
        
        if area_comprar is not None and area_vender is not None:
            pixel_comprar = screenshot.getpixel(area_comprar)
            pixel_vender = screenshot.getpixel(area_vender)
            
            cor_detectada = verificar_cor(cor)
            
            if cor_detectada == "verde":
                pyautogui.click(area_comprar[0], area_comprar[1])
            elif cor_detectada == "vermelho":
                pyautogui.click(area_vender[0], area_vender[1])
        
        time.sleep(1)

def parar_automacao():
    global gravando
    gravando = False

def iniciar_interface_grafica():
    root = tk.Tk()

def iniciar_selecao_cor(t, param):
    global area_cor, area_comprar, area_vender
    area_cor = [None]
    area_comprar = [None]
    area_vender = [None]
    if t == 'area_cor':
        area_cor = selecionar_area(area_cor)
        print("Área de cor selecionada:", area_cor[0])
    elif t == 'area_comprar':
        area_comprar = selecionar_area(area_comprar)
        print("Área de cor selecionada:", area_comprar[0])
    elif t == 'area_vender':
        area_vender = selecionar_area(area_vender)
        print("Área de cor selecionada:", area_vender[0])

if __name__ == "__main__":
    interface_thread = threading.Thread(target=iniciar_interface_grafica)
    automacao_thread = threading.Thread(target=iniciar_automacao, args=(area_cor,))

    interface_thread.start()

    # Aguarde até que a interface gráfica seja fechada antes de iniciar a automação
    interface_thread.join()

    # Somente inicie a thread de automação após a interface gráfica ser fechada
    automacao_thread.start()
    automacao_thread.join()  # Aguarde a conclusão da automação, se necessário

# Criação da interface gráfica
root = tk.Tk()
root.title("Automatização")
root.geometry("340x300")
root.resizable(False, False)
root.configure(background="#1e1e1e")
root.attributes("-topmost", True)
# root.iconbitmap("icon.ico")
# root.wm_attributes("-transparentcolor", "#1e1e1e")
# root.wm_attributes("-alpha", 0.8)
root.wm_attributes("-toolwindow", True)
# root.wm_attributes("-fullscreen", True)
root.wm_attributes("-topmost", True)

padding_top = tk.Frame(root, height=0, bg="#1e1e1e")
title = tk.Label(root, text="Automatização", font=("Helvetica", 20, "bold"), background="#1e1e1e", foreground="white")
actions = tk.Frame(root, height=0, bg="#1e1e1e")
start_button = tk.Button(
    actions, 
    width=14,
    height=2, 
    text="Iniciar Automação", 
    font=("Helvetica", 10, "bold"), 
    background="limegreen", 
    command=lambda: iniciar_automacao(area_cor)
)
stop_button = tk.Button(
    actions, 
    width=14,
    height=2, 
    text="Parar Automação", 
    font=("Helvetica", 10, "bold"), 
    background="salmon", 
    command=parar_automacao
)
select_cor_button = tk.Button(
    root, 
    width=33,
    height=2, 
    text="Selecionar Área de Cor", 
    font=("Helvetica", 10, "bold"), 
    background="cornflowerblue", 
    border=2, 
    command=lambda: iniciar_selecao_cor('area_cor', area_cor)
)
select_comprar_button = tk.Button(
    root, 
    width=33,
    height=2, 
    text="Selecionar Área de Compra", 
    font=("Helvetica", 10, "bold"), 
    background="darksalmon", 
    command=lambda: iniciar_selecao_cor('area_comprar', area_comprar)
)
select_vender_button = tk.Button(
    root, 
    width=33,
    height=2, 
    text="Selecionar Área de Venda", 
    font=("Helvetica", 10, "bold"), 
    background="lightgreen", 
    command=lambda: iniciar_selecao_cor('area_vender', area_vender)
)
footer = tk.Frame(root, height=10, bg="#1e1e1e")
footer.grid_columnconfigure(0, weight=1)
footer.grid_columnconfigure(1, weight=1)
footer.grid_rowconfigure(0, weight=1)
footer_text = tk.Label(footer, text="© 2023,", font=("Helvetica", 8, "normal"), background="#1e1e1e", foreground="white")
footer_text_2 = tk.Label(footer, text="Daniel&Lucas", font=("Helvetica", 8, "bold"), background="#1e1e1e", foreground="white")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

title.grid(row=0, column=0, columnspan=3, rowspan=1, pady=10, padx=0, ipady=0, ipadx=0)
padding_top.grid(row=0, column=1, columnspan=1, rowspan=1, ipady=0, ipadx=0)

actions.grid(row=1, column=1, columnspan=1, rowspan=1, ipady=0, ipadx=0)
start_button.grid(row=1, column=0, columnspan=1, rowspan=1, pady=0, padx=5, ipady=0, ipadx=10)
stop_button.grid(row=1, column=2, columnspan=1, rowspan=1, pady=0, padx=5, ipady=0, ipadx=10)

select_cor_button.grid(row=3, column=1, columnspan=1, rowspan=1, ipady=0, ipadx=10)
select_comprar_button.grid(row=4, column=1, columnspan=1, rowspan=1, ipady=0, ipadx=10)
select_vender_button.grid(row=5, column=1, columnspan=1, rowspan=1, ipady=0, ipadx=10)

footer.grid(row=6, column=1, columnspan=1, rowspan=1, ipady=1, ipadx=0)
footer_text.grid(row=0, column=0, columnspan=1, rowspan=1, ipady=8, ipadx=0)
footer_text_2.grid(row=0, column=1, columnspan=1, rowspan=1, ipady=8, ipadx=0)

root.mainloop()
