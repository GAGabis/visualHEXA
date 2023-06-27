import cv2
import numpy as np
import math
import time
import tkinter as tk
from PIL import Image, ImageTk

# Função para redimensionar a imagem mantendo a proporção
def resize(image, width=None, height=None):
    if width is None and height is None:
        return image
    elif width is None:
        r = height / image.shape[0]
        dim = (int(image.shape[1] * r), height)
    else:
        r = width / image.shape[1]
        dim = (width, int(image.shape[0] * r))

    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Função para desenhar o texto em uma imagem
def draw_text(image, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.1
    font_thickness = 1
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

    x, y = position
    text_position = (x, y + int(text_size[1] * 0.1))
    cv2.putText(image, text, text_position, font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)

# Inicializar a janela Tkinter
window = tk.Tk()
window.title("Grid Window")

# Criar um widget Canvas para exibir as imagens
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# Captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Verifica se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Não foi possível abrir a webcam.")
    exit()

# Obtém as dimensões da tela
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calcula as dimensões das telas na grade
grid_width = screen_width // 2
grid_height = screen_height // 2

# Loop principal
def update_frame():
    # Captura o frame da webcam
    ret, frame = cap.read()

    if not ret:
        print("Não foi possível capturar o quadro.")
        return

    # Redimensiona a imagem da webcam para a resolução desejada
    resized_frame = resize(frame, width=grid_width, height=grid_height)

    # Cria uma imagem preta para o canto superior esquerdo
    black_screen = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    # Desenha um círculo vazado no canto inferior esquerdo
    circle_radius = min(grid_width, grid_height) // 2
    circle_center = (grid_width // 2, grid_height // 2)
    cv2.circle(black_screen, circle_center, circle_radius, (0, 255, 0), 2)

    # Adiciona a linha vertical que gira como um radar
    vertical_line_start = (
        int(circle_center[0]),
        int(circle_center[1] - circle_radius)
    )
    vertical_line_end = (
        int(circle_center[0]),
        int(circle_center[1] + circle_radius)
    )

    cv2.line(black_screen, vertical_line_start, vertical_line_end, (0, 255, 0), 2)

    # Cria uma imagem preta para a tabela
    table_screen = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    # Define os valores da tabela
    values = [
        "Value 1",
        "Value 2",
        "Value 3",
        "Value 4",
        "Value 5",
        "Value 6",
        "Value 7",
        "Value 8",
        "Value 9",
        "Value 10",
        "Value 11",
        "Value 12",
        "Value 13",
        "Value 14",
        "Value 15",
        "Value 16",
        "Value 17",
        "Value 18"
    ]

    # Divide os valores em duas colunas
    num_values_per_column = len(values) // 2
    values_col1 = values[:num_values_per_column]
    values_col2 = values[num_values_per_column:]

    # Define a posição inicial da primeira coluna
    table_start_pos = (20, 40)

    # Desenha os valores da primeira coluna
    for i, value in enumerate(values_col1):
        draw_text(table_screen, value, (table_start_pos[0], table_start_pos[1] + i * 40))

    # Define a posição inicial da segunda coluna
    table_start_pos_col2 = (table_start_pos[0] + grid_width // 2, table_start_pos[1])

    # Desenha os valores da segunda coluna
    for i, value in enumerate(values_col2):
        draw_text(table_screen, value, (table_start_pos_col2[0], table_start_pos_col2[1] + i * 40))

    # Redimensiona a imagem da webcam
    resized_frame = resize(frame, width=grid_width, height=grid_height)

    # Aplica o filtro Canny na imagem da webcam
    edges = cv2.Canny(resized_frame, 100, 200)

    # Cria uma imagem preta para o fundo
    black_background = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)

    # Define as cores das bordas e do fundo
    green_color = (0, 0, 255)
    black_color = (0, 0, 0)

    # Preenche o fundo com a cor preta
    black_background[:] = black_color

    # Copia as bordas para a imagem final
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    edges_colored[edges != 0] = (0, 255, 0)

    # Cria a imagem final combinando as telas usando np.concatenate
    top_row = np.concatenate((black_screen, resized_frame), axis=1)
    bottom_row = np.concatenate((table_screen, edges_colored), axis=1)
    full_screen = np.concatenate((top_row, bottom_row), axis=0)

    # Redimensiona a janela para preencher a tela mantendo a proporção
    resized_screen = resize(full_screen, width=screen_width, height=screen_height)

    # Converte a imagem do OpenCV para o formato PIL
    resized_screen_pil = Image.fromarray(resized_screen)

    # Cria um objeto ImageTk a partir da imagem PIL
    resized_screen_tk = ImageTk.PhotoImage(image=resized_screen_pil)

    # Cria uma label para exibir a imagem na janela Tkinter
    label = tk.Label(window, image=resized_screen_tk)
    label.pack()

    # Função para atualizar a imagem exibida
    def update_image():
        # Captura o frame da webcam
        ret, frame = cap.read()

        if not ret:
            print("Não foi possível capturar o quadro.")
            return

        # Redimensiona a imagem da webcam
        resized_frame = resize(frame, width=grid_width, height=grid_height)

        # Aplica o filtro Canny na imagem da webcam
        edges = cv2.Canny(resized_frame, 100, 200)

        # Cria as telas (black_screen, table_screen, edges_colored) novamente

        # Atualiza a imagem completa
        top_row = np.concatenate((black_screen, resized_frame), axis=1)
        bottom_row = np.concatenate((table_screen, edges_colored), axis=1)
        full_screen = np.concatenate((top_row, bottom_row), axis=0)

        # Redimensiona a janela para preencher a tela mantendo a proporção
        resized_screen = resize(full_screen, width=screen_width, height=screen_height)

        # Converte a imagem do OpenCV para o formato PIL
        resized_screen_pil = Image.fromarray(resized_screen)

        # Cria um objeto ImageTk a partir da imagem PIL
        resized_screen_tk = ImageTk.PhotoImage(image=resized_screen_pil)

        # Atualiza a label com a nova imagem
        label.configure(image=resized_screen_tk)
        label.image = resized_screen_tk

        # Chama a função novamente após um intervalo de tempo
        window.after(10, update_image)

    # Chama a função de atualização da imagem
    update_image()

    # Executa o loop principal do Tkinter
    window.mainloop()

    # Liberar a captura da webcam e destruir as janelas
    cap.release()
    cv2.destroyAllWindows()
